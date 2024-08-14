import cv2
import numpy as np
import time


def convert_to_bw(frame):
    lower = np.array([0, 0, 80])
    upper = np.array([60, 100, 255])
    bw_frame = cv2.inRange(frame, lower, upper)
    return bw_frame


def main():
    # Open webcam
    cap = cv2.VideoCapture(1)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return

    x1, y1, x2, y2 = 0, 200, 640, 480

    while True:
        # start_time = time.time()
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame")
            break

        # Define the region of interest
        roi = frame[y1:y2, x1:x2]

        # Convert ROI to grayscale
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)

        # Convert grayscale frame to black and white
        bw_frame = convert_to_bw(gray_roi)

        num_white_pixels = cv2.countNonZero(bw_frame)
        # print(num_white_pixels)
        if num_white_pixels > 3000:
            print(num_white_pixels)
            time.sleep(0.5)

        # Display the black and white frame
        cv2.imshow('Black and White Webcam', roi)

        # Check for 'q' key press to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
