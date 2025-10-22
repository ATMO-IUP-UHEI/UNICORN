# %%
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.dates as mdates
#%%
#def import_beacon_data(y=2025,m=5,d=19,h=0, readin=180, node=3, dir="/home/sleyer/data/beacon/"):
def import_beacon_data(y=2025,m=5,d=19,h=0, readin=180, node=3, dir="/net/dsvr-02/mnt/data2/UNICORN/raw_data"):


    """
    Reads in CSV files from BEACO2N nodes.

    Args:
        y (int): starting time, year
        m (int): starting time, month
        d (int): starting time, day
        h (int): starting time, hours
        readin (int): number of files to read
        dir (String): directory of csv files
    
    Returns: 
        return_type: pandas DataFrame
    """

    date_start = datetime(y, m, d, h)  # Anfangsdatum und -Uhrzeit
    files_readin = readin #Anzahl Dateien

    dfs = [] # Liste für Dateien als pandas df
    current_date = date_start

    for h_index in range(files_readin): #h_index entspricht Stunden (und somit den Fileabständen)
        current_date = date_start + timedelta(hours=h_index)  # nächster Tag, wenn Stunden > 23
        formatted_date = current_date.strftime('%Y_%m_%d-%H')  # Format: 2024_10_23-09
        filename = f"DEnode{node}-{formatted_date}.csv"
        # Einlesen der Dateien
        path=f"{dir}/unicorn"+f"{node:02d}"+f"/{filename}"
        try:
            df = pd.read_csv(path,header=None)
            # For Debugging: 
            # print('reading:', filename)
            dfs.append(df)
        except FileNotFoundError: #falls eine Datei fehlt
            print(f"Datei {path} nicht gefunden. Überspringe...")
            continue

    # füge alle Files zusammen
    df = pd.concat(dfs, ignore_index=True)
    
    df = df.rename(columns={
        1: 'p',
        2: 'temperature',
        3: 'rh',
        4: 'temperature_dew',
        5: 'pm1',
        6: 'pm2_5',
        7: 'pm10',
        8:'O3',
        9:'O3_aux',
        10: 'CO',
        11: 'CO_aux',
        12:'NO',
        13:'NO_aux',
        14:'NO2',
        15:'NO2_aux',
        19: 'CO2',
        20: 'temperature2', 
        21: 'time'
    })

    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    
    
    df['temperature'] = df['temperature'].replace(-999, np.nan)
    df['temperature'] = df['temperature'].replace('-999', np.nan)
    df['temperature2'] = df['temperature2'].replace(-999, np.nan)
    df['temperature_dew'] = df['temperature_dew'].replace(-999, np.nan)
    df['temperature_dew'] = df['temperature_dew'].replace('-999', np.nan)
    df['rh'] = df['rh'].replace(-999, np.nan)
    df['rh'] = df['rh'].replace('-999', np.nan)
    df['p'] = df['p'].replace(-999, np.nan)
    df['pm1'] = df['pm1'].replace(-999, np.nan)
    df['pm2_5'] = df['pm2_5'].replace(-999, np.nan)
    df['pm10'] = df['pm10'].replace(-999, np.nan)
    df['CO2'] = df['CO2'].replace(-999, np.nan)
    df['CO'] = df['CO'].replace(-999, np.nan)
    df['CO_aux'] = df['CO_aux'].replace(-999, np.nan)
    df['O3'] = df['O3'].replace(-999, np.nan)
    df['O3_aux'] = df['O3_aux'].replace(-999, np.nan)
    df['NO'] = df['NO'].replace(-999, np.nan)
    df['NO_aux'] = df['NO_aux'].replace(-999, np.nan)
    df['NO2'] = df['NO2'].replace(-999, np.nan)
    df['NO2_aux'] = df['NO2_aux'].replace(-999, np.nan)

    df.set_index(['time'], inplace=True)
    df.index = pd.to_datetime(df.index, errors='coerce')
    # Drop rows where the index is NaT (datetime is missing)
    df = df[df.index.notna()]

    #filter out bad data during shutoff RPI each day
    # [] is mask which only keeps this rows,, ~negates
    #so only rows not in that time range are kept
    df = df[~((df.index.time >= pd.to_datetime("16:26:00").time()) &
              (df.index.time <= pd.to_datetime("16:31:00").time()))]
    
    df['CO2_mean'] = df['CO2'].resample('1min').mean()
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['p'] = pd.to_numeric(df['p'], errors='coerce')
    df['rh'] = pd.to_numeric(df['rh'], errors='coerce')
    df['temperature_dew'] = pd.to_numeric(df['temperature_dew'], errors='coerce')

    

    

    #for i, value in enumerate(df['temperature']):
        #try:
            #float(value)
        #except ValueError:
            #df['temperature']=df['temperature'].replace({value}, np.nan) 
    for i, value in enumerate(df['temperature_dew']):
        try:
            float(value)
        except ValueError:
            df['temperature_dew']=df['temperature_dew'].replace({value}, np.nan) 
    for i, value in enumerate(df['rh']):
        try:
            float(value)
        except ValueError:
            df['rh']=df['rh'].replace({value}, np.nan) 

    print(df.head())
    print("hello")
    df = df.reset_index()
    return df

