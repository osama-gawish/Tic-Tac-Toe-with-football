import pygame
import sys
'''
screen vs game_surface
surface is where you'll do all your drawing and game logic updates. it is the size of opencv window
screen is the display. it is the size of laptop screen
'''


# Initialize pygame
pygame.init()

# Set up the display
width, height = 600, 400  # Actual game size
scaleFactor = 1.5
window_width, window_height = width * scaleFactor, height * scaleFactor  # Window display size
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Click to Turn Green')

# Define colors
black = (255, 255, 255)
green = (0, 255, 0)

# background_image = pygame.image.load('cars.png')
# Scale the background image to fit the screen (if necessary)
# background_image = pygame.transform.scale(background_image, (width, height))


# Create a smaller game surface
game_surface = pygame.Surface((width, height))
# Set up a list to store the positions of clicks
click_positions = []

# Main loop
running = True
while running:
    # Fill the screen with black
    game_surface.fill(black)
    # screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Get the position of the mouse click relative to the window size
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Scale the position to match the game surface
                pos = (mouse_x * width // window_width, mouse_y * height // window_height)
                # Append the position to the list
                click_positions.append(pos)
                print(f"Mouse clicked at {pos}")

    # Draw all the green circles for each click position
    for pos in click_positions:
        pygame.draw.circle(game_surface, green, pos, 10)

    # Scale the game surface to the window size and blit it to the screen
    scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
    screen.blit(scaled_surface, (0, 0))
    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
