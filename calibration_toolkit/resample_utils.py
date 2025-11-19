import numpy as np
import xarray as xr
from . import read_data_advanced
from . import  calibration as cali

"""
resample_utils.py

Eine Sammlung von Hilfsfunktionen zum import, resampling, alignment und filtern von Beacon Daten

Funktionen:
-----------
- import_datasets(cfg, start_time=None, end_time=None)
    Liest Sensordaten vom Beacon sowie Hochpräzisionsreferenzdaten ein.

- resample_datasets(ds, interval, cfg)
    Resampelt alle Messgrößen auf ein einheitliches Zeitintervall.

- align_datasets(ds_ref, ds_resampled, cfg, start_time=None, end_time=None)
    Synchronisiert Sensor- und Referenzdaten auf gemeinsame Zeitpunkte.
    Liefert zusätzlich numerische Zeitwerte für Fitfunktionen.

- filter_calibration_data(gas_ref, gas_raw, p, T, rh, cfg)
    Filtert Daten nach Kalibrierzeitraum, entfernt NaNs und optional Werte außerhalb eines spezifizierten Bereichs.
"""

def import_datasets(cfg, start_time=None, end_time=None):
    """Import beacon and reference datasets. Optional: custom time window."""
    print("Importing datasets...")
    if start_time is None: start_time = cfg["start_time_fit"]
    if end_time is None:   end_time   = cfg["end_time_fit"]

    hours = int((end_time - start_time).total_seconds() / 3600)


    df = read_data_advanced.import_beacon_data(
        start_time.year, start_time.month, start_time.day, start_time.hour,
        hours, cfg["node_nr"]
    )
    ds = df.set_index(["time"]).to_xarray()

    if cfg["gas"] == "CO2":
        df_ref = read_data_advanced.import_highprecision_data(start_time.year, start_time.month)
        ds_ref = df_ref.set_index(["date"]).to_xarray().rename({"date": "time"})

    return ds, ds_ref



def resample_datasets(ds, interval, cfg):
    """Resample main dataset variables."""
    print("Resampling data...")
    gas = cfg["gas"]
    resampled = {
        gas: ds[gas].resample(time=interval).mean(),
        "RH": ds["rh"].resample(time=interval).mean(),
        "Tdew": ds["temperature_dew"].resample(time=interval).mean(),
        "P": ds["p"].resample(time=interval).mean(),
        "T2": ds["temperature2"].resample(time=interval).mean(),
        "T": ds["temperature"].resample(time=interval).mean(),
    }
    print("Resampling successful.")
    return resampled





def align_datasets(ds_ref, ds_resampled, cfg, start_time=None, end_time=None):
    print("Aligning data...")
    
    gas = cfg["gas"]  

    if start_time is None:
        start_time = cfg["start_time_fit"]
    if end_time is None:
        end_time = cfg["end_time_fit"]

    # Clean reference data: remove NaT entries
    valid_time_mask = ds_ref["time"].to_pandas().notna()
    ds_ref_clean = ds_ref.isel(time=valid_time_mask)

    # Slice reference dataset to calibration period
    ds_ref_period = ds_ref_clean.where(
        (ds_ref_clean["time"] >= np.datetime64(start_time, "ns")) &
        (ds_ref_clean["time"] <= np.datetime64(end_time, "ns")),
        drop=True
    )

    # Resample reference dataset
    ds_ref_period = ds_ref_period.resample(time=cfg["rs_int"]).mean()

    # ---------- ALIGN ----------
    # Gas first (this is the dataset we align everything to)
    ds_ref_gas, ds_gas = xr.align(ds_ref_period[gas], ds_resampled[gas], join="inner")

    # Then align remaining variables to ds_gas
    ds_gas, ds_T = xr.align(ds_gas, ds_resampled["T"], join="inner")
    ds_gas, ds_T2 = xr.align(ds_gas, ds_resampled["T2"], join="inner")
    ds_gas, ds_RH = xr.align(ds_gas, ds_resampled["RH"], join="inner")
    ds_gas, ds_P  = xr.align(ds_gas, ds_resampled["P"], join="inner")

    # Numeric time axis
    time_vals = ds_gas.time.values.astype("datetime64[s]").astype(float)

    return ds_ref_gas, ds_gas, ds_T, ds_T2 , ds_RH, ds_P, time_vals




