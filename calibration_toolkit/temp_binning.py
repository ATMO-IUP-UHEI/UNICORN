import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import xarray as xr
import pandas as pd

def analyze_temperature_distribution(T, time=None, bins=60, show_stats=True, temp_range=(-20, 60)):
    """
    Analysiert und visualisiert die Temperaturverteilung im Datensatz.
    Erstellt Histogramm + Zeitreihe und berechnet statistische Kennwerte.

    Parameter
    ----------
    T : xarray.DataArray, np.ndarray oder pd.Series
        Temperaturdaten in °C.
    time : xarray.DataArray, np.ndarray oder pd.DatetimeIndex, optional
        Zeitstempel (nur für Zeitreihenplot erforderlich).
    bins : int
        Anzahl der Bins im Histogramm.
    show_stats : bool
        Gibt Kennwerte (Min, Max, Mittelwert) aus.
    temp_range : tuple(float, float)
        Temperaturbereich für Histogramm (x-Achsenbegrenzung).

    Rückgabe
    ----------
    dict :
        {"mean", "median", "std", "min", "max"}
    """

    # --- Daten vorbereiten ---
    if isinstance(T, xr.DataArray):
        temps = T.values
        if time is None and "time" in T.coords:
            time = T["time"].values
    elif isinstance(T, (pd.Series, pd.DataFrame)):
        temps = T.values.squeeze()
    else:
        temps = np.asarray(T)

    temps = temps[np.isfinite(temps)]  # NaNs entfernen

    # --- Zeit-Achse prüfen und ggf. konvertieren ---
    if time is not None:
        time = np.asarray(time)
        # Prüfen ob numerisch statt datetime
        if np.issubdtype(time.dtype, np.number):
            # Wenn Werte im Bereich Unix-Zeit liegen (≈ 1.6e9 → Sekunden)
            if np.nanmean(time) > 1e8 and np.nanmean(time) < 2e10:
                time = pd.to_datetime(time, unit='s')
            # Wenn Werte im Bereich Matplotlib-Zeit liegen (≈ 7e5 → Tage)
            elif np.nanmean(time) > 700000:
                time = dates.num2date(time)
            else:
                print(" Unbekanntes Zeitformat – Zeitplot wird übersprungen.")
                time = None

    # --- Statistische Analyse ---
    stats = {
        "mean": np.nanmean(temps),
        "median": np.nanmedian(temps),
        "std": np.nanstd(temps),
        "min": np.nanmin(temps),
        "max": np.nanmax(temps)
    }

    if show_stats:
        print("Temperaturstatistik:")
        print(f"  Mittelwert : {stats['mean']:.2f} °C")
        print(f"  Median     : {stats['median']:.2f} °C")
        print(f"  Standardabw: {stats['std']:.2f} °C")
        print(f"  Minimum    : {stats['min']:.2f} °C")
        print(f"  Maximum    : {stats['max']:.2f} °C")

    # --- Plot 1: Histogramm ---
    plt.figure(figsize=(8, 5))
    try:
        import seaborn as sns
        if hasattr(sns, "histplot"):
            sns.histplot(temps, bins=bins, kde=True, color="steelblue")
        else:
            sns.distplot(temps, bins=bins, kde=True, color="steelblue")
    except Exception:
        plt.hist(temps, bins=bins, range=temp_range, color="steelblue", alpha=0.7)
    plt.title("Temperaturverteilung")
    plt.xlabel("Temperatur [°C]")
    plt.ylabel("Anzahl Messpunkte")
    plt.xlim(temp_range)
    plt.grid(alpha=0.3)
    plt.tight_layout()

    # --- Plot 2: Zeitlicher Verlauf (optional) ---
    if time is not None:
        plt.figure(figsize=(10, 4))
        plt.plot(time, temps, lw=0.5, color="tab:red")
        plt.title("Zeitlicher Verlauf der Temperatur")
        plt.ylabel("Temperatur [°C]")
        plt.xlabel("Zeit")
        plt.grid(alpha=0.3)
        plt.gca().xaxis.set_major_formatter(dates.DateFormatter("%Y-%m-%d"))
        plt.gcf().autofmt_xdate()
        plt.tight_layout()

    plt.show()

    return stats




def apply_temperature_binning(gas_ref, gas_raw, p, T, rh,  n_bins=10, temp_range=(-10, 50)):
    """
    Führt ein Temperatur-Binning durch, um alle Temperaturbereiche gleichmäßig zu repräsentieren.

    Vorgehen:
    ----------
    1. Temperatur in gleich große Bins einteilen.
    2. Aus jedem Bin eine gleiche Anzahl von Stichproben auswählen.
    3. Rückgabe: gebalancte Daten mit erhaltener Zeitachse.

    Parameter
    ----------
    gas_raw, p, T, rh, gas_ref : xarray.DataArray
        Kalibrationsdaten mit Zeitkoordinate.
    n_bins : int
        Anzahl gleichbreiter Temperatur-Bins.
    temp_range : tuple(float, float)
        Temperaturbereich in °C.

    Rückgabe
    ----------
    tuple : (gas_raw_sel, p_sel, T_sel, rh_sel, gas_ref_sel, time_sel)
        Gebalancte Arrays mit gleicher Temperaturverteilung und Zeitkoordinate.
    """

    # In DataFrame konvertieren
    df = pd.DataFrame({
        "gas_raw": gas_raw.values,
        "p": p.values,
        "T": T.values,
        "rh": rh.values,
        "gas_ref": gas_ref.values,
        "time": gas_raw["time"].values
    })

    # Temperatur-Binning
    df["T_bin"] = pd.cut(df["T"], bins=np.linspace(*temp_range, n_bins + 1))

    # Anzahl der kleinsten Bin-Gruppe
    counts = df["T_bin"].value_counts()
    n_per_bin = counts.min()

    # Falls ein Bin leer ist → Debug-Ausgabe
    if n_per_bin == 0:
        print("⚠️ Leere Temperatur-Bins gefunden!")
        print("➡️ Counts pro Temperatur-Bin:")
        print(counts.sort_index())

        print(" Alle verwendeten Temperaturwerte:")
        print(df["T"].describe())        # Überblick
        print(df["T"].values)            # vollständige Liste

        raise ValueError("Ein oder mehrere Temperaturbereiche enthalten keine Datenpunkte.")
    
    # Gleichmäßiges Sampling pro Bin
    df_balanced = (
        df.groupby("T_bin", group_keys=False)
          .apply(lambda x: x.sample(n=min(len(x), n_per_bin), random_state=42))
          .sort_values("time")
          .reset_index(drop=True)
    )

    # Rückgabe mit Zeit-Koordinate
    time_sel = pd.to_datetime(df_balanced["time"].values)

    def make_da(data):
        return xr.DataArray(data, coords=[time_sel], dims=["time"])

    return (
        make_da(df_balanced["gas_ref"].values),
        make_da(df_balanced["gas_raw"].values),
        make_da(df_balanced["p"].values),
        make_da(df_balanced["T"].values),
        make_da(df_balanced["rh"].values),
        make_da(df_balanced["time"].values)
    )
