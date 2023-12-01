import cv2
import Jetson.GPIO as GPIO
from sound import play_sound  # Import the play_sound function

# Motor control pins on Jetson Nano
left_motor_pin = 18
right_motor_pin = 16

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(left_motor_pin, GPIO.OUT)
GPIO.setup(right_motor_pin, GPIO.OUT)

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load the provided image
provided_image_path = 'path/to/provided/image.jpg'  # Replace with the actual path to the provided image
provided_image = cv2.imread(provided_image_path)

# Function to control the robot based on face position
def control_robot(face_x, frame_width):
    center_x = frame_width // 2
    threshold = 50  # Adjust this threshold based on your preference

    if face_x < center_x - threshold:
        # Face is on the left, turn left
        GPIO.output(left_motor_pin, GPIO.HIGH)
        GPIO.output(right_motor_pin, GPIO.LOW)
    elif face_x > center_x + threshold:
        # Face is on the right, turn right
        GPIO.output(left_motor_pin, GPIO.LOW)
        GPIO.output(right_motor_pin, GPIO.HIGH)
    else:
        # Face is in the center, move forward
        GPIO.output(left_motor_pin, GPIO.HIGH)
        GPIO.output(right_motor_pin, GPIO.HIGH)

# Perform face detection on the provided image
gray_provided_image = cv2.cvtColor(provided_image, cv2.COLOR_BGR2GRAY)
faces_in_provided_image = face_cascade.detectMultiScale(
    gray_provided_image,
    scaleFactor=1.3,
    minNeighbors=5,
    minSize=(30, 30),
    maxSize=(600, 600)
)

# Process each detected face in the provided image
for (x, y, w, h) in faces_in_provided_image:
    # Draw rectangle around the face
    cv2.rectangle(provided_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Control the robot based on the face position
    control_robot(x + w // 2, provided_image.shape[1])

    # Play sound when a person is detected
    play_sound()

# Display the resulting image with detected faces
cv2.imshow('Detected Faces in Provided Image', provided_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Release GPIO resources
GPIO.cleanup()
