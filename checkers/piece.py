from .constants import *
import pygame


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, team_color, row, col):
        self.row = row
        self.col = col
        self.team_color = team_color
        self.king = False # if the piece is king
        self.x = 0
        self.y = 0
        self.calculate_position()
    
    def __repr__(self):
        return str(self.team_color)

    def calculate_position(self):
        self.x = (SQUARE_SIZE * self.col) + (SQUARE_SIZE // 2)
        self.y = (SQUARE_SIZE * self.row) + (SQUARE_SIZE // 2)


    def draw(self, win): # draw a circular piece
        r = SQUARE_SIZE // 2 - self.PADDING # radius
        pygame.draw.circle(win, GREY, (self.x, self.y), r + self.OUTLINE) # circle outline. First we draw a circle with radius = radius + outline 
        pygame.draw.circle(win, self.team_color, (self.x, self.y), r) # After we draw the first circle we draw a smaller circle on top of that with radius = radius
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2)) # win.blit = put some image onto the screen


    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_position()


    def make_king(self):
        self.king = True

    