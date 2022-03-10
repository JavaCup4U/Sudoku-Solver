import sys
import pygame

pygame.init()

width = 500
height = 600



screen = pygame.display.set_mode((width, height))
title = pygame.display.set_caption("Sudoku")


x = 0 
y = 0
dif = 500 / 9
val = 0
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

font1 = pygame.font.SysFont("comicsans", 30)
font2 = pygame.font.SysFont("comicsans", 20)
def cord(pos):
    global x 
    x = pos[0] // dif 
    global y 
    y = pos[1] // dif 


def draw_box():
    for i in range(2):
        pygame.draw.line(screen, (255, 0, 0), (x * dif - 3, (y + i) * dif), (x * dif + dif + 3, (y + i ) * dif), 7)
        pygame.draw.line(screen, (255, 0, 0), ( (x + i) * dif, y * dif), ((x + i ) * dif, y * dif + dif ), 7)


def draw():
    # Draw lines to screen
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:

                # Fill green in already filled box 
                pygame.draw.rect(screen, (205, 127, 50), (i * dif, j * dif, dif + 1, dif + 1))
                
                # Fill box with numbers specified
                text1 = font1.render(str(board[i][j]), 1, (0, 0, 0 ))
                screen.blit(text1, (i * dif + 15, j * dif + 15))
    
    # Draw lines horizontally and vertically to create board
    for i in range(10):
        if i % 3 == 0:
            thick = 7
        else:
            thick = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * dif), (500, i * dif), thick)
        pygame.draw.line(screen, (0, 0, 0), (i * dif, 0), (i * dif, 500), thick)

# Fill value entered 
def draw_value(val):
    text1 = font1.render(str(val), 1, (0, 0, 0))
    screen.blit(text1, (x * dif + 15, y * dif + 15))

# Error when wrong value is entered
def error1():
    text1 = font1.render("Incorrect !", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))
def error2():
    text1 = font1.render("Incorrect, not a valid key.", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))

# Check if value entered is valid 
def val_check(m, i, j, val):
    for it in range(9):
        if m[i][it] == val:
            return False
        if m[it][j] == val:
            return False
    it = i//3
    jt = j//3
    for i in range(it * 3, it * 3 + 3):
        for j in range(jt * 3, jt * 3 + 3):
            if m[i][j] == val:
                return False
    return True



# BackTrack Algo to solve board
def solve(bo, i, j):

    while bo[i][j] != 0:
        if i < 8:
            i += 1
        elif i == 8 and j < 8:
            i = 0
            j += 1
        elif i == 8 and j == 8:
            return True
    pygame.event.pump()
    for it in range(1, 10):
        if val_check(bo, i, j, it) == True:
            bo[i][j] = it
            global x, y
            x = i
            y = j
            # White background 
            screen.fill(( 255, 255, 255))
            draw()
            draw_value(val)
            pygame.display.update()
            pygame.time.delay(20)
            if solve(bo, i, j) == 1:
                return True
            else:
                bo[i][j] = 0
            
            # white background
            screen.fill((255, 255, 255))

            draw()
            draw_box()
            pygame.display.update()
            pygame.time.delay(50)
    return False


# Game instructions 

def display_instructions():
    text1 = font2.render("Press D to reset to default / R to empty", 1, (0, 0, 0))
    text2 = font2.render("Enter values and press enter to visualize", 1, (0, 0, 0))
    screen.blit(text1, (20, 520))
    screen.blit(text2, (20, 540))
    
# Dislay options when solved 
def end_result():
    text1 = font1.render("Finished press R or D", 1, (0, 0, 0))
    screen.blit(text1, (20, 570))




def solve_puzzle(bo):
    
    # Base case 
    find = find_empty_spots(bo)
    if not find:
        return True
    else:
        row, col = find

    # Try to add a value into the position and 
    # check if it is valid 
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve_puzzle(bo):
                return True

            bo[row][col] = 0

    return False 
    

def valid(bo, num, pos):
    
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i]== num and pos[1] != i:
            return False
    # Check column 
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def find_empty_spots(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j) # row, col
    return None
    


background_color = (255, 255, 255)

running = True
flag1 = 0
flag2 = 0
rs = 0
error = 0

while running:
    
    # fill background color 

    screen.fill((background_color))
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
        
        # Get mouse position 
        if event.type == pygame.MOUSEBUTTONDOWN:
            flag1 = 1
            pos = pygame.mouse.get_pos()
            cord(pos)
        
        # Get number to be put if key is pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x -= 1
                flag1 = 1
            if event.key == pygame.K_RIGHT:
                x += 1
                flag1 = 1
            if event.key == pygame.K_UP:
                y -= 1
                flag1 = 1
            if event.key == pygame.K_DOWN:
                y += 1
                flag1 = 1
            if event.key == pygame.K_1:
                val = 1
            if event.key == pygame.K_2:
                val = 2
            if event.key == pygame.K_3:
                val = 3
            if event.key == pygame.K_4:
                val = 4
            if event.key == pygame.K_5:
                val = 5
            if event.key == pygame.K_6:
                val = 6
            if event.key == pygame.K_7:
                val = 7
            if event.key == pygame.K_8:
                val = 8
            if event.key == pygame.K_9:
                val = 9
            if event.key == pygame.K_s:
                solve(board, x, y)
            if event.key == pygame.K_RETURN:
                flag2 = 1
            
            # If R is pressed cleare the board
            if event.key == pygame.K_r:
                rs = 0
                error = 0
                flag2 = 0
                board =[
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]
                ]
            # If D is pressed reset the board to default
            if event.key == pygame.K_d:
                rs = 0 
                error = 0
                flag2 = 0
                board = [ [7,8,0,4,0,0,1,2,0],
                          [6,0,0,0,7,5,0,0,9],
                          [0,0,0,6,0,1,0,7,8],
                          [0,0,7,0,4,0,2,6,0],
                          [0,0,1,0,5,0,9,3,0],
                          [9,0,4,0,6,0,0,0,5],
                          [0,7,0,3,0,0,0,1,2],
                          [1,2,0,0,0,7,4,0,0],
                          [0,4,9,2,0,6,0,0,7]
                          ]
    if flag2 == 1:
        if solve(board, 0, 0) == False:
            error = 1
        else:
            rs = 1
        flag2 = 0
    
    if val != 0:
        draw_value(val)
        # print x 
        # print y 
        if val_check(board, int(x), int(y), val) == True:
            board[int(x)][int(y)] = val
        else:
            board[int(x)][int(y)] = 0
            error2()
        val = 0
    
    if error == 1:
        error1()
    if rs == 1:
        end_result()
    
    draw()
    if flag1 == 1:
        draw_box()
    display_instructions()

    # Update window
    pygame.display.update()

pygame.quit()