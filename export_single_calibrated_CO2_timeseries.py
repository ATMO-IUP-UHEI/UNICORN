#%% 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import matplotlib.colorbar as cbar
import xarray as xr
import pandas as pd
from scipy.optimize import curve_fit
from datetime import datetime, timedelta
import sys
sys.path.append("/home/sleyer/code/")
import importlib
from importlib import reload
import plotting_code
import read_data_advanced
import matplotlib.dates as dates
import os

#%%
#USER INPUT

#Calibration Period
start_time_fit=pd.to_datetime("2025-01-02 00:00:00")
end_time_fit=pd.to_datetime("2025-02-01 00:00:00")
#optional: set stop and restart time for gaps in calibration period
stop_time_fit=pd.to_datetime("2125-02-05 00:00:00")
restart_time_fit=pd.to_datetime('2005-02-25 00:00:00')

#Period for Timeseries
start_time_measurement=pd.to_datetime("2025-02-01 00:00:00")
end_time_measurement=pd.to_datetime("2025-10-21 00:00:00")
#optional: stop and restart time for a gap in evaluated data
stop_time_measurement=pd.to_datetime("2125-05-25 00:00:00")
restart_time_measurement=pd.to_datetime('2005-08-04 00:00:00')

node_nr = 1
location = 'IUP' #for file header
rs_int='1min' #alt: '1h', '1min'

#%% CALIBRATION

#read in beacon data and convert to xarray
#calculate data length in hours
time_difference = end_time_fit - start_time_fit
hours = int(time_difference.total_seconds() / 3600)
reload (read_data_advanced)
df = read_data_advanced.import_beacon_data(start_time_fit.year,start_time_fit.month,start_time_fit.day,start_time_fit.hour,hours,node_nr)
ds = df.set_index(['time']).to_xarray()

#read in reference datasets
reload(read_data_advanced)
df_ref = read_data_advanced.import_highprecision_data(2025,1)
ds_ref = df_ref.set_index(['date']).to_xarray()
ds_ref = ds_ref.rename({'date': 'time'}) #both coordinates have same name

#data resampling
print('resampling data...')
ds_resampled     = ds['CO2'].resample(time=rs_int).mean()
ds_resampled_RH  = ds['rh'].resample(time=rs_int).mean()
ds_resampled_Tdew = ds['temperature_dew'].resample(time=rs_int).mean()
ds_resampled_P   = ds['p'].resample(time=rs_int).mean()
ds_resampled_T2  = ds['temperature2'].resample(time=rs_int).mean()
ds_resampled_T   = ds['temperature'].resample(time=rs_int).mean()
print('resampling successfull')

#dry air and STP correction
def dry_co2_values(CO2,T_dew, T, P):
    P_H2O = 6.1094*np.exp(17.625*T_dew/(243.04+T_dew))
    return CO2 * 1013.25/P * (T + 273.15)/298.15 * 1/(1-(P_H2O/P))


ds_resampled_CO2 = dry_co2_values(ds_resampled, ds_resampled_Tdew, ds_resampled_T2, ds_resampled_P)

# Dataset  Alignment
print('aligning data')
valid_time_mask = ds_ref['time'].to_pandas().notna()
ds_ref_clean = ds_ref.isel(time=valid_time_mask)
ds_ref_clean_f = ds_ref_clean.where(ds_ref_clean['time'] >= np.datetime64(start_time_fit,'ns'), drop=True)
ds_ref_clean_ff = ds_ref_clean_f.where(np.datetime64(end_time_fit, 'ns') > ds_ref_clean_f['time'] , drop=True)

#resample reference data accordingly (has to be done here)
ds_ref_clean_ff=ds_ref_clean_ff.resample(time=rs_int).mean()

ds_ref_clean_ff['CO2'], ds_resampled_CO2 = xr.align(ds_ref_clean_ff['CO2'], ds_resampled_CO2, join="inner")
ds_resampled_CO2, ds_resampled_T = xr.align(ds_resampled_CO2, ds_resampled_T, join="inner")
ds_resampled_CO2, ds_resampled_T2 = xr.align(ds_resampled_CO2, ds_resampled_T2, join="inner")
ds_resampled_CO2, ds_resampled_RH = xr.align(ds_resampled_CO2, ds_resampled_RH, join="inner")
ds_resampled_CO2, ds_resampled_P = xr.align(ds_resampled_CO2, ds_resampled_P, join="inner")

