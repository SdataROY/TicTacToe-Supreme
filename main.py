import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
GRID_SIZE = 4
CELL_SIZE = 100
GRID_LINE_WIDTH = 5  # Grid line width
WIN_LINE_WIDTH = 10  # Winning line width to match X and O
CIRCLE_WIDTH = 10
CROSS_WIDTH = 10
SPACE = CELL_SIZE // 4
SCORE_HEIGHT = 90
BOTTOM_SPACE = 70
BORDER_WIDTH = 70
TOTAL_WIDTH = GRID_SIZE * CELL_SIZE + 2 * BORDER_WIDTH
TOTAL_HEIGHT = GRID_SIZE * CELL_SIZE + SCORE_HEIGHT + BOTTOM_SPACE

# Colors
BACKGROUND_COLOR = (20, 189, 172)
GRID_COLOR = (13, 161, 146)
O_COLOR = (242, 235, 211)
X_COLOR = (84, 84, 84)
HIGHLIGHT_COLOR = (22, 208, 189)

# Screen setup
screen = pygame.display.set_mode((TOTAL_WIDTH, TOTAL_HEIGHT))
pygame.display.set_caption("TicTacToe Supreme")

# Fonts
font = pygame.font.Font(None, 36)

# Game variables
board = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player = "X"
game_over = False
winner_cells = []
player_x_score = 0
player_o_score = 0
draws = 0
starting_player = "X"

def draw_lines():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, (BORDER_WIDTH, SCORE_HEIGHT + i * CELL_SIZE), (TOTAL_WIDTH - BORDER_WIDTH, SCORE_HEIGHT + i * CELL_SIZE), GRID_LINE_WIDTH)
        pygame.draw.line(screen, GRID_COLOR, (BORDER_WIDTH + i * CELL_SIZE, SCORE_HEIGHT), (BORDER_WIDTH + i * CELL_SIZE, SCORE_HEIGHT + GRID_SIZE * CELL_SIZE), GRID_LINE_WIDTH)

