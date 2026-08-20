import sys

import pygame

from platform import system

pygame.init()

screen_height = 600 

screen_width = 600

unit = 100 * 6 // 8

dark = (238, 238, 210)

light = (118, 150, 86)

green = (0, 255, 0)

yellow = (255, 255, 0)

screen = pygame.display.set_mode((screen_width, screen_height))

turn = "w"

check = None

pygame.display.set_caption("Chess")

os = system()

if os == "Linux":

    font = pygame.font.SysFont("dejavusans", unit - 10)

elif os == "Windows":

    font = pygame.font.SysFont("segoeuisymbol", unit - 10)

PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # white
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',  # black
}


all_legal_moves = None

def convert_into_pos(file, rank):

    return ((file - 1) * unit,((8 - rank) * unit))

def convert_into_pos_for_circles(file, rank):

    return ((file - 1) * unit + (unit/2), ((8 - rank) * unit) + (unit/2))

def convert_into_pos_for_pieces(file, rank):

    if os == "Windows":

        return ((file - 1) * unit + 6, ((8 - rank) * unit)-6)

    elif os == "Linux":

        return ((file - 1) * unit + 7, ((8 - rank) * unit)- 0)

def convert_into_file_rank(x, y):

    return ((x // unit) + 1, 8 - (y // unit))

def is_piece_on_square(file, rank):

    if any(piece.file == file and piece.rank == rank for piece in board):

        return True
    
    return False

def get_piece_on_square(file, rank):

    for piece in board:

        if piece.file == file and piece.rank == rank:

            return piece

def is_dangerous(file, rank):
    global all_legal_moves

    calculate_all_legal_moves()

    if (file, rank) in all_legal_moves or (file, rank, "capture") in all_legal_moves:

        return True


    return False

def is_check(colour_of_moved_piece):

    for piece in board:

        if piece.type == "king" and piece.colour != colour_of_moved_piece:

            king = piece

def calculate_all_legal_moves():
    global all_legal_moves

    all_legal_moves = []
            
    for piece in board:
            
        if piece.colour != turn:
            if piece.type != "king":
                piece.calculate_legal_moves()

                all_legal_moves.extend(piece.legal_moves)




class Piece:
    def __init__(self, file, rank, colour):

        self.file = file

        self.rank = rank

        self.colour = colour

        self.pos_x, self.pos_y = convert_into_pos(self.file,self.rank)

        self.legal_moves = []

    def move(self, new_file, new_rank):

        global turn

        if is_piece_on_square(new_file, new_rank):

            piece_to_remove = get_piece_on_square(new_file, new_rank)

            board.remove(piece_to_remove)

        self.file = new_file

        self.rank = new_rank

        all_legal_moves = []

        if self.colour == "w":

            turn = "b"
        else:
            
            turn = "w"

        for piece in board:
            
            piece.legal_moves = []

    def see_legal_moves(self):
        self.calculate_legal_moves()

        for legal_move in self.legal_moves:

            if "capture" in legal_move:

                pygame.draw.rect(screen, yellow, (*convert_into_pos(legal_move[0], legal_move[1]), unit, unit), 4)

            else:

                pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)

        

        self.pos_x, self.pos_y = convert_into_pos(self.file,self.rank)

class Pawn(Piece):

    def __init__(self, file, rank, colour):

        super().__init__(file, rank, colour)

        self.type = "pawn"

        if colour == "w":

            self.symbol = "P"

        else:

            self.symbol = "p"

        self.legal_moves = []

    def calculate_legal_moves(self):

        if len(self.legal_moves) == 0:
            
            # This part checks if the pawn can move forward one square or two squares (if it's on its starting rank)
            # and if there are no pieces blocking its path

            if self.colour == "w" and  is_piece_on_square(self.file, self.rank + 1) == False:
               
                if self.rank == 2:

                    if is_piece_on_square(self.file, self.rank + 2) == False:

                        self.legal_moves = [(self.file, self.rank + 1), (self.file, self.rank + 2)]
                    else:
                        self.legal_moves = [(self.file, self.rank + 1)]

                elif self.rank > 2:

                    self.legal_moves = [(self.file, self.rank + 1)]

            elif self.colour == "b" and is_piece_on_square(self.file, self.rank - 1) == False:

                if self.rank == 7:

                    if is_piece_on_square(self.file, self.rank - 2) == False:

                        self.legal_moves = [(self.file, self.rank - 1), (self.file, self.rank - 2)]
                    else:
                        self.legal_moves = [(self.file, self.rank - 1)]

                elif self.rank < 7:
                    self.legal_moves = [(self.file, self.rank - 1)]


            # This part checks if the pawn can capture an opponent's piece diagonally

            if self.colour == "w":

                if is_piece_on_square(self.file + 1, self.rank + 1) and get_piece_on_square(self.file + 1, self.rank + 1).colour == "b":

                    self.legal_moves.append((self.file + 1, self.rank + 1, "capture"))

                if is_piece_on_square(self.file - 1, self.rank + 1) and get_piece_on_square(self.file - 1, self.rank + 1).colour == "b":

                    self.legal_moves.append((self.file - 1, self.rank + 1, "capture"))
            elif self.colour == "b":

                if is_piece_on_square(self.file + 1, self.rank - 1) and get_piece_on_square(self.file + 1, self.rank - 1).colour == "w":

                    self.legal_moves.append((self.file + 1, self.rank - 1, "capture"))

                if is_piece_on_square(self.file - 1, self.rank - 1) and get_piece_on_square(self.file - 1, self.rank - 1).colour == "w":

                    self.legal_moves.append((self.file - 1, self.rank - 1, "capture"))

class Queen(Piece):
    def __init__(self, file, rank, colour):

        super().__init__(file, rank, colour)

        self.type = "queen"

        if colour == "w":

            self.symbol = "Q"

        else:

            self.symbol = "q"

        self.legal_moves = []

    def calculate_legal_moves(self):
        if len(self.legal_moves) == 0:

            # To the Right
            for i in range(self.file + 1, 9):
                if self.file + 1 < 9 and self.rank + 1 < 9:
                    if is_piece_on_square(i, self.rank):

                        if get_piece_on_square(i, self.rank).colour != self.colour:

                            self.legal_moves.append((i, self.rank, "capture"))
                        break
                    else:
                        self.legal_moves.append((i, self.rank))

            # To the Left

            for i in range(self.file - 1, 0, -1):

                if self.file - 1 > 0 and self.rank - 1 > 0:

                    if is_piece_on_square(i, self.rank):   

                        if get_piece_on_square(i, self.rank).colour != self.colour:

                            self.legal_moves.append((i, self.rank, "capture"))
                        break
                    else:
                        self.legal_moves.append((i, self.rank))

            # For Up
            for i in range(self.rank + 1, 9):

                if self.file + 1 < 9 and self.rank + 1 < 9:

                    if is_piece_on_square(self.file, i):

                        if get_piece_on_square(self.file, i).colour != self.colour:

                            self.legal_moves.append((self.file, i, "capture"))

                        break
                    else:
                        self.legal_moves.append((self.file, i))

            # For Down

            for i in range(self.rank - 1 , 0, -1):

                if self.file + 1 < 9 and self.rank - 1 > 0:

                    if is_piece_on_square(self.file, i):

                        if get_piece_on_square(self.file, i).colour != self.colour:

                            self.legal_moves.append((self.file, i, "capture"))

                        break
                    else:
                        self.legal_moves.append((self.file, i))

            # For Diagonal Moves To the Top right

            for i in range (1, 9):

                if self.file + i < 9 and self.rank + i < 9:

                    if is_piece_on_square(self.file + i, self.rank + i):

                        if get_piece_on_square(self.file + i, self.rank + i).colour != self.colour:
                        
                            self.legal_moves.append((self.file + i, self.rank + i, "capture"))
                        break
            
                    else:

                        self.legal_moves.append((self.file  + i, self.rank + i))

            # For the Diagonal Moves to the Top Left
            
            for i in range(1, 9):

                if is_piece_on_square(self.file - i, self.rank + i):

                    if get_piece_on_square(self.file - i, self.rank + i).colour != self.colour:

                        self.legal_moves.append((self.file - i, self.rank + i, "capture"))

                    break

                if self.file - i > 0 and self.rank + i < 9:

                    self.legal_moves.append((self.file - i, self.rank + i))

            # For Diagonal Moves to the bottom left

            for i in range(1, 9):

                if is_piece_on_square(self.file - i, self.rank - i):

                    if get_piece_on_square(self.file - i, self.rank - i).colour != self.colour:

                        self.legal_moves.append((self.file - i, self.rank - i, "capture"))
                    break

                if self.file - i > 0 and self.rank - i > 0:

                    self.legal_moves.append((self.file-i,self.rank - i))

            # For Diagonal Moves to the bottom right
            for i in range(1,9):

                if self.file + i < 9 and self.rank - i > 0:

                    if is_piece_on_square(self.file + i, self.rank - i):

                        if get_piece_on_square(self.file + i, self.rank - i).colour != self.colour:

                            self.legal_moves.append((self.file + i, self.rank - i, "capture"))
                        break


                    else:
                        self.legal_moves.append((self.file + i, self.rank - i))     

class Rook(Piece):

    def __init__(self, file, rank, colour):

        super().__init__(file, rank, colour)

        self.type = "rook"

        if colour == "w":

            self.symbol = "R"

        else:

            self.symbol = "r"

        self.legal_moves = []
    def calculate_legal_moves(self):
        if len(self.legal_moves) == 0:

           # To the Right
            for i in range(self.file + 1, 9):

                if is_piece_on_square(i, self.rank):

                    if get_piece_on_square(i, self.rank).colour != self.colour:

                        self.legal_moves.append((i, self.rank, "capture"))
                    break

                else:
                    self.legal_moves.append((i, self.rank))

            # To the Left

            for i in range(self.file - 1, 0, -1):

                if is_piece_on_square(i, self.rank):

                    if get_piece_on_square(i, self.rank).colour != self.colour:

                        self.legal_moves.append((i, self.rank, "capture"))
                    break
                else:
                    self.legal_moves.append((i, self.rank))

            # For Up
            for i in range(self.rank + 1, 9):

                if is_piece_on_square(self.file, i):

                    if get_piece_on_square(self.file, i).colour != self.colour:

                        self.legal_moves.append((self.file, i, "capture"))

                    break
                else:
                    self.legal_moves.append((self.file, i))

            # For Down

            for i in range(self.rank - 1 , 0, -1):

                if is_piece_on_square(self.file, i):

                    if get_piece_on_square(self.file, i).colour != self.colour:

                        self.legal_moves.append((self.file, i, "capture"))

                    break
                else:
                    self.legal_moves.append((self.file, i))
        
class Bishop(Piece):

    def __init__(self, file, rank, colour):

        super().__init__(file, rank, colour)

        self.type = "bishop"

        if colour == "w":

            self.symbol = "B"

        else:

            self.symbol = "b"

        self.legal_moves = []
    def calculate_legal_moves(self):
        if len(self.legal_moves) == 0:

            # For Diagonal Moves To the Top right

            for i in range (1, 9):

                if self.file + i < 9 and self.rank + i < 9:

                    if is_piece_on_square(self.file + i, self.rank + i):

                        if get_piece_on_square(self.file + i, self.rank + i).colour != self.colour:
                        
                            self.legal_moves.append((self.file + i, self.rank + i, "capture"))
                        break

                    else:
                        self.legal_moves.append((self.file  + i, self.rank + i))

            # For the Diagonal Moves to the Top Left
            
            for i in range(1, 9):

                if self.file - i > 0 and self.rank + i < 9:

                    if is_piece_on_square(self.file - i, self.rank + i):

                        if get_piece_on_square(self.file - i, self.rank + i).colour != self.colour:

                            self.legal_moves.append((self.file - i, self.rank + i, "capture"))

                        break


                    else:

                        self.legal_moves.append((self.file - i, self.rank + i))

            # For Diagonal Moves to the bottom left

            for i in range(1, 9):
                
                if self.file - i > 0 and self.rank - i > 0:

                    if is_piece_on_square(self.file - i, self.rank - i):

                        if get_piece_on_square(self.file - i, self.rank - i).colour != self.colour:

                            self.legal_moves.append((self.file - i, self.rank - i, "capture"))

                        break

                    else:
                        self.legal_moves.append((self.file-i,self.rank - i))

            # For Diagonal Moves to the bottom right
            for i in range(1,9):

                if is_piece_on_square(self.file + i, self.rank - i):

                    if get_piece_on_square(self.file + i, self.rank - i).colour != self.colour:

                        self.legal_moves.append((self.file + i, self.rank - i, "capture"))
                    break

                if self.file + i < 9 and self.rank - i > 0:

                    self.legal_moves.append((self.file + i, self.rank - i))   

        for legal_move in self.legal_moves:

            if "capture" in legal_move:

                pygame.draw.rect(screen, yellow, (*convert_into_pos(legal_move[0], legal_move[1]), unit, unit), 4)

            else:

                pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)

