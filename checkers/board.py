from .constants import *
from .piece import Piece
import pygame

class Board:

    def __init__(self): # constructor
        self.board = []
        self.black_piece_count = self.white_piece_count = 12
        self.black_kings = self.white_kings = 0
        self.create_board() # create the board when we create Board object

    def create_board(self): # we create a matrix to put the pieces
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row % 2 == ((col +  1) % 2):
                    if row < 3: # white pieces
                        self.board[row].append(Piece(WHITE, row, col))
                    elif row > 4: # black pieces
                        self.board[row].append(Piece(BLACK, row, col))
                    else: # blank piece
                        self.board[row].append(0)
                else: # blank piece
                    self.board[row].append(0)

    def draw_the_board_squares(self, win): # draw the background of the board
        win.fill(BROWN) # initially we fill it with brown
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2): # start by drawing a CREAM SQUARE at column 0 then step by two colum 3 , column 5 , so on
                pygame.draw.rect(win, CREAM, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                # pygame starts drawing from top left so top left coordinates are (0,0)
                # pygame.draw.rect(where we will draw(win), color, (x ,y , width, height))

    def draw(self, win): # draw everything (piece, board)
        self.draw_the_board_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove_taken_pieces(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.team_color == WHITE:
                    self.white_piece_count -= 1
                else:
                    self.black_piece_count -= 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.team_color == color:
                    pieces.append(piece)

        return pieces

    def evaluate(self):
        return self.white_piece_count - self.black_piece_count + (self.white_kings * 0.5 - self.black_kings * 0.5)
       
    def move(self, piece, row , col): # moves a piece on the board
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col]
        piece.move(row, col)
        if row == 0 or row == ROWS - 1:
            piece.make_king()
            if piece.team_color == BLACK:
                self.black_kings += 1
            else:
                self.white_kings += 1

    def check_winner(self):
        if self.white_piece_count <= 0:
            return BLACK
        elif self.black_piece_count <= 0:
            return WHITE
        else:
            return None

    def determine_valid_moves_for_a_piece(self, piece):
        moves = {}
        row = piece.row  #6
        left = piece.col - 1 #4
        right = piece.col + 1 # left + 2

        if piece.team_color == BLACK or piece.king :#or piece.king
            moves.update(self.__traverse_NorthWest_SouthWest(row -1, max(row-3, -1), -1, piece.team_color, left, piece, False)) # up left
            moves.update(self.__traverse_NorthEast_SouthEast(row -1, max(row-3, -1), -1, piece.team_color, right, piece, False)) # up right
        if piece.team_color == WHITE or piece.king:# or piece.king
            moves.update(self.__traverse_NorthWest_SouthWest(row +1, min(row+3, ROWS), 1, piece.team_color, left, piece, False)) # down left
            moves.update(self.__traverse_NorthEast_SouthEast(row +1, min(row+3, ROWS), 1, piece.team_color, right, piece, False)) # down right

        return moves

    def __traverse_NorthWest_SouthWest(self, start, end, direction, color, left, piece, turned, jumped=[]):          
        moves = {} # (x,y) : [coordinates of taken pieces if we have any]
        # final position is (x,y)
        # let's say we start at (5,4) if we move upwards left diagonal we go to (4,3) but if there is a opposite color at (4,3) we jump over so we are at (3,2)
        # so in moves dict ; keys = final position (3,2), values = [(4,3),...] we could jump over more than one piece
        last_jumped = []
        for r in range(start, end, direction):# let's say our piece is at (6,5) then start = 5 , end = 3, direction = -1 so r = [5,4] , left = 4 
            if left < 0:                      # after recurse : start = 3, end = 1, left = 2, jumped = [board[5][4]]
                break                         ### start = 3, end = 1, left = 2, direction = reversed, jumped = [board[1][6], board[3][4]] --> r = [3,2]              
                                              ### r = 3, left = 2 ---- r = 2, left = 1  
            current = self.board[r][left] #  first loop => r = 5, left = 4 --- second loop => r = 4, left = 3
                                          # after recurse => first loop => r = 3 ,left = 2 --- second loop => r = 2, left = 1  
            # current = board[5][4] if there is no piece current = 0
            if current == 0: # if the position we want to move is empty
                
                if jumped and not last_jumped: 
                    break
                
                elif jumped:
                    moves[(r,left)] = jumped + last_jumped  # moves = {(2,1):[board[3][2], board[5][4]}
                                                           
                else:
                    moves[(r,left)] = last_jumped # moves = {(4,3):[board[5][4]]}

                if last_jumped:
                    if direction == 1: # down
                        row = min(r+3, ROWS)
                    else: # up
                        row = max(r-3, -1)
                    moves.update(self.__traverse_NorthWest_SouthWest(r + direction, row, direction, color, left-1, piece, False, jumped=last_jumped+jumped))# (3,1,-1,color,left=2,jumped=[board[5][4]])
                                                                                                                                       # (1,0,-1,left = 0,jumped=[board[3][2], board[5][4])
                    moves.update(self.__traverse_NorthEast_SouthEast(r + direction, row, direction, color, left+1, piece, False, jumped=last_jumped+jumped))# (1,-1,-1,color,right=2,jumped=[board[3][2], board[5][4])
                    
                    if piece.king and last_jumped and not turned:  
                        if direction == 1: # normally down but its opposite
                            row = max(r-3, -1)
                        else: # up
                            row = min(r+3, ROWS)
                        if piece.team_color == BLACK:
                            moves.update(self.__traverse_NorthWest_SouthWest(r - 1, row, -direction, color, left-1 , piece, True, jumped=last_jumped+jumped))                                                                                                                                 
                            moves.update(self.__traverse_NorthEast_SouthEast(r - 1, row, -direction, color, left+1, piece, True, jumped=last_jumped+jumped))
                        else:
                            moves.update(self.__traverse_NorthWest_SouthWest(r + 1, row, -direction, color, left-1 , piece, True, jumped=last_jumped+jumped))                                                                                                                                 
                            moves.update(self.__traverse_NorthEast_SouthEast(r + 1, row, -direction, color, left+1, piece, True, jumped=last_jumped+jumped))



                break
                    
            elif current.team_color == color: # if the pos we'll move to is already taken with a piece that is our color (can't jump)
                break

            else: # if opposite color technically we could jump over it
                last_jumped = [current] # last_jumped = [board[5][4]]  ,   last_jumped = [board[3][2]]

            left -= 1
        
        return moves

    def __traverse_NorthEast_SouthEast(self, start, end, direction, color, right, piece, turned, jumped=[]):
        # start = 1, end = -1, direction = -1, right = 2, jumped = [board[5][3],boad[3][1]]
        #(1,0,-1,color,right=2,jumped=[board[3][2], board[5][4])
        moves = {} 
        last_jumped = []  

        for r in range(start, end, direction): # r = 1, right = 2
            if right >=  COLS:
                break
            
            current = self.board[r][right] # first loop => board[1][2] --- second loop => board[0][3]
         
            if current == 0: # if the position we want to move is empty
               
                if jumped and not last_jumped: 
                    break
                
                elif jumped:
                    moves[(r,right)] = jumped + last_jumped # moves = (0,3) = [board[5][4],board[3][2],board[1][2]]
                else:
                    moves[(r,right)] = last_jumped 

                if last_jumped:
                    if direction == 1: # down
                        row = min(r+3, ROWS)
                    else: # up
                        row = max(r-3, -1) # -1
                    moves.update(self.__traverse_NorthWest_SouthWest(r + direction, row, direction, color, right-1, piece, False, jumped=last_jumped+jumped)) #(-1,-1)
                    moves.update(self.__traverse_NorthEast_SouthEast(r + direction, row, direction, color, right+1, piece, False, jumped=last_jumped+jumped)) # 
                    if piece.king and last_jumped and not turned:
                        if direction == 1: # normally down but its opposite
                            row = max(r-3, -1)
                        else: # up
                            row = min(r+3, ROWS)
                        if piece.team_color == BLACK:
                            moves.update(self.__traverse_NorthWest_SouthWest(r - 1, row, -direction, color, right-1 , piece, True, jumped=last_jumped+jumped))                                                                                                                                 
                            moves.update(self.__traverse_NorthEast_SouthEast(r - 1, row, -direction, color, right+1, piece, True, jumped=last_jumped+jumped))
                        else:
                            moves.update(self.__traverse_NorthWest_SouthWest(r + 1, row, -direction, color, right-1 , piece, True, jumped=last_jumped+jumped))                                                                                                                                 
                            moves.update(self.__traverse_NorthEast_SouthEast(r + 1, row, -direction, color, right+1, piece, True, jumped=last_jumped+jumped))
                break
                    
            elif current.team_color == color: # if the pos we'll move to is already taken with a piece that is our color (can't jump)
                break

            else:
                last_jumped = [current] # [board[1][2]]

            right += 1
        
        return moves
                        