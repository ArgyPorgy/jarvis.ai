import requests
import numpy as np 
import cv2

def cctv(output_file='output_cctv_video.mp4'):
    fourccCode = cv2.VideoWriter_fourcc(*'mp4v')  # You can choose other codecs based on your preferences
    out = cv2.VideoWriter(output_file, fourccCode, 20.0, (640, 480))

    while True: 
        images = requests.get("http://192.168.21.41:8080/shot.jpg")  # Replace with your phone's IP address and port
        video = np.array(bytearray(images.content), dtype=np.uint8)
        render = cv2.imdecode(video, -1)
        cv2.imshow('frame', render)
        out.write(render)

        if (cv2.waitKey(1) & 0xFF == ord('q')):
            break

    out.release()
    cv2.destroyAllWindows()

# Call the function
# capture_and_write_video()