# Filter the dataset based on time range
time_mask_cal = (((ds_resampled_CO2['time'] >= np.datetime64(start_time_fit, 'ns')) & (ds_resampled_CO2['time'] <= np.datetime64(stop_time_fit, 'ns'))) |
                 ((ds_resampled_CO2['time'] >= np.datetime64(restart_time_fit, 'ns')) & (ds_resampled_CO2['time'] <= np.datetime64(end_time_fit, 'ns'))))



CO2_raw = ds_resampled_CO2[time_mask_cal]
p = ds_resampled_P[time_mask_cal]
T = ds_resampled_T2[time_mask_cal]
rh = ds_resampled_RH[time_mask_cal]
CO2_ref = ds_ref_clean_ff['CO2'][time_mask_cal]
time=dates.date2num(CO2_raw['time']) #in days and fractions of days

# Remove NaNs
data = np.column_stack((CO2_raw, p, T, rh, CO2_ref, time))
mask = ~np.isnan(data).any(axis=1)

CO2_raw, p, T, rh, CO2_ref, time= CO2_raw[mask], p[mask], T[mask], rh[mask], CO2_ref[mask], time[mask]


mask_val=((300<=CO2_raw)&(CO2_raw<=1200)&(300<=CO2_ref)&(CO2_ref<=1200))

CO2_raw, p, T, rh, CO2_ref, time= CO2_raw[mask_val], p[mask_val], T[mask_val], rh[mask_val], CO2_ref[mask_val], time[mask_val]

#Heidelberg Fitting Method
print("performing fit....")
start_ind=np.argmin(np.abs(dates.date2num(start_time_fit)-dates.date2num(CO2_raw['time'])))
end_ind=np.argmin(np.abs(dates.date2num(end_time_fit)-dates.date2num(CO2_raw['time'])))

def fit_multi_lin2(vars, a0, a1, a2, asquared, a3, drift, y):
    CO2_raw, p, T, rh, time = vars
    return a0 * CO2_raw + (a1 * p + a2 * T + asquared*T**2 + a3 * rh + y)
    #return a0 * CO2_raw + (a1 * p + a2 * T + asquared*T**2 + a3 * rh + drift*(time-time[0]) y)
    
vars = (CO2_raw, p, T, rh, time)
vars_fit = (CO2_raw[start_ind:end_ind], p[start_ind:end_ind], T[start_ind:end_ind], rh[start_ind:end_ind], time[start_ind:end_ind])
params, covariance = curve_fit(fit_multi_lin2, vars_fit, CO2_ref[start_ind:end_ind], p0=[1, 0.1, 1, 0.1, 0.1, 0.0001, 50], bounds=([-2,-2,-40,-2,-2,-0.06,-400], [2, 2, 40, 2, 2, 0.06, 400]))
#params, covariance = curve_fit(fit_multi_lin2, vars, CO2_ref, p0=[1, 0.1, 1, 0.1, 0.1, 0.0001, 50])
a0, a1, a2, asquared, a3, drift, y = params
errors = np.sqrt(np.diag(covariance))

# Calculate residuals and R²
predicted = fit_multi_lin2(vars, a0, a1, a2, asquared, a3, drift, y)
residuals_fit = CO2_ref[start_ind:end_ind] - predicted[start_ind:end_ind]
ss_res = np.sum(residuals_fit ** 2)
ss_tot = np.sum((CO2_ref[start_ind:end_ind] - np.mean(CO2_ref[start_ind:end_ind])) ** 2)
r_squared = 1 - (ss_res / ss_tot)

residuals=CO2_ref - predicted
# Print results
print(f"Node "+str(node_nr)+" - Fitted Parameters:")
print(f"a_CO2 = {a0:.4f} ± {errors[0]:.4f}, a_p = {a1:.4f} ± {errors[1]:.4f}, a_T = {a2:.4f} ± {errors[2]:.4f}, a_T_squared = {asquared:.4f} ± {errors[3]:.4f}, a_RH = {a3:.4f} ± {errors[4]:.4f}, drift = {drift:.4f} ± {errors[5]:.4f}, y = {y:.4f} ± {errors[6]:.4f}")
print(f"$R^2$ = {float(r_squared):.4f}")
print("Covariance matrix:\n", covariance)

