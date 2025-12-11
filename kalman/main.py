import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from src.ekf import EKF
from src.data_load import load_sensor_data
from src.visualize import setup_plot
import os

# Load dataset
file_path = os.path.join("data", "clleaned.csv")
df = load_sensor_data(file_path)

# Extract sensor data
ax_data = df['aX'].values
ay_data = df['aY'].values
az_data = df['aZ'].values
gx_data = df['gX'].values
gy_data = df['gY'].values
gz_data = df['gZ'].values

# Initialize EKF
dt = 1.0
state_dim = 6  
measure_dim = 6
process_noise = 0.1
measure_noise = 0.5
ekf = EKF(dt, state_dim, measure_dim, process_noise, measure_noise)

# Data storage
filtered_data = {key: [] for key in ["aX", "aY", "aZ", "gX", "gY", "gZ"]}
forecast_data = {key: [] for key in ["aX", "aY", "aZ", "gX", "gY", "gZ"]}

# Setup plots
frames = len(ax_data)
fig, axes, lines, shaded_regions = setup_plot()

def update_plot(frame):
    measurement = np.array([ax_data[frame], ay_data[frame], az_data[frame],
                            gx_data[frame], gy_data[frame], gz_data[frame]])

    ekf.predict()
    forecast_states = ekf.forecast(steps=10)
    forecast_array = np.hstack(forecast_states)  

    filtered_state = ekf.update(measurement)

    for key, idx in zip(["aX", "aY", "aZ", "gX", "gY", "gZ"], range(6)):
        filtered_data[key].append(filtered_state[idx, 0])
        forecast_data[key] = forecast_array[idx, :].tolist()

    for key in ["aX", "aY", "aZ", "gX", "gY", "gZ"]:
        lines[f"{key}_raw"].set_data(range(len(filtered_data[key])), filtered_data[key])
        lines[f"{key}_filtered"].set_data(range(len(filtered_data[key])), filtered_data[key])
        forecast_x = np.arange(len(filtered_data[key]), len(filtered_data[key]) + len(forecast_data[key]))
        lines[f"{key}_forecast"].set_data(forecast_x, forecast_data[key])

    for row in axes:
        for ax in row:
            ax.relim()
            ax.autoscale_view()
    
    return list(lines.values())

ani = animation.FuncAnimation(fig, update_plot, frames=frames, interval=50, blit=False)

gif_filename = os.path.join("output", "sensorDataEKF_proactive.gif")
ani.save(gif_filename, writer="pillow", fps=30)

print(f"Proactive Filtration Simulation saved as {gif_filename}")
plt.show()
