def is_valid_move(grid, row, col, number):
    """
    This function checks if it is possible to place the given number
    in the specified position without violating Sudoku rules.
    """
    # This will check if the same number is present in the same column
    for x in range(9):
        if grid[row][x] == number:
            return False
    
    # This will check if the same number is present in the same row
    for x in range(9): 
        if grid[x][col] == number:
            return False
    
    # This code checks if the number can be placed in the 3x3 square
    corner_row = row - row % 3  # Finds the top-left corner
    corner_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if grid[corner_row + x][corner_col + y] == number:
                return False
    
    return True

def solve(grid, row, col):
    """
    This function solves the Sudoku puzzle using backtracking.
    """
    # We will check if the place we are inputting the number is overflowing or not
    if col == 9: # We put 9, because the columns can go from 0 to 8
        if row == 8: # If we have reached the 8th row, then we will end the Sudoku puzzle
            return True
        row += 1
        col = 0
        
    # Now we keep calling this function recursively until we reach column 9
    if grid[row][col] == 0:
        for num in range(1, 10):
            if is_valid_move(grid, row, col, num):
                # If the number is a valid move, place it in the grid
                grid[row][col] = num
                # Recursively solve the puzzle
                if solve(grid, row, col + 1):
                    return True
                # If the solution fails, backtrack by resetting the grid position
                grid[row][col] = 0
        return False
    else:
        # If the cell is already filled, move to the next column
        return solve(grid, row, col + 1)

grid = [
    [5, 0, 0, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 7, 8, 3],
    [0, 0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 3, 0, 0, 1, 0, 0, 0],
    [0, 8, 0, 0, 0, 0, 0, 7, 0],
    [0, 0, 0, 9, 0, 0, 0, 0, 0],
    [0, 0, 7, 6, 0, 0, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1]
]

if solve(grid, 0, 0):
    for i in range(9):
        for j in range(9):
            print(f'{grid[i][j]}', end=" ") # This will simply print out the whole grid without line breaks
        print(f' ')
else:
    print(f'No Solution was found for the provided Suduko!')