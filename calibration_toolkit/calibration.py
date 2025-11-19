import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
from scipy.optimize import curve_fit


def select_fit_range(vars, gas_ref, cfg):
    """
    Bestimmt den Start- und Endindex für den Fitbereich anhand der im cfg angegebenen Zeiten
    und gibt die zugeschnittenen Daten zurück.

    Parameter
    ----------
    vars : tuple
        Enthält (gas_raw, p, T, rh, time), jeweils als xarray.DataArray oder numpy-Array.
    gas_ref : xarray.DataArray oder np.ndarray
        Referenz-Gasdaten zur Kalibration (z. B. CO2_ref oder CH4_ref).
    cfg : dict
        Konfigurationsdictionary mit Schlüsseln:
            - "start_time_fit"
            - "end_time_fit"

    Rückgabe
    --------
    vars_fit : tuple
        Gleicher Aufbau wie `vars`, aber nur innerhalb des Fitbereichs.
    gas_ref_fit : np.ndarray
        Referenzdaten im Fitbereich.
    start_ind, end_ind : int
        Indizes des Fitbereichs.
    """

    gas_raw, p, T, rh, time = vars

    # --- Zeit in numerisches Format konvertieren ---
    t_raw = dates.date2num(gas_raw["time"])
    t_start = dates.date2num(cfg["start_time_fit"])
    t_end = dates.date2num(cfg["end_time_fit"])

    # --- Indexbereich bestimmen ---
    start_ind = np.argmin(np.abs(t_raw - t_start))
    end_ind = np.argmin(np.abs(t_raw - t_end))

    # --- Fitbereich zuschneiden ---
    vars_fit = (
        gas_raw[start_ind:end_ind],
        p[start_ind:end_ind],
        T[start_ind:end_ind],
        rh[start_ind:end_ind],
        time[start_ind:end_ind],
    )

    gas_ref_fit = gas_ref[start_ind:end_ind]

    return vars_fit, gas_ref_fit, start_ind, end_ind

#Heidelberg Fitting Method


def fit_multi_lin2(vars, *params):
    a0, a1, a2, asquared, a3, drift, y = params
    CO2_raw, p, T, rh, time = vars
    return a0 * CO2_raw + (a1 * p + a2 * T + asquared*T**2 + a3 * rh + y)
    #return a0 * CO2_raw + (a1 * p + a2 * T + asquared*T**2 + a3 * rh + drift*(time-time[0]) y)


def dry_co2_values(CO2, T_dew, T, P):
    """Apply dry air and STP correction."""
    P_H2O = 6.1094 * np.exp(17.625 * T_dew / (243.04 + T_dew))
    return CO2 * 1013.25 / P * (T + 273.15) / 298.15 * 1 / (1 - (P_H2O / P))


def heidelberg_fitting_method(vars, CO2_ref, cfg):
    """
    Führt die eigentliche Kalibration durch (Heidelberg-Methode).

    Erwartet, dass der Fitbereich bereits durch `select_fit_range` bestimmt wurde.
    """
    print("Performing Heidelberg fit...")

    # --- Fit durchführen ---
    params, covariance = curve_fit(
        fit_multi_lin2,
        vars,
        CO2_ref,
        p0=[1, 0.1, 1, 0.1, 0.1, 0.0001, 50],
        bounds=([-2, -2, -40, -2, -2, -0.06, -400],
                [2, 2, 40, 2, 2, 0.06, 400])
    )

    errors = np.sqrt(np.diag(covariance))
    print("Fit erfolgreich abgeschlossen.")
    return params, errors, covariance




