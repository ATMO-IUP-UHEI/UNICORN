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
ds_node1=pd.read_csv('/home/sleyer/data/calibrated_data/unicorn1.csv', skiprows=3)
ds_node2=pd.read_csv('/home/sleyer/data/calibrated_data/unicorn2.csv', skiprows=3)
ds_node3=pd.read_csv('/home/sleyer/data/calibrated_data/unicorn3.csv', skiprows=3)
# %%
start_time_plot=pd.to_datetime('2025-09-22 T00:00:00')
end_time_plot=pd.to_datetime('2025-10-20  T00:00:00')

mask1=((pd.to_datetime(ds_node1['time'])<=end_time_plot)&(pd.to_datetime(ds_node1['time'])>=start_time_plot))
ds_node1m=ds_node1[mask1]

mask2=((pd.to_datetime(ds_node2['time'])<=end_time_plot)&(pd.to_datetime(ds_node2['time'])>=start_time_plot))
ds_node2m=ds_node2[mask2]

mask3=((pd.to_datetime(ds_node3['time'])<=end_time_plot)&(pd.to_datetime(ds_node3['time'])>=start_time_plot))
ds_node3m=ds_node3[mask3]

mask=((ds_node3m['CO2'])>=400)
ds_node3m=ds_node3m[mask]
# %%
plt.figure(figsize=(7,3))
plt.plot(pd.to_datetime(ds_node1m['time']), ds_node1m['CO2'], label='IUP', linewidth='.2')
plt.plot(pd.to_datetime(ds_node2m['time']), ds_node2m['CO2'], label='Czernyring', linewidth='.2')
plt.plot(pd.to_datetime(ds_node3m['time']), ds_node3m['CO2'], label='Eppelheim', linewidth='.2')
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(minticks=3, maxticks=7))
plt.title('calibrated UNICORN CO2 timeseries')
plt.ylabel(r'$CO_2$ [ppm]')
plt.xlabel('time [UTC]')
leg=plt.legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(2)

plt.gca().xaxis.set_minor_locator(mdates.DayLocator(interval=1))

# Gitterlinien aktivieren
plt.gca().grid(True, which='major', linestyle='-', linewidth=0.8)
plt.gca().grid(True, which='minor', linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.savefig('/home/sleyer/plots/calib_CO2_Oct_IUP_CZE_EPP.pdf', dpi=300)
# %%