def draw_figures():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "X":
                pygame.draw.line(screen, X_COLOR, (BORDER_WIDTH + col * CELL_SIZE + SPACE, SCORE_HEIGHT + row * CELL_SIZE + SPACE),
                                 (BORDER_WIDTH + col * CELL_SIZE + CELL_SIZE - SPACE, SCORE_HEIGHT + row * CELL_SIZE + CELL_SIZE - SPACE),
                                 CROSS_WIDTH)
                pygame.draw.line(screen, X_COLOR, (BORDER_WIDTH + col * CELL_SIZE + CELL_SIZE - SPACE, SCORE_HEIGHT + row * CELL_SIZE + SPACE),
                                 (BORDER_WIDTH + col * CELL_SIZE + SPACE, SCORE_HEIGHT + row * CELL_SIZE + CELL_SIZE - SPACE), CROSS_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, O_COLOR, (BORDER_WIDTH + col * CELL_SIZE + CELL_SIZE // 2, SCORE_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2),
                                   CELL_SIZE // 2 - SPACE, CIRCLE_WIDTH)

def highlight_winner_cells():
    for cell in winner_cells:
        row, col = cell
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (BORDER_WIDTH + col * CELL_SIZE, SCORE_HEIGHT + row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_winner_line():
    color = X_COLOR if player == "X" else O_COLOR
    if len(winner_cells) == 4:
        centers = [(BORDER_WIDTH + col * CELL_SIZE + CELL_SIZE // 2, SCORE_HEIGHT + row * CELL_SIZE + CELL_SIZE // 2)
                   for row, col in winner_cells]

        # Check for square winning condition
        if winner_cells == [(winner_cells[0][0], winner_cells[0][1]),
                            (winner_cells[0][0], winner_cells[1][1]),
                            (winner_cells[2][0], winner_cells[2][1]),
                            (winner_cells[3][0], winner_cells[3][1])]:
            # Draw square
            top_left = centers[0]
            top_right = centers[1]
            bottom_right = centers[3]
            bottom_left = centers[2]
            pygame.draw.line(screen, color, top_left, top_right, WIN_LINE_WIDTH)
            pygame.draw.line(screen, color, top_right, bottom_right, WIN_LINE_WIDTH)
            pygame.draw.line(screen, color, bottom_right, bottom_left, WIN_LINE_WIDTH)
            pygame.draw.line(screen, color, bottom_left, top_left, WIN_LINE_WIDTH)
        elif winner_cells == [(0, 0), (0, 3), (3, 0), (3, 3)]:
            pygame.draw.line(screen, color, centers[0], centers[3], WIN_LINE_WIDTH)
            pygame.draw.line(screen, color, centers[1], centers[2], WIN_LINE_WIDTH)
        else:
            # Extend line beyond the grid for non-square cases
            if centers[0][0] == centers[1][0]:  # Vertical line
                pygame.draw.line(screen, color, (centers[0][0], centers[0][1]), (centers[-1][0], centers[-1][1]), WIN_LINE_WIDTH)
            elif centers[0][1] == centers[1][1]:  # Horizontal line
                pygame.draw.line(screen, color, (centers[0][0], centers[0][1]), (centers[-1][0], centers[-1][1]), WIN_LINE_WIDTH)
            else:  # Diagonal line
                if centers[0][0] < centers[1][0]:  # top-left to bottom-right diagonal
                    pygame.draw.line(screen, color, centers[0], centers[-1], WIN_LINE_WIDTH)
                else:  # top-right to bottom-left diagonal
                    pygame.draw.line(screen, color, centers[0], centers[-1], WIN_LINE_WIDTH)


def check_winner(mark):
    global winner_cells
    winner_cells = []
    # Check horizontal and vertical
    for i in range(GRID_SIZE):
        if all([board[i][j] == mark for j in range(GRID_SIZE)]):
            winner_cells = [(i, j) for j in range(GRID_SIZE)]
            return True
        if all([board[j][i] == mark for j in range(GRID_SIZE)]):
            winner_cells = [(j, i) for j in range(GRID_SIZE)]
            return True

    # Check diagonals
    if all([board[i][i] == mark for i in range(GRID_SIZE)]):
        winner_cells = [(i, i) for i in range(GRID_SIZE)]
        return True
    if all([board[i][GRID_SIZE - 1 - i] == mark for i in range(GRID_SIZE)]):
        winner_cells = [(i, GRID_SIZE - 1 - i) for i in range(GRID_SIZE)]
        return True

    # Check squares
    for i in range(GRID_SIZE - 1):
        for j in range(GRID_SIZE - 1):
            if board[i][j] == board[i][j + 1] == board[i + 1][j] == board[i + 1][j + 1] == mark:
                winner_cells = [(i, j), (i, j + 1), (i + 1, j), (i + 1, j + 1)]
                return True

    # Check the order grids
    order_positions = [(0, 0), (0, GRID_SIZE - 1), (GRID_SIZE - 1, 0), (GRID_SIZE - 1, GRID_SIZE - 1)]
    if all([board[x][y] == mark for x, y in order_positions]):
        winner_cells = order_positions
        return True

    return False

def draw_winner_text(winner):
    color = X_COLOR if winner == "X" else O_COLOR
    text = font.render("GAME OVER! Player {} Wins!".format(winner), True, color)
    screen.blit(text, (TOTAL_WIDTH // 2 - text.get_width() // 2, TOTAL_HEIGHT - BOTTOM_SPACE + 10))

def draw_draw_text():
    text = font.render("GAME OVER! It's a Draw!", True, X_COLOR)
    screen.blit(text, (TOTAL_WIDTH // 2 - text.get_width() // 2, TOTAL_HEIGHT - BOTTOM_SPACE + 10))

def draw_score():
    score_text = font.render("Player X: {}  Player O: {}  Draws: {}".format(player_x_score, player_o_score, draws), True, X_COLOR)
    screen.blit(score_text, (TOTAL_WIDTH // 2 - score_text.get_width() // 2, 10))

def draw_turn():
    if not game_over:
        turn_text = font.render("Player {}'s turn".format(player), True, X_COLOR if player == "X" else O_COLOR)
        screen.blit(turn_text, (TOTAL_WIDTH // 2 - turn_text.get_width() // 2, 40))

def reset_game():
    global board, game_over, winner_cells, player, starting_player
    board = [[" " for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    game_over = False
    winner_cells = []
    starting_player = "O" if starting_player == "X" else "X"
    player = starting_player

def main():
    global player, game_over, player_x_score, player_o_score, draws

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    reset_game()
                else:
                    mouse_x, mouse_y = event.pos
                    clicked_row = (mouse_y - SCORE_HEIGHT) // CELL_SIZE
                    clicked_col = (mouse_x - BORDER_WIDTH) // CELL_SIZE

                    if 0 <= clicked_row < GRID_SIZE and 0 <= clicked_col < GRID_SIZE and board[clicked_row][clicked_col] == " ":
                        board[clicked_row][clicked_col] = player
                        if check_winner(player):
                            game_over = True
                            if player == "X":
                                player_x_score += 1
                            else:
                                player_o_score += 1
                        else:
                            player = "O" if player == "X" else "X"

                        if not any(" " in row for row in board):
                            game_over = True
                            draws += 1

        screen.fill(BACKGROUND_COLOR)
        highlight_winner_cells()
        draw_lines()
        draw_figures()
        draw_score()
        draw_turn()

        if game_over:
            draw_winner_line()
            if any(check_winner(p) for p in ["X", "O"]):
                draw_winner_text(player)
            else:
                draw_draw_text()

        pygame.display.update()

if __name__ == "__main__":
    main()
