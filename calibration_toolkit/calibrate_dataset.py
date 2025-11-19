from . import resample_utils as ru
from . import  calibration as cali
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr


def create_calibrated_dataset(cfg, *params, acc, fit_func= cali.fit_multi_lin2, filename = None, base_path = "/home/tvoss/code/data/calibrated_data/"):
    """
    Erstellt und speichert einen kalibrierten Datensatz basierend auf der Multi-Linearen Fitfunktion.
    Nutzt Version A der Import/Resample/Align-Funktionen (import_datasets, resample_datasets, align_datasets).

    Konfiguration erfolgt ausschließlich über cfg.
    """

    # --- CONFIG PARAMETER ---
    start_time = cfg["start_time_measurement"]
    end_time   = cfg["end_time_measurement"]
    stop_time  = cfg["stop_time_measurement"]
    restart_time = cfg["restart_time_measurement"]
    rs_int     = cfg["rs_int"]

    print("\n=== STEP 1: Import datasets ===")
    ds, ds_ref = ru.import_datasets(cfg, start_time= start_time, end_time=end_time)   # nutzt automatisch *_fit oder *_measurement je nach cfg


    print("\n=== STEP 2: Resample measurement data ===")
    ds_resampled = ru.resample_datasets(ds, rs_int, cfg)

    print("\n=== STEP 3: Compute dry CO2 ===")
    ds_resampled["CO2_dry"] = cali.dry_co2_values(
        ds_resampled["CO2"],
        ds_resampled["Tdew"],
        ds_resampled["T2"],
        ds_resampled["P"]
    )


    print("\n=== STEP 4: Skip alignment (measurement mode) ===")

    ds_CO2 = ds_resampled["CO2_dry"]
    ds_T2  = ds_resampled["T2"]
    ds_RH  = ds_resampled["RH"]
    ds_P   = ds_resampled["P"]

    time_vals = ds_CO2.time.values.astype("datetime64[s]").astype(float)

    # --- TIME MASK FOR MEASUREMENT PERIOD ---

    time_mask = (
        ((ds_CO2["time"] >= np.datetime64(start_time, "ns")) &
         (ds_CO2["time"] <= np.datetime64(stop_time, "ns"))) |
        ((ds_CO2["time"] >= np.datetime64(restart_time, "ns")) &
         (ds_CO2["time"] <= np.datetime64(end_time, "ns")))
    )

    CO2_raw  = ds_CO2[time_mask]
    p        = ds_P[time_mask]
    T        = ds_T2[time_mask]
    rh       = ds_RH[time_mask]
    time_num = time_vals[time_mask.values]  # already numeric seconds

    

    # --- MULTI-LINEAR APPLICATION ---
    print("\n=== STEP 5: Apply calibration model ===")
    vars = (CO2_raw, p, T, rh, time_num)
    calibrated_CO2 = fit_func(vars, *params)
    
    # --- PREVIEW PLOT ---
    plt.figure(figsize=(12, 5))
    plt.plot(calibrated_CO2["time"], calibrated_CO2, '.', markersize=1, label="calibrated")
    plt.plot(CO2_raw["time"], CO2_raw, '.', markersize=1, label="raw")
    plt.xlim(start_time, end_time)
    plt.xlabel("time [UTC]")
    plt.ylabel("CO2 [ppm]")
    plt.title("Preview of calibrated CO2 data")
    plt.legend(markerscale=8)
    plt.show()

    # --- EXPORT DATASET ---
    print("\n=== STEP 6: Export calibrated dataset ===")
    data = xr.Dataset({
        "CO2": calibrated_CO2,
        "p": p,
        "T": T,
        "rh": rh
    })

    header = (
        f"# Node {cfg['node_nr']} {cfg['location']} - calibrated timeseries. Sampling interval: {rs_int}",
        "# Calibration method: a0*CO2_raw + (a1*p + a2*T + asquared*T**2 + a3*rh + y)",
        f"# Resulting RMSE in calibration period: {acc} ppm"
    )
    data.attrs["readme"] = header

    # Filepaths
    
    if filename == None: 
        filename = "CO2_cal-rs{rs_int}"
    nc_path = base_path + f"unicorn{cfg['node_nr']}" + filename + ".cd"
    csv_path = base_path + f"unicorn{cfg['node_nr']}" + filename + ".csv"

    data.to_netcdf(nc_path)
    df_export = data.to_dataframe()
    df_export.to_csv(csv_path)

    # Insert header into CSV
    with open(csv_path, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("\n".join(header) + "\n" + content)

    print(f"\nCalibration saved as:\n- {nc_path}\n- {csv_path}\n")