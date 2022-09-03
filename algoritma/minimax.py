from checkers.game import Game
from checkers.board import Board
from copy import deepcopy
import pygame
from checkers.constants import *
"""
function minimax(node, depth, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (* minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value
"""
def simulate_move(piece, move, board: Board, game, jumped):
    board.move(piece, move[0], move[1])
    if jumped:
        board.remove_taken_pieces(jumped)

    return board


def get_all_moves(board: Board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.determine_valid_moves_for_a_piece(piece)
        for move, jumped in valid_moves.items():
            draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            newBoard = simulate_move(temp_piece, move, temp_board, game, jumped)
            moves.append(newBoard)

    return moves


def draw_moves(game: Game, board: Board, piece):
    valid_moves = board.determine_valid_moves_for_a_piece(piece)
    board.draw(game.window)
    pygame.draw.circle(game.window, GREEN, (piece.x, piece.y), 38, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()


def minimax(pos, depth, maximizing_player, game):
    if depth == 0 or pos.check_winner() != None:
        return pos.evaluate(), pos
    
    if maximizing_player:
        max_val = float("-Inf")
        best_move = None
        for move in get_all_moves(pos, WHITE, game):
            value =  minimax(move, depth-1, False, game)[0]
            max_val = max(max_val, value)
            if max_val == value:
                best_move = move

        return max_val, best_move
    
    else:
        min_val = float("Inf")
        best_move = None
        for move in get_all_moves(pos, BLACK, game):
            value = minimax(move, depth-1, True, game)[0]
            min_val = min(min_val, value)
            if min_val == value:
                best_move = move
        
        return min_val, best_move
    
        