#Analysefunktion
def analyze_calibration_results(vars, gas_ref, params, errors, covariance, cfg, fit_func, names=None):
    """
    Führt Analyse und Visualisierung der Kalibration durch (generisch für beliebiges Gas).
    """
    gas_name = cfg["gas"]  # z.B. "CO2", "CH4", ...
    
    gas_raw = vars[0]

    # --- Fitbereich bestimmen ---
    start_ind = np.argmin(np.abs(
        dates.date2num(cfg["start_time_fit"]) - dates.date2num(gas_raw['time'])
    ))
    end_ind = np.argmin(np.abs(
        dates.date2num(cfg["end_time_fit"]) - dates.date2num(gas_raw['time'])
    ))

    # --- Modellvorhersage ---
    predicted = fit_func(vars, *params)

    # --- Residuen & R² ---
    residuals_fit = gas_ref[start_ind:end_ind] - predicted[start_ind:end_ind]
    ss_res = np.sum(residuals_fit ** 2)
    ss_tot = np.sum((gas_ref[start_ind:end_ind] - np.mean(gas_ref[start_ind:end_ind])) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    residuals = gas_ref - predicted


    # --- Parameterprint ---
    if names is None:
        # Standard: a0, a1, a2, ...
        names = [f"a{i}" for i in range(len(params))]
    
    if len(names) != len(params):
        raise ValueError("names und params müssen gleich lang sein!")

    print(f"Node {cfg['node_nr']} - Fitted Parameters:")
    for name, val, err in zip(names, params, errors):
        print(f"{name} = {val:.4f} ± {err:.4f}")
    print(f"$R^2$ = {float(r_squared):.4f}")
    print("Covariance matrix:\n", covariance)

    # --- Residualplot ---
    plt.figure(figsize=(8, 5))
    plt.scatter(predicted, residuals, alpha=0.6,
                c=dates.date2num(predicted['time']), cmap='plasma')
    plt.axhline(0, color='red', linestyle='--', linewidth=1)
    plt.xlabel(f'{gas_name}_calib [{cfg.get("units", gas_name)}]')
    plt.ylabel(f'residuals ({gas_name}_ref - {gas_name}_calib)')
    plt.title(f'residual plot - node {cfg["node_nr"]}')
    plt.grid()

    cbar = plt.colorbar()
    tick_locs = cbar.get_ticks()
    tick_labels = [dates.num2date(t).strftime('%Y-%m-%d') for t in tick_locs]
    cbar.set_ticks(tick_locs)
    cbar.set_ticklabels(tick_labels)
    cbar.set_label('Date')

    # --- Timeseries comparison ---
    plt.figure(figsize=(8,5))
    plt.plot(predicted['time'], predicted, label='calibrated data', linewidth=.3)
    plt.plot(predicted['time'], gas_ref, label='reference', linewidth=.3)
    plt.title(f'timeseries comparison - node {cfg["node_nr"]}')
    plt.ylabel(f'{gas_name} [{cfg.get("units", gas_name)}]')
    plt.xlabel('time [UTC]')

    plt.xticks(
        np.arange(cfg["start_time_fit"],
                  cfg["end_time_fit"],
                  15*24*60*60*10**6)
    )

    leg = plt.legend()
    for legobj in leg.legendHandles:
        legobj.set_linewidth(1.0)

    # --- Histogramm der Residuen ---
    mins = len(residuals)
    plt.figure(figsize=(8,5))
    hist = plt.hist(residuals, bins=100, range=(-20,20),
                    color='grey', label='full time span')

    hist1 = plt.hist(residuals[:int(mins/3)], bins=100, range=(-20,20),
                     color='blue', alpha=.6,
                     label='early period')

    hist2 = plt.hist(residuals[int(mins/3):int(2*mins/3)],
                     bins=100, range=(-20,20),
                     color='red', alpha=.6,
                     label='middle period')

    hist3 = plt.hist(residuals[int(2*mins/3):], bins=100, range=(-20,20),
                     color='yellow', alpha=.6,
                     label='late period')

    plt.xlim(-20,20)
    plt.title(f'accuracy - calibration of node {cfg["node_nr"]}')
    plt.xlabel(f'{gas_name}_ref - {gas_name}_calib')
    plt.ylabel('counts')
    plt.legend(loc='upper left')

    # --- Fit der Genauigkeit ---
    hist = np.histogram(residuals_fit, bins=100, range=(-20,20))
    yg = hist[0]
    x = hist[1][1:]

    hist_full = np.histogram(residuals, bins=100, range=(-20,20))
    y_full = hist_full[0]
    x_full = hist_full[1][1:]

    def gaussian(x, A, mu, sig):
        return A * np.exp(-0.5 * ((x - mu) / sig)**2)

    poptg, _ = curve_fit(gaussian, x, yg)
    poptg1, _ = curve_fit(gaussian, x_full, y_full)

    plt.plot(x, gaussian(x, *poptg))
    plt.plot(x_full, gaussian(x_full, *poptg1))

    plt.text(.99,.99, r'$\sigma_{acc}$='+str(np.abs(np.round(poptg[2], 2)))+' ppm', ha='right', va='top', size=18, transform=plt.gca().transAxes)
    plt.text(.99,.9, r'$\mu_{calib}$='+str(np.round(poptg[1],2))+' ppm', size=18, ha='right', va='top', transform=plt.gca().transAxes)


    acc = abs(round(poptg[2], 2))
    print(f'resolution: σ = {acc}')

    plt.show()
    return acc
