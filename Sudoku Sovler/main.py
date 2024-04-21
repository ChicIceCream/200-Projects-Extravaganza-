def is_valid_move(grid, row, col, number):
    """
    This function basically tells us if it is possible for the number to be placed in that positi
    on or not
    """
    # This will check if the same number is present in the same column
    for x in range(9):
        if [row][x] == number:
            return False
    
    # This will check if the same number is present in the same row
    for x in range(9): 
        if [x][col] == number:
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
    
    # We will check if the place we are inputting the number is overflowing or not
    if col == 9: # We put 9, because the olumns can go from 1 to 8
        if row == 8: # If we have reached the 8th row, then we will end the Sudoku puzzle
            return True
        row += 1
        col = 0
        
        # Now we keep calling this funciton recursively until we reach column 9
        if grid[row][col] > 0:
            return solve(grid, row, col)
        
        for num in range(1, 10):
            
            if is_valid_move(grid, row, col, num):
                
                # It is obvious that if the number is a valid move, the number will be placed in that grid place
                grid[row][col] = num
                
                if solve(grid, row, col + 1):
                    return True
            
            grid[row][col] = 0 
        
        return False

if solve(grid, 0, 0):
    for i in range(9):
        for j in range(9):
            print(f'{grid[i][j]}', end=" ")
else:
    print(f'No Solution was found for the provided Suduko!')