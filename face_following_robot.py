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

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set the camera resolution
cap.set(3, 640)  # Width
cap.set(4, 480)  # Height

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

# Main loop
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(30, 30),  # Adjust this based on the desired minimum face size
        maxSize=(600, 600)  # Adjust this based on the desired maximum face size
    )

    # Process each detected face
    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Control the robot based on the face position
        control_robot(x + w // 2, frame.shape[1])

        # Play sound when a person is detected
        play_sound()

    # Display the resulting frame
    cv2.imshow('Face Following Robot', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
