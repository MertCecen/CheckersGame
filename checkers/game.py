import pygame
from .constants import *
from checkers.board import Board

class Game:

    def __init__(self, window):
        self.__reset()
        self.window = window
    
    def update_the_game(self):
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def __reset(self):
        self.selected = None
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}

    def reset_the_game(self):
        self.__reset()

    def get_board(self):
        return self.board

    def opposite_side_play(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def draw_valid_moves(self, valid_moves):
        for move in valid_moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, ((SQUARE_SIZE//2) + (col * SQUARE_SIZE), (SQUARE_SIZE//2) + (row * SQUARE_SIZE)), 15)

    def __move_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            jumped_over = self.valid_moves[(row, col)]
            if jumped_over:
                self.board.remove_taken_pieces(jumped_over)
            self.opposite_side_play()
        else:
            return False

        return True

    def select_piece(self, row, col):
        if self.selected:
            moved = self.__move_piece(row, col)
            if not moved:
                self.selected = None
                self.select_piece(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.team_color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.determine_valid_moves_for_a_piece(piece)
            return True

        return False

    def get_winner(self):
        return self.board.check_winner()

    def computer_play(self, board):
        self.board = board
        self.opposite_side_play()