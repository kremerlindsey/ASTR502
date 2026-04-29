# reading in data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from astropy.timeseries import LombScargle
from astropy.stats import SigmaClip
from astropy.stats import sigma_clip
from scipy.stats import median_abs_deviation

#--------------------------------------------------------# ChatGPT helped me read in data from every file in a folder
import os

def read_files_from_folder(folder_path):
    
    data = []
    names = []
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if not filename.endswith(".fits"):               # this shouldn't matter because they're all fits files, but I don't know. Just in case
            continue                                       
        
        with fits.open(file_path) as hdul:
            lc_data = hdul[1].data 
            data.append(lc_data)
        
        name = filename[25:34]                           # indexes the file name for just the light curve number so I can use this as ID later
        names.append(name)
        
    return data, names
#--------------------------------------------------------#
    
data, names = read_files_from_folder("/Users/lindseykremer/all k2 ssf light curves - ASTR502") # added by me -> 18 items in this folder (from Dropbox with Ian)

def _bin_series_fixed_width(x, y, width):
    if not np.isfinite(width) or width <= 0:
        return np.array([]), np.array([])
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    mask = np.isfinite(x_arr) & np.isfinite(y_arr)
    if not mask.any():
        return np.array([]), np.array([])
    x_valid = x_arr[mask]
    y_valid = y_arr[mask]
    x_min = np.nanmin(x_valid)
    x_max = np.nanmax(x_valid)
    if not np.isfinite(x_min) or not np.isfinite(x_max):
        return np.array([]), np.array([])
    if x_min == x_max:
        edges = np.array([x_min, x_min + width])
    else:
        edges = np.arange(x_min, x_max + width, width)
        if edges.size < 2:
            edges = np.array([x_min, x_max])
    return _bin_series_by_edges(x_valid, y_valid, edges)

def _bin_series_by_edges(x, y, edges):
    x_arr = np.asarray(x, dtype=float)
    y_arr = np.asarray(y, dtype=float)
    mask = np.isfinite(x_arr) & np.isfinite(y_arr)
    if not mask.any():
        return np.array([]), np.array([])
    x_valid = x_arr[mask]
    y_valid = y_arr[mask]
    inds = np.digitize(x_valid, edges) - 1
    valid = (inds >= 0) & (inds < len(edges) - 1)
    if not valid.any():
        return np.array([]), np.array([])
    x_valid = x_valid[valid]
    y_valid = y_valid[valid]
    inds = inds[valid]
    centers = []
    values = []
    for idx in np.unique(inds):
        bin_mask = inds == idx
        if np.any(bin_mask):
            centers.append(0.5 * (edges[idx] + edges[idx + 1]))
            values.append(np.nanmean(y_valid[bin_mask]))
    return np.array(centers), np.array(values)

star_periods = []                                                                   # lists for holding periods and powers that need to be indexed
star_powers = []

