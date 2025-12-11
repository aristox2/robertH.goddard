import numpy as np

class EKF:
    def __init__(self, dt, state_dim, measure_dim, process_noise, measure_noise):
        self.dt = dt
        self.state_dim = state_dim
        self.measure_dim = measure_dim
        self.x = np.zeros((state_dim, 1))
        self.P = np.eye(state_dim)
        self.Q = process_noise * np.eye(state_dim)
        self.R = measure_noise * np.eye(measure_dim)
        self.I = np.eye(state_dim)
    
    def state_transition(self, x):
        return np.eye(self.state_dim) @ x

    def jacobian_state_transition(self, x):
        return np.eye(self.state_dim)

    def measurement_function(self, x):
        return np.eye(self.measure_dim, self.state_dim) @ x

    def jacobian_measurement_function(self, x):
        return np.eye(self.measure_dim, self.state_dim)

    def predict(self):
        F = self.jacobian_state_transition(self.x)
        self.x = self.state_transition(self.x)
        self.P = F @ self.P @ F.T + self.Q
        return self.x.copy()

    def update(self, z):
        H = self.jacobian_measurement_function(self.x)
        z = np.reshape(z, (self.measure_dim, 1))
        y = z - H @ self.x  
        innovation_norm = np.linalg.norm(y)
        threshold = .5
        if innovation_norm > threshold:
            self.R *= 1.05  
        else:
            self.R *= 0.99  
        S = H @ self.P @ H.T + self.R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (self.I - K @ H) @ self.P
        return self.x.copy()

    def forecast(self, steps=10):
        temp_x = self.x.copy()
        forecast_states = []
        for _ in range(steps):
            temp_x = self.state_transition(temp_x)
            forecast_states.append(temp_x.copy())
        return forecast_states