# %%
def import_highprecision_data(year=2025,month=1, dir="/net/dsvr-02/mnt/data2/UNICORN/reference_data"):
    try:
        df = pd.read_csv(f"{dir}/Daten_HD_1min_CO2_{year}.csv")
    except FileNotFoundError: #falls eine Datei fehlt
        #print(f"Datei nicht gefunden. Überspringe...")
        df['date'] = df['date'].astype(str).str.strip()  # Ensure all entries are strings



    # Convert to datetime safely
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df[(df['date'].dt.hour != 0) | (df['date'].dt.minute != 0) | (df['date'].dt.second != 0)] #filters out row at each day at midnight cause dayformat is not correct there(hours, min, s missing)

    return df

# %% Import of CO reference data
def import_CO_data(dir="/net/dsvr-02/mnt/data2/UNICORN/referencedata"):
    try:
        df = pd.read_csv(f"{dir}/CO_data.csv")
    except FileNotFoundError: #falls eine Datei fehlt
        print(f"Datei nicht gefunden")



    # Convert to datetime safely
    df['date'] = pd.to_datetime(df['startdate'], errors='coerce')
    df = df[(df['date'].dt.hour != 0) | (df['date'].dt.minute != 0) | (df['date'].dt.second != 0)] #filters out row at each day at midnight cause dayformat is not correct there(hours, min, s missing)
    ds= df.set_index(['date']).to_xarray()
    return ds



# %%
def import_weatherstation_data(year=2024,month=12,day=14,readin=200,dir="/home/phaas/beacon/data/weatherstation/"):
    date_start = datetime(year, month, day)  # Anfangsdatum und -Uhrzeit
    files_readin = readin #Anzahl Dateien

    dfs = [] # Liste für Dateien als pandas df
    current_date = date_start

    for day_index in range(files_readin): #h_index entspricht Stunden (und somit den Fileabständen)
        current_date = date_start + timedelta(days=day_index)  # nächster Tag, wenn Stunden > 23
        formatted_date = current_date.strftime('%y%m%d')  # Format: 2024_10_23-09
        try:
            df = pd.read_csv(f"{dir}HEImeteo_{formatted_date}.dat",sep=";",comment='#')
            dfs.append(df)
        except FileNotFoundError: #falls eine Datei fehlt
            print(f"Datei nicht gefunden. Überspringe...")
    

    # füge alle Files zusammen
    df = pd.concat(dfs, ignore_index=True)
    df['IntvlStart'] = pd.to_datetime(df['IntvlStart'])
    return df

# %%

ref=import_highprecision_data()

# %%