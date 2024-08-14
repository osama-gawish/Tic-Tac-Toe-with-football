# disable grayscale cam

from ultralytics import YOLO
import cv2
import numpy as np
import pygame
import time


def initialize_game(window_width1, window_height1):
    pygame.init()
    screen1 = pygame.display.set_mode((window_width1, window_height1))
    pygame.display.set_caption('Click to Turn Green')
    return screen1


def create_game_surface(width1, height1):
    return pygame.Surface((width1, height1))


# Parameters
width, height = 300, 200
scaleFactor = 1.5
window_width, window_height = width * scaleFactor, height * scaleFactor

# Initialize the game
screen = initialize_game(window_width, window_height)
game_surface = create_game_surface(width, height)

black = (255, 255, 255)
green = (0, 255, 0)
click_positions = []

# Load the perspective transform matrix from the file
M = np.load('perspective_transform_matrix.npy')
dst_width = 87 * 5  # Width of the destination image
dst_height = 74 * 5  # Height of the destination image

# Load the YOLO model
model = YOLO('yolov8n.pt')

# Start capturing video from the default webcam
cap = cv2.VideoCapture(1)  # detection
# cap2 = cv2.VideoCapture(1)  # grayscale

cap.set(cv2.CAP_PROP_FPS, 55)
# Get the frames per second (fps) of the video
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)

while True:
    ret, frame = cap.read()  # detectioncam
    # ret2, frame2 = cap2.read()  # black and white cam
    if not ret:
        break

    game_surface.fill(black)

    # Run object detection on the current frame
    results = model(frame, show=False, conf=0.2, save=False,classes=32, verbose=False)

    # Extract click positions from bounding boxes
    for box in results[0].boxes:
        # Get the coordinates of the bounding box
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        cx = int((x1 + x2) / 2)
        cy: int = int((y1 + y2) / 2)
        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # Ball hit detected
        if cv2.waitKey(1) & 0xFF == ord("h"):
            mouse_x, mouse_y = cx, cy
            pos = (mouse_x * width // window_width, mouse_y * height // window_height)
            click_positions.append(pos)
            print('hit')
            print(f'hiit detected at: {cx}, {cy}')
            time.sleep(0.5)

    for pos in click_positions:
        pygame.draw.circle(game_surface, green, pos, 10)

    scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
    screen.blit(scaled_surface, (0, 0))
    pygame.display.flip()

    # Show the frame with detected objects
    cv2.imshow('YOLO Detection', frame)

    # Check for the quit key ('q')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the OpenCV window
cap.release()
cv2.destroyAllWindows()