# %%
plt.figure(figsize=(8, 5))
plt.scatter(predicted, residuals, alpha=0.6,  c=dates.date2num(predicted['time']), cmap='plasma')
plt.axhline(0, color='red', linestyle='--', linewidth=1)
plt.xlabel(r'$CO_{2_{calib}}$ [ppm]')
plt.ylabel(r'residuals ($CO2_{ref} - CO2_{calib}$) [ppm]')
plt.title('residual plot - node '+str(node_nr))
plt.grid()
cbar=plt.colorbar()
tick_locs = cbar.get_ticks()
tick_labels = [mdates.num2date(tick).strftime('%Y-%m-%d') for tick in tick_locs]
cbar.set_ticks(tick_locs)
cbar.set_ticklabels(tick_labels)
cbar.set_label('Date')


plt.figure(figsize=(8,5))
plt.plot(predicted['time'], predicted, label='calibrated data', linewidth=.3)
plt.plot(predicted['time'], CO2_ref, label='reference', linewidth=.3)
plt.title('timeseries comparison - node '+str(node_nr))
plt.ylabel(r'$CO_2$ [ppm]')
plt.xlabel('time [UTC]')
plt.xticks(np.arange(start_time_fit, end_time_fit, 15*24*60*60*10**6))
leg = plt.legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(1.0)
    
mins=len(residuals)
    
plt.figure(figsize=(8,5))
hist = plt.hist(residuals, bins=100, range=(-20,20), color='grey', label='full time span')
hist1 = plt.hist(residuals[:np.int(mins/3)], bins=100, range=(-20,20), color='blue', label=str(np.array(residuals['time'][0]))[:-19]+' to '+str(np.array(residuals['time'][int(mins/3)]))[:-19], alpha=.6)
hist2 = plt.hist(residuals[np.int(mins/3):np.int(2*mins/3)], bins=100, range=(-20,20), color='red', label=str(np.array(residuals['time'][int(mins/3)]))[:-19]+' to '+str(np.array(residuals['time'][int(2*mins/3)]))[:-19], alpha=.6)
hist3 = plt.hist(residuals[np.int(2*mins/3):], bins=100, range=(-20,20), color='yellow', label=str(np.array(residuals['time'][int(2*mins/3)]))[:-19]+' to '+str(np.array(residuals['time'][int(mins-1)]))[:-19], alpha=.6)
plt.xlim(-20,20)
plt.title('accuracy - calibration of node '+str(node_nr))
plt.xlabel(r'$CO_{2_{ref}}-CO_{2_{calib}}$ [ppm]')
plt.ylabel('counts')
plt.legend(loc='upper left')

hist=np.histogram(residuals_fit, bins=100, range=(-20,20))
yg=hist[0]
x=hist[1][1:]

hist_full=np.histogram(residuals, bins=100, range=(-20,20))
y_full=hist_full[0]
x_full=hist_full[1][1:]


def gaussian (x, A, mu, sig):
    return A*np.exp(-0.5*((x-mu)/sig)**2)

poptg, pcovg = curve_fit(gaussian, x, yg)
poptg1, pcovg1 =curve_fit(gaussian, x_full, y_full)
plt.plot(x, gaussian(x, *poptg))
plt.plot(x_full, gaussian(x_full, *poptg1))
plt.text(.99,.99, r'$\sigma_{acc}$='+str(np.abs(np.round(poptg[2], 2)))+' ppm', ha='right', va='top', size=18, transform=plt.gca().transAxes)
plt.text(.99,.9, r'$\mu_{calib}$='+str(np.round(poptg[1],2))+' ppm', size=18, ha='right', va='top', transform=plt.gca().transAxes)

print('resolution: sigma= ', np.abs(poptg[2]), 'ppm')

acc=np.abs(np.round(poptg[2],2))
    
#%%

