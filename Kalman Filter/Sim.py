import numpy as np
import pygame
import random

class KalmanFilter:
    def __init__(self):
        self.state = np.zeros(4, dtype=np.float64)
        self.P = np.eye(4, dtype=np.float64) * 1000
        self.dt = 0.1
        
        self.F = np.array([
            [1, 0, self.dt, 0],
            [0, 1, 0, self.dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float64)
        
        self.Q = np.eye(4, dtype=np.float64) * 0.1
        self.H_camera = np.array([[1, 0, 0, 0],
                                 [0, 1, 0, 0]], dtype=np.float64)
        self.H_radar = np.array([[1, 0, 0, 0],
                                [0, 1, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]], dtype=np.float64)
        self.R_camera = np.eye(2, dtype=np.float64) * 5
        self.R_radar = np.eye(4, dtype=np.float64) * 2

    def predict(self):
        self.state = self.F @ self.state
        self.P = self.F @ self.P @ self.F.T + self.Q
        return self.state

    def update_camera(self, measurement):
        return self._update(measurement, self.H_camera, self.R_camera)

    def update_radar(self, measurement):
        return self._update(measurement, self.H_radar, self.R_radar)

    def _update(self, measurement, H, R):
        y = measurement - H @ self.state
        S = H @ self.P @ H.T + R
        K = self.P @ H.T @ np.linalg.inv(S)
        self.state = self.state + K @ y
        self.P = (np.eye(len(self.state)) - K @ H) @ self.P
        return self.state

class Simulator:
    def __init__(self):
        pygame.init()
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Kalman Filter Prediction Demo")
        
        self.kf = KalmanFilter()
        # Reduced initial velocities
        self.true_state = np.array([400.0, 300.0, 15.0, 10.0], dtype=np.float64)
        
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
        self.clock = pygame.time.Clock()
        self.object_visible = True
        self.visibility_timer = 0
        self.prediction_path = []

    def add_noise(self, value, std):
        return value + np.random.normal(0, std, value.shape)

    def get_measurements(self):
        if not self.object_visible:
            return None, None
        
        camera_pos = self.add_noise(self.true_state[:2], 15)
        radar_measurement = self.add_noise(self.true_state, 5)
        return camera_pos, radar_measurement

    def draw_circle(self, color, position, radius):
        pygame.draw.circle(self.screen, color, 
                         position.astype(np.int32), radius)

    def draw_line(self, color, start_pos, end_pos, width):
        pygame.draw.line(self.screen, color,
                        start_pos.astype(np.int32), 
                        end_pos.astype(np.int32), width)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update visibility
            self.visibility_timer += 1
            if self.visibility_timer >= 100:  # Toggle visibility every ~3 seconds
                self.object_visible = not self.object_visible
                self.visibility_timer = 0
                if not self.object_visible:
                    self.prediction_path = []  # Clear prediction path when object disappears

            # Update true state with slower velocities
            self.true_state[:2] += self.true_state[2:] * self.kf.dt
            self.true_state[2:] += np.random.normal(0, 0.1, 2)  # Reduced noise

            # Bounce off walls
            for i in range(2):
                if self.true_state[i] < 0 or self.true_state[i] > (self.width if i == 0 else self.height):
                    self.true_state[i+2] *= -1

            # Get measurements only when object is visible
            camera_pos, radar_measurement = self.get_measurements()

            # Kalman filter prediction
            predicted_state = self.kf.predict()
            
            # Update only when measurements are available
            if self.object_visible:
                if random.random() < 0.7:
                    self.kf.update_camera(camera_pos)
                if random.random() < 0.5:
                    self.kf.update_radar(radar_measurement)
                self.prediction_path = []  # Clear predictions when visible
            else:
                # Store prediction path when object is invisible
                self.prediction_path.append(predicted_state[:2].copy())
                if len(self.prediction_path) > 30:  # Keep last 30 predictions
                    self.prediction_path.pop(0)

            # Drawing
            self.screen.fill((0, 0, 0))
            
            # Draw prediction path when object is invisible
            if not self.object_visible:
                for i in range(1, len(self.prediction_path)):
                    self.draw_line(self.YELLOW, 
                                 self.prediction_path[i-1], 
                                 self.prediction_path[i], 1)

            # Draw true position and measurements only when visible
            if self.object_visible:
                self.draw_circle(self.WHITE, self.true_state[:2], 10)
                if camera_pos is not None:
                    self.draw_circle(self.RED, camera_pos, 5)
                if radar_measurement is not None:
                    self.draw_circle(self.GREEN, radar_measurement[:2], 5)

            # Always draw Kalman filter estimate
            self.draw_circle(self.BLUE, self.kf.state[:2], 8)
            
            # Draw velocity vectors
            if self.object_visible:
                end_pos = self.true_state[:2] + self.true_state[2:] * 2
                self.draw_line(self.WHITE, self.true_state[:2], end_pos, 2)
            
            end_pos = self.kf.state[:2] + self.kf.state[2:] * 2
            self.draw_line(self.BLUE, self.kf.state[:2], end_pos, 2)

            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

if __name__ == "__main__":
    sim = Simulator()
    sim.run()