import cv2
import os
import datetime
def take_picture():
    # Open the default camera (usually the built-in webcam)
    try:
        cap = cv2.VideoCapture(0)

        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return        
        # Save the captured frame as an image file (e.g., "captured_image.jpg")
        current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        cv2.imwrite(f"captured/{current_datetime}.jpg", frame)

        # Release the camera
        cap.release()

        print("PICTURED SAVED")
        # view the pic
        new_filename = os.path.join('captured', f"{current_datetime}.jpg")
        os.startfile(new_filename)
    except Exception as e:
        print(e)


        