#OUTPUT CALIBRATED DATA
#calculate data length in hours
time_difference = end_time_measurement - start_time_measurement
hours = int(time_difference.total_seconds() / 3600)
#read in beacon data
print("read in measurement data...")
reload (read_data_advanced)
df = read_data_advanced.import_beacon_data(start_time_measurement.year,start_time_measurement.month,start_time_measurement.day,start_time_measurement.hour,hours,node_nr)
ds = df.set_index(['time']).to_xarray()

#data resampling
print('resampling data...')
ds_resampled     = ds['CO2'].resample(time=rs_int).mean()
ds_resampled_RH  = ds['rh'].resample(time=rs_int).mean()
ds_resampled_Tdew = ds['temperature_dew'].resample(time=rs_int).mean()
ds_resampled_P   = ds['p'].resample(time=rs_int).mean()
ds_resampled_T2  = ds['temperature2'].resample(time=rs_int).mean()
ds_resampled_T   = ds['temperature'].resample(time=rs_int).mean()
print('resampling successfull')

#dry air and STP correction

ds_resampled_CO2 = dry_co2_values(ds_resampled, ds_resampled_Tdew, ds_resampled_T2, ds_resampled_P)

# Dataset  Alignment
print('aligning data')

ds_resampled_CO2, ds_resampled_T = xr.align(ds_resampled_CO2, ds_resampled_T, join="inner")
ds_resampled_CO2, ds_resampled_T2 = xr.align(ds_resampled_CO2, ds_resampled_T2, join="inner")
ds_resampled_CO2, ds_resampled_RH = xr.align(ds_resampled_CO2, ds_resampled_RH, join="inner")
ds_resampled_CO2, ds_resampled_P = xr.align(ds_resampled_CO2, ds_resampled_P, join="inner")

# Filter the dataset based on time range
time_mask_cal = (((ds_resampled_CO2['time'] >= np.datetime64(start_time_measurement, 'ns')) & (ds_resampled_CO2['time'] <= np.datetime64(stop_time_measurement, 'ns'))) |
                 ((ds_resampled_CO2['time'] >= np.datetime64(restart_time_measurement, 'ns')) & (ds_resampled_CO2['time'] <= np.datetime64(end_time_measurement, 'ns'))))



CO2_raw = ds_resampled_CO2[time_mask_cal]
p = ds_resampled_P[time_mask_cal]
T = ds_resampled_T[time_mask_cal]
rh = ds_resampled_RH[time_mask_cal]
time=dates.date2num(CO2_raw['time']) #in days and fractions of days


vars = (CO2_raw, p, T, rh, time)
calibrated_CO2=fit_multi_lin2(vars, a0, a1, a2, asquared, a3, drift, y)

#%%

plt.plot(calibrated_CO2['time'], calibrated_CO2, label='calibrated', marker='.', markersize=.5, linestyle='none')
plt.plot(CO2_raw['time'], CO2_raw, label='raw', marker='.', markersize=.5, linestyle='none')
plt.xlim(pd.to_datetime(start_time_measurement),pd.to_datetime(end_time_measurement))
plt.ylim(400,600)
leg=plt.legend(markerscale=10)
plt.xlabel('time [UTC]')
plt.ylabel('CO2 [ppm]')
plt.title('preview of calibrated data output')

#%%

##Data_export
data = xr.Dataset({
    "CO2": calibrated_CO2,
    "p": p,
    "T": T,
    "rh": rh
})


header= (
    "# Node "+str(node_nr) +' '+str(location) +" - calibrated timeseries since deployment. Sampling interval"+str(rs_int), 
    "# Calibration method: a0*CO2_raw + (a1*p+ a2*T + asquared*T**2 + a3*rh + y) ",
    "# resulting minutely RMSE in calibration period: "+str(acc)+"ppm",
)


data.attrs["readme"]= header

data.to_netcdf('/home/sleyer/data/calibrated_data/unicorn'+str(node_nr)+'CO2_cal-rs'+str(rs_int)+'.cd')

df=data.to_dataframe()
df.to_csv('/home/sleyer/data/calibrated_data/unicorn'+str(node_nr)+'.csv')
with open("/home/sleyer/data/calibrated_data/unicorn"+str(node_nr)+".csv", "r+") as f:
    content = f.read()
    f.seek(0, 0)
    f.write("\n".join(header) + "\n" + content)
# %%
