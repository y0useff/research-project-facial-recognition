import cv2
from time import sleep
from deepface import DeepFace
key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
sleep(2)
while True:

    try:
        check, frame = webcam.read()
        print(check)
        print(frame) 
        cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)
        if key == ord('s'):
            cv2.imwrite(filename='saved_img.jpg', img=frame)
            webcam.release()
            print("Processing image...")
            img_ = cv2.imread('saved_img.jpg', cv2.IMREAD_ANYCOLOR)
            print("Converting RGB image to grayscale...")
            gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            print("Converted RGB image to grayscale...")
            print("Resizing image to 28x28 scale...")
            img_ = cv2.resize(gray,(28,28))
            print("Resized...")
            img_resized = cv2.imwrite(filename='saved_img-final.jpg', img=img_)
            print("Image saved!")
           
            break
       
        elif key == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break
   
    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break

img1_path = r"C:\Users\BlueSky\Downloads\deepface-master\saved_img.jpg"
img2_path = r"C:\Users\BlueSky\Downloads\deepface-master\Messi1.jpg"

img1 = DeepFace.detectFace(img1_path)
img2 = DeepFace.detectFace(img2_path)

model_name = 'Facenet'

resp = DeepFace.verify(img1_path, img2_path, model_name = model_name)

print(resp)