for i, column in enumerate(data):                                                   # edited by me
    
    lc = data[i]
    
    name = names[i]                                                                 # added by me
    
    # lomb scargle section for obtaining star period and power -> added by me

    time = data[i]["T"]
    flux = data[i]["FCOR"]
    normflux = flux / np.nanmedian(flux)
    frequency, power = LombScargle(time, normflux, center_data = True).autopower(minimum_frequency = (1/40), maximum_frequency = 1/0.2)
        
    ## subsection for long term detrending
    
    finite = np.isfinite(time) & np.isfinite(flux)           # start with a finite mask
    t0 = time[finite]
    f0 = flux[finite]
    
    sigclip = SigmaClip(sigma = 2, maxiters = None, cenfunc = 'median', stdfunc = 'mad_std') # could also use median
    
    clipped = sigclip(f0)                                    # returns a masked array telling you what got clipped
    
    good = ~clipped.mask                                     # is true where not clipped
    
    time_clean = t0[good]
    flux_clean = f0[good]
    p = np.polyfit(time_clean, flux_clean, deg = 3) # third order polynomial
    
    fit_flux = np.polyval(p, time_clean)
    reduced_flux = flux_clean / fit_flux
    time = time_clean
    flux = reduced_flux
    
    ## end of subsection
    
    max_power_index = np.argmax(power)                      # finding star period
    max_frequency = frequency[max_power_index]
    star_period = 1 / max_frequency
    star_periods.append(star_period)
        
    star_power = np.max(power)                              # finding star power
    star_powers.append(star_power)

    # end of Lomb Scargle section
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8), constrained_layout=True)
    ax_time = axes[0, 0]
    ax_phase = axes[0, 1]
    ax_two_phase = axes[1, 0]
    #ax_zoom = axes[1, 1]

    amp = np.nanstd(normflux)                               # added by me 
    
    fig.suptitle(
        f"EPIC {name}, P={star_period:.2f}, 2xP={2*star_period:.2f},Φ={star_power:.3f}, A={amp * 100:.2f}%",
        fontsize=14,
    )
    
    def _get_flux_ylim(best_amp_val, flux_vals):
        if np.isfinite(best_amp_val) and best_amp_val > 0:
            return (1 - 5 * best_amp_val, 1 + 5 * best_amp_val)
        finite_flux = flux_vals[np.isfinite(flux_vals)]
        if finite_flux.size:
            f_med = np.nanmedian(finite_flux)
            f_std = np.nanstd(finite_flux)
            if not np.isfinite(f_std) or f_std == 0:
                f_std = 0.1 * abs(f_med) if f_med else 1.0
            return (f_med - 5 * f_std, f_med + 5 * f_std)
        return None
    
    #### top left 
    
    ax_time.scatter(time, flux, s=2, color="0.7", alpha=0.4, edgecolor="none", linewidths=0)
    bin_width_days = 4.0 / 24.0
    binned_time, binned_flux = _bin_series_fixed_width(time, flux, bin_width_days)
    if binned_time.size:
        ax_time.scatter(
            binned_time,
            binned_flux,
            s=16,
            color="k",
            alpha=0.9,
            edgecolor="none",
            linewidths=0,
        )
    ax_time.set_xlabel("time [days]", fontsize = 14)
    ax_time.set_ylabel("corrected flux", fontsize = 14)
    ax_time.set_title(f"EPIC {name} corrected flux vs time", fontsize = 14)
    ax_time.grid(True, which="both", ls=":", lw=0.4, alpha=0.5)
    ylims_time = _get_flux_ylim(amp, flux)
    ax_time.set_ylim(ylims_time)
    
    #### top right
    
    period = star_period
    ylims_phase = _get_flux_ylim(amp, flux)
    if np.isfinite(period) and period > 0:
        time0 = np.nanmin(time)
        phase = np.mod(time - time0, period) / period
        ax_phase.scatter(phase, flux, s=2, color="0.7", alpha=0.4, edgecolor="none", linewidths=0)
        phase_edges = np.linspace(0, 1, 101)
        binned_phase, binned_phase_flux = _bin_series_by_edges(phase, flux, phase_edges)
        if binned_phase.size:
            ax_phase.scatter(
                binned_phase,
                binned_phase_flux,
                s=16,
                color="k",
                alpha=0.9,
                edgecolor="none",
                linewidths=0,
            )
        ax_phase.set_xlim(0, 1)
        ax_phase.text(
            0.98,
            0.95,
            f"P={period:.2f}",
            transform=ax_phase.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color="k",
        )
        if ylims_phase:
            ax_phase.set_ylim(ylims_phase)
        if ylims_time:
            y_line = ylims_time[1] - 0.05 * (ylims_time[1] - ylims_time[0])
        else:
            y_line = ax_time.get_ylim()[1]
        x_start = np.nanmin(time)
        x_end = x_start + period
        ax_time.hlines(y_line, x_start, x_end, colors="crimson", linewidth=2, zorder=5)
    else:
        ax_phase.text(
            0.5,
            0.5,
            "No valid first_period",
            ha="center",
            va="center",
            transform=ax_phase.transAxes,
        )
        if ylims_phase:
            ax_phase.set_ylim(ylims_phase)
    ax_phase.set_xlabel("phase", fontsize = 14)
    ax_phase.set_ylabel("flux", fontsize = 14)
    ax_phase.set_title(f"EPIC {name} flux vs phase", fontsize = 14)
    ax_phase.grid(True, which="both", ls=":", lw=0.4, alpha=0.5)
    
    ##### bottom left 
    
    period = 0.5*star_period
    ylims_phase = _get_flux_ylim(amp, flux)
    if np.isfinite(period) and period > 0:
        time0 = np.nanmin(time)
        phase = np.mod(time - time0, period) / period
        ax_two_phase.scatter(phase, flux, s=2, color="0.7", alpha=0.4, edgecolor="none", linewidths=0)
        phase_edges = np.linspace(0, 1, 101)
        binned_phase, binned_phase_flux = _bin_series_by_edges(phase, flux, phase_edges)
        if binned_phase.size:
            ax_two_phase.scatter(
                binned_phase,
                binned_phase_flux,
                s=16,
                color="k",
                alpha=0.9,
                edgecolor="none",
                linewidths=0,
            )
        ax_two_phase.set_xlim(0, 1)
        ax_two_phase.text(
            0.98,
            0.95,
            f"P={period:.2f}",
            transform=ax_two_phase.transAxes,
            ha="right",
            va="top",
            fontsize=9,
            color="k",
        )
        if ylims_phase:
            ax_two_phase.set_ylim(ylims_phase)
        if ylims_time:
            y_line = ylims_time[1] - 0.05 * (ylims_time[1] - ylims_time[0])
        else:
            y_line = ax_time.get_ylim()[1]

        x_start = np.nanmin(time)
        x_end = x_start + period
        ax_time.hlines(y_line, x_start, x_end, colors="cyan", linewidth=2, zorder=10)
        #ax_time.hlines(y_line, x_start, x_end, colors="", linewidth=2)
    else:
        ax_two_phase.text(
            0.5,
            0.5,
            "No valid first_period",
            ha="center",
            va="center",
            transform=ax_two_phase.transAxes,
        )
        if ylims_phase:
            ax_two_phase.set_ylim(ylims_phase)
    ax_two_phase.set_xlabel("phase", fontsize = 14)
    ax_two_phase.set_ylabel("flux", fontsize = 14)
    ax_two_phase.set_title(f"EPIC {name} 2x(flux vs phase)", fontsize = 14)
    ax_two_phase.grid(True, which="both", ls=":", lw=0.4, alpha=0.5)
    
    #### LS periodogram on bottom right
    
    plt.plot(1/frequency, power)                            
    plt.title(f"Lomb Scargle Periodogram for {names[i]}") 
    plt.xlabel("period (days)", fontsize = 14)                               
    plt.ylabel("power", fontsize = 14)
    plt.show()

    x_end = np.nanmax(time[0] + 1)
    x_start = x_end - 2*star_period
    #ax_zoom.hlines(y_line, x_start, x_end, colors="cyan", linewidth=2)     # leftover from old bottom right

    x_start = np.nanmax(time[0])
    x_end = x_start + star_period
    #ax_zoom.hlines(y_line, x_start, x_end, colors="crimson", linewidth=2)  # leftover from old bottom right
    
    fig.savefig(f"light_curve_{name}.png")
    
    #plt.close()
    
savethis = { 
    'Light Curve' : names,
    'Star Period' : star_periods,
    'Star Power' : star_powers
    }

df = pd.DataFrame(savethis)       # turn into a data frame

file_name = 'Kremer_K2data.xlsx'  # choose a file name

df.to_excel(file_name, sheet_name = 'Kremer_K2data', index = False)

