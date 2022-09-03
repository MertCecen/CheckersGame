import pygame
from checkers.game import Game
#import time
from checkers.constants import *
from algoritma.minimax import minimax


pygame.init()
FPS = 60
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
font = pygame.font.Font('freesansbold.ttf', 32)
text_black = font.render('BLACK WON', True, GREEN, BLUE)
textRect = text_black.get_rect()
text_white = font.render('WHITE WON', True, GREEN, BLUE)
textRect = text_white.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 2)

def get_the_coordinates_of_the_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WINDOW)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 4, WHITE, game)
            game.computer_play(new_board)

        if game.get_winner() != None:
            print(game.get_winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_the_coordinates_of_the_mouse(pos)
                game.select_piece(row, col)

        game.update_the_game()
        
    
    pygame.quit()

main()