class Knight(Piece):
    def __init__(self, file, rank, colour):

        if colour == "w":

            self.symbol = "N"

        else:

            self.symbol = "n"

        super().__init__(file, rank, colour)

        self.type = "knight"

        self.legal_moves = []

    def calculate_legal_moves(self):
        
        if len(self.legal_moves) == 0:
        
            # Go 1 square to the right and 2 squares above
            if self.file + 1 < 9 and self.rank + 2 < 9:

                if is_piece_on_square(self.file + 1, self.rank + 2):

                    if not self.colour == get_piece_on_square(self.file + 1, self.rank + 2).colour:

                        self.legal_moves.append((self.file + 1, self.rank + 2, "capture")) 
                else:

                    self.legal_moves.append((self.file + 1, self.rank + 2))

            # Go 1 square to the left and 2 squares above
            if self.file - 1 > 0 and self.rank + 2 < 9:

                if is_piece_on_square(self.file - 1, self.rank + 2):

                    if not self.colour == get_piece_on_square(self.file - 1, self.rank + 2).colour:

                        self.legal_moves.append((self.file - 1, self.rank + 2, "capture"))

                else:
                    self.legal_moves.append((self.file - 1, self.rank + 2))

            # Go 2 squares to the right and 1 square above
            if self.file + 2 < 9 and self.rank + 1 < 9:

                if is_piece_on_square(self.file + 2, self.rank + 1):

                    if not self.colour == get_piece_on_square(self.file + 2, self.rank + 1).colour:

                        self.legal_moves.append((self.file + 2, self.rank + 1, "capture"))

                else:

                    self.legal_moves.append((self.file + 2, self.rank + 1))


            # Go 2 squares to the left and 1 square above
            if self.file - 2 > 0 and self.rank + 1 < 9:

                if is_piece_on_square(self.file - 2, self.rank + 1):

                    if not self.colour == get_piece_on_square(self.file - 2, self.rank + 1).colour:

                        self.legal_moves.append((self.file - 2, self.rank + 1, "capture"))
                else:
                    self.legal_moves.append((self.file - 2, self.rank + 1, ))

            # Go 2 squares to the right and 1 square below
            if self.file + 2 < 9 and self.rank - 1 > 0:

                if is_piece_on_square(self.file + 2, self.rank - 1):

                    if not self.colour == get_piece_on_square(self.file + 2, self.rank - 1).colour:

                        self.legal_moves.append((self.file + 2, self.rank - 1, "capture"))

                else:

                    self.legal_moves.append((self.file + 2, self.rank - 1))

            # Go 2 squares to the left and 1 square below
            if self.file - 2 > 0 and self.rank - 1 > 0:

                if is_piece_on_square(self.file - 2, self.rank - 1):

                    if not self.colour == get_piece_on_square(self.file - 2, self.rank - 1).colour:

                        self.legal_moves.append((self.file - 2, self.rank - 1, "capture"))
                else:

                    self.legal_moves.append((self.file - 2, self.rank - 1))


            # Go 1 squares to the right and 2 squares below
            if self.file + 1 < 9 and self.rank - 2 > 0:

                if is_piece_on_square(self.file + 1, self.rank - 2):

                    if not self.colour == get_piece_on_square(self.file + 1, self.rank - 2).colour:

                        self.legal_moves.append((self.file + 1, self.rank - 2, "capture"))
                else:

                    self.legal_moves.append((self.file + 1, self.rank - 2))


            # Go 1 squares to the left and 2 squares below
            if self.file - 1 > 0 and self.rank - 2 > 0:

                if is_piece_on_square(self.file - 1, self.rank - 2):

                    if not self.colour == get_piece_on_square(self.file - 1, self.rank - 2).colour:

                        self.legal_moves.append((self.file - 1, self.rank - 2, "capture"))
                else:
                    self.legal_moves.append((self.file - 1, self.rank - 2))

