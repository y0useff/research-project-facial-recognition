import time
from jetbot import Robot

class JetbotTracker:
    def __init__(self):
        self.robot = Robot()
        self.tracking_speed = 0.3  # Adjust as necessary

    def track(self, face_x, frame_width):
        """
        Adjust the robot's movement based on the position of the detected face.
        :param face_x: The x-coordinate of the detected face's center.
        :param frame_width: The width of the frame from the camera feed.
        """
        center = frame_width / 2
        error = face_x - center

        # Adjust these values as necessary for your specific robot
        k_p = 0.1  # Proportional gain
        adjustment = k_p * error

        # Set motor speeds
        left_speed = max(min(self.tracking_speed + adjustment, 1), 0)
        right_speed = max(min(self.tracking_speed - adjustment, 1), 0)

        self.robot.set_motors(left_speed, right_speed)
        time.sleep(0.1)

    def stop(self):
        self.robot.stop()