def filter_calibration_data(gas_ref, gas_raw,T1, T2, rh, p , cfg):
    """
    Generalized calibration filter for arbitrary gas defined in cfg["gas"].
    gas_raw:   sensor gas concentration (e.g. CO2_raw)
    gas_ref:   reference gas concentration (e.g. CO2_ref)
    """

    gas = cfg["gas"]           # e.g. "CO2"
    start1 = np.datetime64(cfg["start_time_fit"], "ns")
    stop1  = np.datetime64(cfg["stop_time_fit"], "ns")
    start2 = np.datetime64(cfg["restart_time_fit"], "ns")
    stop2  = np.datetime64(cfg["end_time_fit"], "ns")

    # Zeitfenster-Maske
    time_mask = (
        ((gas_raw.time >= start1) & (gas_raw.time <= stop1)) |
        ((gas_raw.time >= start2) & (gas_raw.time <= stop2))
    )

    # Auf Zeitfenster trimmen
    gas_raw = gas_raw.sel(time=time_mask)
    p       = p.sel(time=time_mask)
    T1       = T1.sel(time=time_mask)
    T2       = T2.sel(time=time_mask)
    rh      = rh.sel(time=time_mask)
    gas_ref = gas_ref.sel(time=time_mask)

    # NaN-Maske
    mask_valid = (
        np.isfinite(gas_raw.values) &
        np.isfinite(p.values) &
        np.isfinite(T1.values) &
        np.isfinite(T2.values) &
        np.isfinite(rh.values) &
        np.isfinite(gas_ref.values)
    )

    # Für alle identische gültige Zeitpunkte behalten
    gas_raw = gas_raw.isel(time=mask_valid)
    p       = p.isel(time=mask_valid)
    T1       = T1.isel(time=mask_valid)
    T2       = T2.isel(time=mask_valid)
    rh      = rh.isel(time=mask_valid)
    gas_ref = gas_ref.isel(time=mask_valid)

    # Optionaler Bereichsfilter
    if "val_min" in cfg and "val_max" in cfg:
        val_min = cfg["val_min"]
        val_max = cfg["val_max"]

        valid_val_mask = (
            (gas_raw >= val_min) & (gas_raw <= val_max) &
            (gas_ref >= val_min) & (gas_ref <= val_max)
        )

        gas_raw = gas_raw.where(valid_val_mask, drop=True)

        # Zeitachsen synchron halten
        p       = p.sel(time=gas_raw.time)
        T1       = T1.sel(time=gas_raw.time)
        T2       = T2.sel(time=gas_raw.time)
        rh      = rh.sel(time=gas_raw.time)
        gas_ref = gas_ref.sel(time=gas_raw.time)

    # Zeit → numerisch (für Fits)
    time_vals = gas_raw.time.values.astype("datetime64[s]").astype(float)

    return gas_ref, gas_raw,T1, T2, rh, p , time_vals

def prepare_dataset_for_cali(cfg):
    ds, ds_ref = import_datasets(cfg)
    ds_resampled = resample_datasets(ds, cfg["rs_int"],cfg)
    if cfg["gas"] == "CO2":
        ds_resampled["CO2"]= cali.dry_co2_values(ds_resampled["CO2"], ds_resampled["Tdew"], ds_resampled["T2"], ds_resampled["P"])
    gas_ref, gas_raw,T1, T2, rh, p , time= align_datasets(ds_ref, ds_resampled, cfg)
    gas_ref, gas_raw,T1, T2, rh, p , time = filter_calibration_data(gas_ref, gas_raw,T1, T2, rh, p ,  cfg)
   
    print("Calibration dataset prepared successfully.")
    return gas_ref, gas_raw, p, T2, rh,  time
