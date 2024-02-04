import cv2
from keras.models import load_model
from jetson_tracking import JetbotTracker
from search_algorithm import JetbotSearch

# Initialize the face detection model and Jetbot controller
model = load_model('missing_children_model.h5')
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
tracker = JetbotTracker()
searcher = JetbotSearch()

cap = cv2.VideoCapture(0)  # Adjust the camera source as needed

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    frame_center = frame.shape[1] / 2

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            # For simplicity, focus on the first detected face
            face_center = x + w / 2
            tracker.track(face_center, frame_center)
            break  # If tracking one face, remove this line to track multiple faces
    else:
        searcher.search()

    # Display the resulting frame
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture and stop the robot
cap.release()
cv2.destroyAllWindows()
tracker.stop()
searcher.stop()
