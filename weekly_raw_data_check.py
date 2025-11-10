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
import read_data_advanced
import matplotlib.dates as dates
import os

#%%
#USER INPUT
#set time period from monday of this week at midnight to exactly one week before
start_time = pd.to_datetime(dates.num2date(dates.date2num(pd.to_datetime(datetime.now().date()))-7-datetime.now().isoweekday()+1))
end_time = pd.to_datetime(dates.num2date(dates.date2num(datetime.now().date())-datetime.now().isoweekday()+1))

nodes_to_eval = [1,2,3,4,5,7,8,9,10,12,13,14,15,16,17]
#nodes_to_eval=[1,2,4]
rs_int='1min' #alt: '1h', '1min'

#calculate data length in hours
time_difference = end_time - start_time
hours = int(time_difference.total_seconds() / 3600)

#plot-datanames
plot_path=str("/home/sleyer/plots/sanity_checks/raw data week "+str(start_time)[:-15]+"/")

if not os.path.isdir(plot_path):
    os.makedirs(plot_path)

# %%
#DATA Import

time_difference = end_time - start_time
hours = int(time_difference.total_seconds() / 3600)


raw_data=[]


for i in nodes_to_eval:
    
        #read in beacon data
        print("read in  data from node"+str(i)+"...")
        reload (read_data_advanced)
        df = read_data_advanced.import_beacon_data(start_time.year,start_time.month,start_time.day,start_time.hour,hours,i)
        ds = df.set_index(['time']).to_xarray()

        #data resampling
        print('resampling data...')
        #ds_resampled_CO2     = ds['CO2'].resample(time=rs_int).mean()
        #ds_resampled_RH  = ds['rh'].resample(time=rs_int).mean()
        #ds_resampled_Tdew = ds['temperature_dew'].resample(time=rs_int).mean()
        #ds_resampled_P   = ds['p'].resample(time=rs_int).mean()
        #ds_resampled_T2  = ds['temperature2'].resample(time=rs_int).mean()
        #ds_resampled_T   = ds['temperature'].resample(time=rs_int).mean()
            
        ds_resampled = ds.resample(time=rs_int).mean()
            
        print('resampling successfull')
        raw_data.append(ds_resampled)
                
raw_data_ds = xr.concat(raw_data, dim='node')
#%%
#for more robust code experimenting: temp save data to save on long read-in times
df=raw_data_ds.to_dataframe()
df.to_csv(plot_path+'data_temp.csv')
#%%
#if needed:read in pre-saved data
#readin=pd.read_csv(plot_path+'data_temp.csv')
#raw_data_ds = readin.set_index(['time', 'node']).to_xarray()

# %%
# Plot Temperature
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['temperature'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck Temperature Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'temperature.png')
# %%
# Plot Temperature2
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['temperature2'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck  int. Temperature Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'temperature2.png')
# %%
# Plot Pressure
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['p'].plot(ax=ax, color='tab:blue', ylim=(980,1025))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck pressure Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'pressure.png')
# %%
# Plot rh
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['rh'].plot(ax=ax, color='tab:blue', ylim=(0,100))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck rh Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'rh.png')
# %%
# Plot pm1
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=False)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['pm1'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw pm1 Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'pm1.png')
# %%
# Plot pm2_5
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=False)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['pm2_5'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw pm2_5 Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'pm2_5.png')
# %%
# Plot pm10
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=False)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['pm10'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw pm10 Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'pm10.png')
# %%
# Plot O3
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    (ds['O3']-ds['O3_aux']).plot(ax=ax, color='tab:blue', ylim=(-0.05, 0.05))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw O3 (working-aux) Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'O3.png')

# %%
# Plot CO
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    (ds['CO']-ds['CO_aux']).plot(ax=ax, color='tab:blue', ylim=(0,0.5))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw CO (work-aux) Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'CO.png')
# %%

# Plot NO
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    (ds['NO']-ds['NO_aux']).plot(ax=ax, color='tab:blue', ylim=(-0.05, 0.15))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw NO Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'NO.png')
# %%
# Plot NO2
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    (ds['NO2']-ds['NO2_aux']).plot(ax=ax, color='tab:blue', ylim=(-0.03, 0.03))
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw NO2 Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'NO2.png')
# %%
# Plot CO2
fig, axes = plt.subplots(6, 3, figsize=(22, 22), sharex=True, sharey=True)
axes = axes.flatten()  # flache Liste für einfacheren Zugriff

for i in range(len(nodes_to_eval)):
    ax = axes[nodes_to_eval[i]-1]
    
     # Beispiel: Daten aus deinem Dictionary oder Dataset holen
    ds = raw_data_ds.isel(node=i)
    
    # z. B. Temperatur plotten
    ds['CO2'].plot(ax=ax, color='tab:blue')
    
    ax.set_title(f'Node {nodes_to_eval[i]}')
    ax.grid(True, alpha=0.3)

# Leere Subplots ausblenden, wenn du weniger als 20 Plots hast
for j in range(len(axes)):
    if j+1 not in nodes_to_eval:
        fig.delaxes(axes[j])

fig.suptitle("Sanitycheck raw CO2 Week "+str(start_time)[:-15], fontsize=18)
#plt.tight_layout()
plt.savefig(plot_path+'CO2_raw.png')
# %%
