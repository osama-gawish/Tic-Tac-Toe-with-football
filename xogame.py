import pygame
import sys

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Sound effects
o_sound = pygame.mixer.Sound('o_sound.wav')
win_sound = pygame.mixer.Sound('winsound.wav')
x_sound = pygame.mixer.Sound('x_sound.wav')
# Constants
WIDTH, HEIGHT = 500, 500
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# WHITE = (255, 255, 255)
BG_COLOR = (0, 0, 74)  # background color
LINE_COLOR_x = (220, 20, 30)
LINE_COLOR_o = (0, 30, 230)

# Screen setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# this is a new thing in branch one
print('test and push')
# Board setup
board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Fonts
font = pygame.font.Font(None, 60)

# Load images
o_image = pygame.image.load('o_image.png')  # Replace with the correct path
x_image = pygame.image.load('x_image.png')  # Replace with the correct path

# Scale images to fit the squares
o_image = pygame.transform.scale(o_image, (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))
x_image = pygame.transform.scale(x_image, (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))


# Draw lines
def draw_lines_x():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR_x, (0, 0), (WIDTH, 0), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR_x, (0, 0), (0, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_x, (3 * SQUARE_SIZE, 0), (3 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_lines_o():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR_o, (0, 0), (WIDTH, 0), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (0, 3 * SQUARE_SIZE), (WIDTH, 3 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR_o, (0, 0), (0, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR_o, (3 * SQUARE_SIZE, 0), (3 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                screen.blit(o_image, (col * SQUARE_SIZE + 10, row * SQUARE_SIZE + 10))

            elif board[row][col] == 2:
                screen.blit(x_image, (col * SQUARE_SIZE + 5, row * SQUARE_SIZE + 5))


def check_winner(player):
    for row in range(BOARD_ROWS):
        if board[row][0] == board[row][1] == board[row][2] == player:
            return True
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] == player:
            return True
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    if board[2][0] == board[1][1] == board[0][2] == player:
        return True
    return False


def check_draw():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 0:
                return False
    return True


def restart():
    screen.fill(BG_COLOR)
    draw_lines_x()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0


def handle_click(position, player):
    mouseX, mouseY = position

    clicked_row = mouseY // SQUARE_SIZE
    clicked_col = mouseX // SQUARE_SIZE

    if board[clicked_row][clicked_col] == 0:
        board[clicked_row][clicked_col] = player
        draw_figures()
        if check_winner(player):
            win_sound.play()
            return 'O wins!' if player == 1 else 'X wins!'
        elif check_draw():
            win_sound.play()
            return 'Draw!'


        return None
    return None


while True:
    draw_lines_x()

    player = 2
    game_over = False
    result_text = ""

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                result_text = handle_click(event.pos, player)
                if result_text:
                    game_over = True
                else:
                    player = 2 if player == 1 else 1
                    # draw_lines_o() if player == 1 else draw_lines_x()  # flip between lines color after each turn
                    if player == 1:
                        draw_lines_o()
                        o_sound.play()
                    else:
                        draw_lines_x()
                        x_sound.play()
            else:
                # Restart the game if left-clicking after the game is over
                if event.type == pygame.MOUSEBUTTONDOWN and game_over:  # 1 represents the left mouse button
                    restart()
                    game_over = False
                    player = 2
                    result_text = ""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart()
                    game_over = False
                    player = 2
                    result_text = ""
        if game_over:
            text = font.render(result_text, True, RED)
            text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
            screen.blit(text, text_rect)
        pygame.display.update()


