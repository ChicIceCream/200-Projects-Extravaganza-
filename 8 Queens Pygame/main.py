import pygame
import sys
import time
# Initialize pygame
pygame.init()

# Constants
ROWS, COLS = 8, 8
CELL_SIZE = 60
BOARD_WIDTH = COLS * CELL_SIZE   # 8 * 60 = 480
SIDE_PANEL_WIDTH = 300           # Width for side screen
WIDTH = BOARD_WIDTH + SIDE_PANEL_WIDTH
HEIGHT = ROWS * CELL_SIZE        # 480
FPS = 1  # controls animation speed

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (220, 220, 220)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("8 Queens Animation with Side Panel")

# Font for drawing text
font = pygame.font.SysFont("monospace", 20)
big_font = pygame.font.SysFont("monospace", 40)

def draw_board(current_row, board):
    """Draw the chess board with queens and a side panel showing internal variables."""
    # Fill entire screen white
    screen.fill(WHITE)
    
    # --- Draw the chess board area ---
    for row in range(ROWS):
        for col in range(COLS):
            # Compute cell rectangle in board area (left part)
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            # If a queen is placed at this row (board[row] equals col), draw "*"
            if board[row] == col:
                text = big_font.render("*", True, BLACK)
            else:
                text = big_font.render("-", True, BLACK)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
    
    # --- Draw the side panel ---
    side_rect = pygame.Rect(BOARD_WIDTH, 0, SIDE_PANEL_WIDTH, HEIGHT)
    pygame.draw.rect(screen, LIGHT_GRAY, side_rect)
    pygame.draw.rect(screen, BLACK, side_rect, 2)
    
    # Prepare text lines for side panel
    lines = []
    lines.append("DEBUG INFO:")
    lines.append(f"Current Row: {current_row}")
    # Display the board state as a list; if not placed, show '-'
    board_state = []
    for i in range(ROWS):
        if board[i] == -1:
            board_state.append("-")
        else:
            board_state.append(str(board[i]))
    lines.append("Board State:")
    lines.append(" ".join(board_state))
    
    # Display each line in the side panel
    y_offset = 20
    for line in lines:
        text = font.render(line, True, BLACK)
        screen.blit(text, (BOARD_WIDTH + 10, y_offset))
        y_offset += 30

    pygame.display.flip()

def process_events():
    """Process pygame events so the window remains responsive."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def solve_queens(row, board):
    """Backtracking solution for 8 Queens with animation and side panel updates.
    
    board is a list of length ROWS where board[i] is the column index of the queen in row i,
    or -1 if no queen is placed.
    """
    process_events()
    draw_board(row, board)
    pygame.time.wait(500)  # wait 500ms to animate the current step
    
    if row == ROWS:
        return True

    for col in range(COLS):
        if is_safe(row, col, board):
            board[row] = col  # Place queen at (row, col)
            if solve_queens(row + 1, board):
                return True  # Stop after finding one solution
            board[row] = -1  # Backtrack: remove queen from row
            draw_board(row, board)
            pygame.time.wait(500)
    return False

def is_safe(row, col, board):
    """Check if placing a queen at (row, col) is safe given current board state."""
    for prev_row in range(row):
        # Check same column or diagonal conflicts
        if board[prev_row] == col or abs(board[prev_row] - col) == abs(prev_row - row):
            return False
    return True

def main():
    # Initialize board with -1 meaning no queen is placed in that row
    board = [-1] * ROWS
    solve_queens(0, board)
    
    # Final drawing of solution with side panel
    draw_board(ROWS, board)
    while True:
        process_events()
        pygame.time.wait(100)

if __name__ == "__main__":
    main()
