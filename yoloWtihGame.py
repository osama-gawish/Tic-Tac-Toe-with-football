# todo: make the game take the whole screen size (laptop screen)

from ultralytics import YOLO
import cv2
import numpy as np
import pygame
import time

# Check if newcameramtx and roi are present in the file, otherwise compute them
if newcameramtx is None or roi is None:
    print("Optimal new camera matrix and ROI not found in the file, computing them...")
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (640, 480), 1, (640, 480))

# Load the perspective transform matrix from the file
M = np.load('perspective_transform_matrix.npy')
dst_width = 87 * 5  # Width of the destination image in pixels
dst_height = 74 * 5  # Height of the destination image in pixels. use actual real dimensions with a scale factor

def initialize_game(window_width, window_height):
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Click to Turn Green')
    return screen

def create_game_surface(width, height):
    return pygame.Surface((width, height))


# Parameters
width, height = dst_width, dst_height # todo: adjust so it matches detection cam dimintions
scaleFactor = 1
window_width, window_height = width * scaleFactor, height * scaleFactor

# Initialize the game
game_surface = create_game_surface(width*1.25, height*1.25) # It seems that pygame uses its own pixel size. that's why I multplied by 1.25
screen = initialize_game(window_width, window_height)

white = (255, 255, 255)
green = (0, 255, 0)
click_positions = []

# Load the calibration parameters
with np.load('camera_calibration.npz') as data:
    mtx = data['mtx']
    dist = data['dist']
    newcameramtx = data.get('newcameramtx')
    roi = data.get('roi')




#### Staff for grayscale camera
def convert_to_bw(frame):
    lower = np.array([0, 0, 80])
    upper = np.array([60, 100, 255])  # range for blue color
    bw_frame = cv2.inRange(frame, lower, upper)
    return bw_frame


# ROI for the second camera
c2x1, c2y1, c2x2, c2y2 = 0, 200, 640, 480  # Note that we have x and y variables for both cameras

#####

# Load the YOLO model
model = YOLO('yolov8n.pt')

# Start capturing video from the default webcam
cap = cv2.VideoCapture(0)  # detection
cap2 = cv2.VideoCapture(1)  # grayscale

cap.set(cv2.CAP_PROP_FPS, 55)
# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)



while True:
    ret, frame = cap.read()  # detectioncam
    ret2, frame2 = cap2.read()  # black and white cam
    if not ret or not ret2:
        break
    game_surface.fill(white)
    # Undistort the frame
    undistorted_frame = cv2.undistort(frame, mtx, dist, None, newcameramtx)
    undistorted_frame = cv2.warpPerspective(undistorted_frame, M, (dst_width, dst_height))

    # Run object detection on the current frame
    results = model(frame, show=False, conf=0.1, save=False, classes=0, verbose=False)

    # Convert the second camera's frame to grayscale
    # Define the region of interest
    c2_roi = frame2[c2y1:c2y2, c2x1:c2x2]
    # Convert ROI to grayscale
    c2_roi = cv2.cvtColor(c2_roi, cv2.COLOR_BGR2RGB)
    # Convert grayscale frame to black and white
    bw_frame = convert_to_bw(c2_roi)
    num_white_pixels = cv2.countNonZero(bw_frame)

    # Extract click positions from bounding boxes
    for box in results[0].boxes:
        # Get the coordinates of the bounding box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx = int((x1 + x2) / 2)
        cy = int((y1 + y2) / 2)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # Ball hit detected
        if cv2.waitKey(1) & 0xFF == ord('h'):
        # if num_white_pixels > 3000:
            mouse_x, mouse_y = cx*1.25, cy*1.25
            # pos = (mouse_x * width // window_width, mouse_y * height // window_height)
            pos = (mouse_x, mouse_y)
            click_positions.append(pos)
            print('hit')
            print(f'hit detected at: {cx}, {cy}')
            time.sleep(0.5)
    for pos in click_positions:
        pygame.draw.circle(game_surface, green, pos, 10)
    scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()
    # Show the frame with detected objects
    cv2.imshow('YOLO Detection', frame)
    cv2.imshow('Grayscale - Camera 2', bw_frame)

    # Check for the quit key ('q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
