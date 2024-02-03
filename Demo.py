import streamlit as st
import cv2

st.title('AI Fitness Trainer: Squats Analysis')

# Open the front camera (index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    st.error("Error: Unable to access the front camera.")
else:
    # Read frames from the camera
    while True:
        ret, frame = cap.read()

        if not ret:
            st.error("Error: Unable to capture a frame.")
            break

        # Display the frame in the Streamlit app
        # st.image(frame, channels="BGR")

        # # Check if the user pressed the 'Stop' button to exit
        #   # Generate a dynamic key
        # if st.button("Stop", key='q'):
        #     break
        sample_vid = st.empty()
        sample_vid.video(0)

    # Release the camera when done
    cap.release()
