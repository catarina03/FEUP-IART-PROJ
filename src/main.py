import pygame
import pygame_menu
import time
from constants import WHITE_PIECE, BLACK_PIECE
from copy import deepcopy
import sys
sys.setrecursionlimit(1000)
pygame.init()

from constants import WIDTH, HEIGHT, SQUARE_SIZE
from classes.game import Game

FPS = 60

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Neutreeko')
settings = "pvp"
diff_pvc = None
diff_cvc_1 = None
diff_cvc_2 = None
mode = 1


def set_difficulty(value, difficulty):
    global diff_pvc
    diff_pvc = difficulty

def set_difficulty_PC1(value, difficulty):
    global diff_cvc_1
    diff_cvc_1 = difficulty

def set_difficulty_PC2(value, difficulty):
    global diff_cvc_2
    diff_cvc_2 = difficulty

def set_gamemode(value, gamemode):
    global settings
    global mode
    menu.remove_widget(quit_button)
    if gamemode == 1 and settings == "pvc":
        settings = "pvp"
        mode = 1
        menu.remove_widget(difficulty_selector)
    elif gamemode == 1 and settings == "cvc":
        settings = "pvp"
        mode = 1
        menu.remove_widget(difficulty_selector_PC1)
        menu.remove_widget(difficulty_selector_PC2)
    elif gamemode == 2 and settings == "pvp":
        mode = 2
        settings = "pvc"
        menu.add_generic_widget(difficulty_selector)
    elif gamemode == 2 and settings == "cvc":
        settings = "pvc"
        mode = 2
        menu.add_generic_widget(difficulty_selector)
        menu.remove_widget(difficulty_selector_PC1)
        menu.remove_widget(difficulty_selector_PC2)
    elif gamemode == 3 and settings == "pvp":
        settings = "cvc"
        mode = 3
        menu.add_generic_widget(difficulty_selector_PC1)
        menu.add_generic_widget(difficulty_selector_PC2)
    elif  gamemode == 3 and settings == "pvc":
        settings = "cvc"
        mode = 3
        menu.remove_widget(difficulty_selector)
        menu.add_generic_widget(difficulty_selector_PC1)
        menu.add_generic_widget(difficulty_selector_PC2)

    menu.add_generic_widget(quit_button)


def plaverVSPlayer():
    run = True
    finished = False
    game = Game(WINDOW, 1)
    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not finished:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x <= 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row,col)
                    if game.checkWin() != -1:
                        finished = True
                
    
        game.update()
    
   


def pcVSPc():
    global diff_cvc_1
    global diff_cvc_2
    run = True
    game = Game(WINDOW, 3)
    firstMove = True
    finished = False

    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x > 800 and game.getPlayer() == 1:
                    if not firstMove:
                        row, col = game.getLastMove()
                    else:
                        row = 0
                        col = 0
                    (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, 6, -2000, 2000, 2)
                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                elif x > 800 and game.getPlayer() == 2:
                    row, col = game.getLastMove()
                    (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, 6, -2000, 2000, 1)
                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                
    
        game.update()
    pass


#Not working properly
def playerVSPc():
    global diff_pvc
    run = True

    game = Game(WINDOW, 2)
    pcTurn = False
    finished = False

    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN and finished:
                    run = False
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = pos
                if x <= 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row,col)
                    if game.checkWin() != -1:
                        finished = True
                
                elif x > 800 and game.getPlayer() == 2:
                    row, col = game.getLastMove()
                    (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, 6, -2000, 2000, 1)
                    game.selected = oldRow, oldCol
                    game.ai_move(finalRow, finalCol)
                    if game.checkWin() != -1:
                        finished = True
                
                

        game.update()


def start_the_game():
    global diff_pvc
    global diff_cvc_1
    global diff_cvc_2
    global mode
    
    if mode == 1:
        plaverVSPlayer()
    elif mode == 2:
        playerVSPc()
    elif mode == 3:
        pcVSPc()


def get_row_col_from_mouse(pos):
    x,y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE

    return row,col


def main():
    run = True

    menu.mainloop(WINDOW)
    
    #clock = pygame.time.Clock()
    #board = Board()
    '''game = Game(WINDOW)
    
    while run:
        #clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row,col)
                game.update()
                continue
                if game.checkWin() != -1:
                    print("Vitória")

        if game.getPlayer() == 2:
            row, col = game.getLastMove()
            (m, oldRow , oldCol , finalRow, finalCol) = game.max(row, col, 6, -2000, 2000)
            game.selected = oldRow, oldCol
            game.ai_move(finalRow, finalCol)

        
        if game.checkWin():
            print("Vitória")
            run = False

        game.update()'''
        
    
    pygame.quit()


mytheme = pygame_menu.themes.THEME_DEFAULT.copy()

myimage = pygame_menu.baseimage.BaseImage(image_path='assets/bg.png', drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)

mytheme.background_color = myimage
mytheme.widget_font = pygame_menu.font.FONT_NEVIS
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
mytheme.title_background_color = (76,188,228, 100)
mytheme.title_font_size = 70
mytheme.title_font_color = (250,250,250)
mytheme.title_font = pygame_menu.font.FONT_NEVIS
mytheme.widget_font_size = 45
mytheme.widget_margin = (0,30)
mytheme.widget_padding = 10

menu = pygame_menu.Menu(HEIGHT, WIDTH, 'NEUTREEKO', theme=mytheme)
menu.add.button('Play', start_the_game)
menu.add.selector('Game Mode ', [('Player vs Player', 1), ('Player vs Computer', 2), ('Computer vs Computer', 3)], onchange=set_gamemode)
difficulty_selector = menu.add.selector('Computer Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3), ('Impossible', 4)], onchange=set_difficulty)
difficulty_selector_PC1 = menu.add.selector('Computer 1 (Black) Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3), ('Impossible', 4)], onchange=set_difficulty_PC1)
difficulty_selector_PC2 = menu.add.selector('Computer 2 (White) Difficulty :', [('Easy', 1), ('Medium', 2), ('Hard', 3), ('Impossible', 4)], onchange=set_difficulty_PC2)
menu.remove_widget(difficulty_selector)
menu.remove_widget(difficulty_selector_PC1)
menu.remove_widget(difficulty_selector_PC2)
quit_button = menu.add.button('Quit', pygame_menu.events.EXIT)


if __name__ == "__main__":
    main()