class King(Piece):

    def __init__(self, file, rank, colour):

        super().__init__(file, rank, colour)

        self.type = "king"

        if colour == "w":

            self.symbol = "K"
        else:

            self.symbol = "k"

        self.legal_moves = []

    def calculate_legal_moves(self):

        if len(self.legal_moves) == 0:
            # To the Top right
            if self.file + 1 < 9 and self.rank + 1 < 9:
                # if not is_dangerous(self.file + 1, self.rank + 1):
                        
                    if is_piece_on_square(self.file + 1, self.rank + 1):

                        if not self.colour == get_piece_on_square(self.file + 1, self.rank + 1).colour:

                            self.legal_moves.append((self.file + 1, self.rank + 1, "capture"))

                    else:
                        self.legal_moves.append((self.file + 1, self.rank + 1))
            # To the bottom right
            if self.file + 1 < 9 and self.rank - 1 > 0:
                # if not is_dangerous(self.file + 1, self.rank - 1):
                    if is_piece_on_square(self.file + 1, self.rank - 1):

                        if not self.colour == get_piece_on_square(self.file + 1, self.rank - 1).colour:

                            self.legal_moves.append((self.file + 1, self.rank - 1, "capture"))

                    else:
                        self.legal_moves.append((self.file + 1, self.rank - 1))

            # To the Right
            if self.file + 1 < 9:

                # if not is_dangerous(self.file + 1, self.rank):

                    if is_piece_on_square(self.file + 1, self.rank):

                        if not self.colour == get_piece_on_square(self.file + 1, self.rank).colour:

                            self.legal_moves.append((self.file + 1, self.rank, "capture"))

                    else:
                        self.legal_moves.append((self.file + 1, self.rank))

            # To the Top Left

            if self.file - 1 > 0 and self.rank + 1 < 9:

                # if not is_dangerous(self.file - 1, self.rank + 1):

                    if is_piece_on_square(self.file - 1, self.rank + 1):

                        if not self.colour == get_piece_on_square(self.file - 1, self.rank + 1).colour:

                            self.legal_moves.append((self.file - 1, self.rank + 1, "capture"))

                    else:
                        self.legal_moves.append((self.file - 1, self.rank + 1))

            # To the Bottom Left
            if self.file - 1 > 0 and self.rank - 1 > 0:

                # if not is_dangerous(self.file - 1, self.rank - 1):

                    if is_piece_on_square(self.file - 1, self.rank - 1):

                        if not self.colour == get_piece_on_square(self.file - 1, self.rank - 1).colour:

                            self.legal_moves.append((self.file - 1, self.rank - 1, "capture"))
                    else:
                        self.legal_moves.append((self.file - 1, self.rank - 1))
            # To the Left
            if self.file - 1 > 0:

                # if not is_dangerous(self.file - 1, self.rank):

                    if is_piece_on_square(self.file - 1, self.rank):

                        if not self.colour == get_piece_on_square(self.file - 1, self.rank).colour:

                            self.legal_moves.append((self.file - 1, self.rank, "capture"))

                    else:

                        self.legal_moves.append((self.file - 1, self.rank))

            # To the Bottom
            if self.rank - 1 > 0:

                # if not is_dangerous(self.file, self.rank - 1):

                    if is_piece_on_square(self.file, self.rank - 1):

                        if not self.colour == get_piece_on_square(self.file, self.rank - 1).colour:

                            self.legal_moves.append((self.file, self.rank - 1, "capture"))
                    else:
                        self.legal_moves.append((self.file, self.rank - 1))

            # To the Top
            if self.rank + 1 < 9:

                # if not is_dangerous(self.file, self.rank + 1):

                    if is_piece_on_square(self.file, self.rank + 1):

                        if not self.colour == get_piece_on_square(self.file, self.rank + 1).colour:

                            self.legal_moves.append((self.file, self.rank + 1, "capture"))
                    else:
                        self.legal_moves.append((self.file, self.rank + 1))



