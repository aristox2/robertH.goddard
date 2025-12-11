import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
def setup_plot():
    fig, axes = plt.subplots(6, 2, figsize=(12, 12))
    titles = ["aX", "aY", "aZ", "gX", "gY", "gZ"]
    lines = {}
    shaded_regions = {}

    for i, title in enumerate(titles):
        raw_ax = axes[i, 0]
        (raw_line,) = raw_ax.plot([], [], label=f"Raw {title}", color="blue", alpha=0.6)
        raw_ax.set_title(f"Raw {title}")
        raw_ax.legend()
        lines[f"{title}_raw"] = raw_line

        filt_ax = axes[i, 1]
        (filt_line,) = filt_ax.plot([], [], label=f"Filtered {title}", color="red", linewidth=2)
        (fc_line,) = filt_ax.plot([], [], label=f"Forecast {title}", color="green", linestyle="--")
        
        # Confidence Interval (Shaded Region)
        ci_fill = filt_ax.fill_between([], [], [], color="red", alpha=0.2)

        filt_ax.set_title(f"Filtered & Forecast {title}")
        filt_ax.legend()
        lines[f"{title}_filtered"] = filt_line
        lines[f"{title}_forecast"] = fc_line
        shaded_regions[title] = ci_fill

    plt.tight_layout()
    return fig, axes, lines, shaded_regions

def update_plot(data, ekf_covariances, lines, shaded_regions, axes):
    """
    Update the plot with new data and confidence intervals.
    
    data: Dict containing "raw", "filtered", and "forecast" values.
    ekf_covariances: Covariance matrix P from the EKF, used to compute confidence intervals.
    lines: Dictionary of line objects.
    shaded_regions: Dictionary of fill_between objects for confidence intervals.
    axes: Subplot axes array (6x2) from setup_plot().
    """
    titles = ["aX", "aY", "aZ", "gX", "gY", "gZ"]
    
    for i, title in enumerate(titles):
        raw_values = data[f"{title}_raw"]
        filtered_values = data[f"{title}_filtered"]
        forecast_values = data[f"{title}_forecast"]
        
        # Extract standard deviation from covariance matrix
        sigma = np.sqrt(ekf_covariances[i, i])  # Assuming diagonal entries correspond to measurement variances
        
        # Compute upper and lower bounds for confidence interval (±2σ for 95%)
        upper_bound = filtered_values + 2 * sigma
        lower_bound = filtered_values - 2 * sigma
        
        # Update plot lines
        lines[f"{title}_raw"].set_data(np.arange(len(raw_values)), raw_values)
        lines[f"{title}_filtered"].set_data(np.arange(len(filtered_values)), filtered_values)
        lines[f"{title}_forecast"].set_data(np.arange(len(forecast_values)), forecast_values)
        
        # Update confidence interval shaded region
        shaded_regions[title].remove()  # Remove old shaded region
        shaded_regions[title] = axes[i, 1].fill_between(
            np.arange(len(filtered_values)), lower_bound, upper_bound, color="red", alpha=0.2
        )

    return lines, shaded_regions
