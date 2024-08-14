import pygame
import sys


def initialize_game(window_width, window_height):
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Click to Turn Green')
    return screen


def create_game_surface(width, height):
    return pygame.Surface((width, height))


def main_loop(screen, game_surface, width, height, window_width, window_height, get_user_input):
    black = (255, 255, 255)
    green = (0, 255, 0)
    click_positions = []

    running = True
    while running:
        game_surface.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = get_user_input()
                    pos = (mouse_x * width // window_width, mouse_y * height // window_height)
                    click_positions.append(pos)
                    print(f"Mouse clicked at {pos}")

        for pos in click_positions:
            pygame.draw.circle(game_surface, green, pos, 10)

        scaled_surface = pygame.transform.scale(game_surface, (window_width, window_height))
        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

    pygame.quit()
    sys.exit()
