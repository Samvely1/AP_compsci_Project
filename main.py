import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_size = (800, 650)
cell_size = 80
font_size = 64
font = pygame.font.Font(None, font_size)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)

GREEN = (0,255,0)

def create_board(size, num_mines):
    board = [[' ' for _ in range(size)] for _ in range(size)]
    mines = set()

    while len(mines) < num_mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        mines.add((row, col))
        board[row][col] = 'X'
    return board

def print_board():
    noah = True
    size = len(board)
    for row in range(size):
        for col in range(size):
            cell = board[row][col]
            cell_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)

            if cell == 'X':
                pygame.draw.rect(window, WHITE, cell_rect)
            elif cell.isdigit():
                pygame.draw.rect(window, GRAY, cell_rect)

                # Different color for cells with digits
                text_color = BLACK
                cell_color = GREEN  # Change to the desired color

                text = font.render(cell, True, text_color)
                text_rect = text.get_rect(center=cell_rect.center)
                pygame.draw.rect(window, cell_color, cell_rect)  # Draw cell with custom color
                window.blit(text, text_rect)
            else:
                pygame.draw.rect(window, WHITE, cell_rect)

    pygame.display.update()

def count_adjacent_mines(row, col):
    size = len(board)
    count = 0

    for i in range(max(0, row - 1), min(row + 2, size)):
        for j in range(max(0, col - 1), min(col + 2, size)):
            if board[i][j] == 'X':
                count += 1

    return count

def reveal_cell(row, col, revealed):
    if board[row][col] != ' ' or (row, col) in revealed:
        return

    size = len(board)
    count = count_adjacent_mines(row, col)
    board[row][col] = str(count) if count > 0 else ' '
    revealed.add((row, col))

    if count == 0:
        for i in range(max(0, row - 1), min(row + 2, size)):
            for j in range(max(0, col - 1), min(col + 2, size)):
                reveal_cell(i, j, revealed)

def play_game(size, num_mines):
    global board
    board = create_board(size, num_mines)
    game_over = False
    revealed_cells = set()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    row = mouse_pos[1] // cell_size
                    col = mouse_pos[0] // cell_size

                    if board[row][col] == 'X':
                        print('Game Over!')
                        game_over = True
                    else:
                        reveal_cell(row, col, revealed_cells)
                        total_cells = size * size
                        revealed_count = len(revealed_cells)
                        if revealed_count + num_mines == total_cells:
                            print_board()
                            print('Congratulations! You won!')
                            game_over = True

        print_board()

# Start the game
play_game(8, 10)




'''import random
import pygame
pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()

def create_board(size, num_mines):
    board = [[' ' for _ in range(size)] for _ in range(size)]
    mines = set()

    while len(mines) < num_mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        mines.add((row, col))
        board[row][col] = 'X'

    return board

def print_board(board):
    size = len(board)
    print('   ' + ' '.join(str(i) for i in range(size)))  
    print('  ' + '-' * (size * 2 + 1))

    for row in range(size):
        print(f'{row} |', end=' ')
        for col in range(size):
            print(board[row][col], end=' ')
        print('|')

    print('  ' + '-' * (size * 2 + 1))

def count_adjacent_mines(board, row, col):
    size = len(board)
    count = 0

    for i in range(max(0, row - 1), min(row + 2, size)):
        for j in range(max(0, col - 1), min(col + 2, size)):
            if board[i][j] == 'X':
                count += 1

    return count

def reveal_cell(board, row, col, revealed):
    if board[row][col] != ' ' or (row, col) in revealed:
        return

    size = len(board)
    count = count_adjacent_mines(board, row, col)
    board[row][col] = str(count) if count > 0 else ' '
    revealed.add((row, col))

    if count == 0:
        for i in range(max(0, row - 1), min(row + 2, size)):
            for j in range(max(0, col - 1), min(col + 2, size)):
                reveal_cell(board, i, j, revealed)

def play_game(size, num_mines):
    board = create_board(size, num_mines)
    game_over = False

    while not game_over:
        print_board(board)
        print("Enter the row and column (separated by a space) or 'f' to flag a cell:")
        user_input = input("> ")
        parts = user_input.strip().split()

        if len(parts) == 2:
            row, col = map(int, parts)
            if board[row][col] == 'X':
                print('Game Over!')
                game_over = True
            else:
                reveal_cell(board, row, col, set())
        elif len(parts) == 1 and parts[0] == 'f':
            print("Enter the row and column (separated by a space) to flag a cell:")
            user_input = input("> ") 
            parts = user_input.strip().split()
            row, col = map(int, parts)
            board[row][col] = 'F'
        else:
            print('Invalid input. Please try again.')

        if not game_over:
            total_cells = size * size
            revealed_cells = sum(row.count(' ') for row in board)
            if revealed_cells + num_mines == total_cells:
                print_board(board)
                print('Congratulations! You won!')
                game_over = True

play_game(8, 10)'''