board = [(Rook(1, 1, "w")), (Knight(2, 1, "w")), (Bishop(3, 1, "w")), (Queen(4, 1, "w")), (King(5, 1, "w")), (Bishop(6, 1, "w")), (Knight(7, 1, "w")), (Rook(8, 1, "w")),

         (Pawn(1, 2, "w")), (Pawn(2, 2, "w")), (Pawn(3, 2, "w")), (Pawn(4, 2, "w")), (Pawn(5, 2, "w")), (Pawn(6, 2, "w")), (Pawn(7, 2, "w")), (Pawn(8, 2, "w")),

         (Pawn(1, 7, "b")), (Pawn(2, 7, "b")), (Pawn(3, 7, "b")), (Pawn(4, 7, "b")), (Pawn(5, 7, "b")), (Pawn(6, 7, "b")), (Pawn(7, 7, "b")), (Pawn(8, 7, "b")),

         (Rook(1, 8, "b")), (Knight(2, 8, "b")), (Bishop(3, 8, "b")), (Queen(4, 8, "b")), (King(5, 8, "b")), (Bishop(6, 8, "b")), (Knight(7, 8, "b")), (Rook(8, 8, "b"))]


class ChessGame:
    def __init__(self):

        self.selected_piece = None

    def check_where_clicked(self, event):
        changed = False
        click_square = convert_into_file_rank(*event.pos)

        for piece in board:

            if (piece.file, piece.rank)== click_square and piece.colour == turn:

                if not self.selected_piece == piece:

                    changed = True

                self.selected_piece = piece
            if piece == board[-1] and not changed:
                    # This if block check if the selected piece has legal moves on the selected
                    # square and if it does, it moves the piece to that square


                if self.selected_piece is not None:
                            
                        if (click_square in self.selected_piece.legal_moves) or ((*click_square, "capture") in self.selected_piece.legal_moves):
                    
                            self.selected_piece.move(*click_square)
                    
                            self.selected_piece.legal_moves = []
                    
                            self.selected_piece = None

                # If the clicked square is literally empty, it deselects the selected piece

                self.selected_piece = None


    def draw_piece(self, piece, file, rank):

        text_surface = font.render(PIECE_SYMBOLS[piece], True, (0,0,0))
                   
        screen.blit(text_surface, convert_into_pos_for_pieces(file, rank))
        
    def draw_board(self):

        first_light = False
        
        for y in range(0,8):
            if first_light:
                for x in range(0,8,2):
                    pygame.draw.rect(screen, light, (x * unit, y * unit, unit, unit))

                for x in range(1,8,2):
                    pygame.draw.rect(screen, dark, (x * unit, y * unit, unit, unit))

            else:
                for x in range(0,8,2):
                    pygame.draw.rect(screen, dark, (x * unit, y * unit, unit, unit))

                for x in range(1,8,2):
                    pygame.draw.rect(screen, light, (x * unit, y * unit, unit, unit))


            first_light = not first_light

        for piece in board:

            self.draw_piece(piece.symbol, piece.file, piece.rank)
            

    def run(self):
        running = True
        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running= False
                    
                elif event.type == pygame.MOUSEBUTTONDOWN:
            
                    self.check_where_clicked(event)

            self.draw_board()

            if self.selected_piece is not None:

                if self.selected_piece.colour == turn:

                    self.selected_piece.see_legal_moves()

            pygame.display.flip()


chess_game = ChessGame()

chess_game.run()

pygame.quit()

sys.exit()


