import sys

import pygame

pygame.init()

screen_height = 600 

screen_width = 600

unit = 100 * 6 // 8

dark = (238, 238, 210)

light = (118, 150, 86)

green = (0, 255, 0)

screen = pygame.display.set_mode((screen_width, screen_height))

turn = "white"

pygame.display.set_caption("Chess")

font = pygame.font.SysFont("segoeuisymbol", unit - 10)

PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # white
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',  # black
}

board = [(Rook(1, 1)), (Knight(2, 1)), (Bishop(3, 1)), (Queen(4, 1)), (King(5, 1)), (Bishop(6, 1)), (Knight(7, 1)), (Rook(8, 1)),

         (Pawn(1, 2)), (Pawn(2, 2)), (Pawn(3, 2)), (Pawn(4, 2)), (Pawn(5, 2)), (Pawn(6, 2)), (Pawn(7, 2)), (Pawn(8, 2)),

         (Pawn(1, 7)), (Pawn(2, 7)), (Pawn(3, 7)), (Pawn(4, 7)), (Pawn(5, 7)), (Pawn(6, 7)), (Pawn(7, 7)), (Pawn(8, 7)),

         (Rook(1, 8)), (Knight(2, 8)), (Bishop(3, 8)), (Queen(4, 8)), (King(5, 8)), (Bishop(6, 8)), (Knight(7, 8)), (Rook(8, 8))]

def convert_into_pos(file, rank):

    return ((file - 1) * unit,((8 - rank) * unit))

def convert_into_pos_for_circles(file, rank):

    return ((file - 1) * unit + (unit/2), ((8 - rank) * unit) + (unit/2))

def convert_into_pos_for_pieces(file, rank):

    return ((file - 1) * unit + 4, ((8 - rank) * unit)-2)



class ChessGame:
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
            self.draw_piece(*piece)
            

    def run(self):
        running = True
        while running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running= False

            
            screen.fill((255, 0, 0))

            self.draw_board()

            self.draw_piece("K", 5, 1)

            pygame.display.flip()

class Piece:
    def __init__(self, file, rank):

        self.file = file

        self.rank = rank

        self.pos_x, self.pos_y = convert_into_pos(self.file,self.rank)

        
class Pawn(Piece):

    def __init__(self, file, rank):
        self.symbol = "p"
        super().__init__(file, rank)

    def see_legal_moves(self):

        if self.rank == 2:

            legal_moves = [(self.file, self.rank + 1), (self.file, self.rank + 2)]

        elif self.rank > 2:
            legal_moves = [(self.file, self.rank + 1)]

        for legal_move in legal_moves:
            
            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)
class Queen(Piece):
    def __init__(self, file, rank):

        self.symbol = "q"

        super().__init__(file, rank)

    legal_moves = []

    def see_legal_moves(self):
        if len(self.legal_moves) == 0:

            # To the Right
            for i in range(self.file + 1, 9):

                self.legal_moves.append((i, self.rank))

            # To the Left

            for i in range(self.file - 1, 0, -1):

                self.legal_moves.append((i, self.rank))

            # For Up
            for i in range(self.rank + 1, 9):

                self.legal_moves.append((self.file, i))

            # For Down

            for i in range(self.rank - 1 , 0, -1):

                self.legal_moves.append((self.file, i))

            # For Diagonal Moves To the Top right

            for i in range (1, 9):
                
                self.legal_moves.append((self.file  + i, self.rank + i))

            # For the Diagonal Moves to the Top Left
            
            for i in range(1, 9):

                self.legal_moves.append((self.file - i, self.rank + i))

            # For Diagonal Moves to the bottom left

            for i in range(1, 9):

                self.legal_moves.append((self.file-i,self.rank - i))

            # For Diagonal Moves to the bottom right
            for i in range(1,9):

                self.legal_moves.append((self.file + i,self.rank - i))
            

            print(self.legal_moves)



        for legal_move in self.legal_moves:

            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)



class Rook(Piece):
    def __init__(self, file, rank):

        self.symbol = "r"

        super().__init__(file, rank)

    legal_moves = []
    def see_legal_moves(self):
        if len(self.legal_moves) == 0:

            # To the Right
            for i in range(self.file + 1, 9):

                self.legal_moves.append((i, self.rank))

            # To the Left

            for i in range(self.file - 1, 0, -1):

                self.legal_moves.append((i, self.rank))

            # For Up
            for i in range(self.rank + 1, 9):

                self.legal_moves.append((self.file, i))

            # For Down

            for i in range(self.rank - 1 , 0, -1):

                self.legal_moves.append((self.file, i))


        
        for legal_move in self.legal_moves:

            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)

class Bishop(Piece):

    def __init__(self, file, rank):
        
        self.symbol = "b"

        super().__init__(file, rank)

    legal_moves = []
    def see_legal_moves(self):
        if len(self.legal_moves) == 0:

            # For Diagonal Moves To the Top right

            for i in range (1, 9):
                
                self.legal_moves.append((self.file  + i, self.rank + i))

            # For the Diagonal Moves to the Top Left
            
            for i in range(1, 9):

                self.legal_moves.append((self.file - i, self.rank + i))

            # For Diagonal Moves to the bottom left

            for i in range(1, 9):

                self.legal_moves.append((self.file-i,self.rank - i))

            # For Diagonal Moves to the bottom right
            for i in range(1,9):

                self.legal_moves.append((self.file + i,self.rank - i))
            

            print(self.legal_moves)

        for legal_move in self.legal_moves:

            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10) 
class Knight(Piece):
    def __init__(self, file, rank):

        self.symbol = "n"

        super().__init__(file, rank)
    
    legal_moves = []

    def see_legal_moves(self):
        
        if len(self.legal_moves) == 0:
            # Go 1 square to the right and 2 squares above
            self.legal_moves.append((self.file + 1, self.rank + 2))

            # Go 1 square to the left and 2 squares above
            self.legal_moves.append((self.file - 1, self.rank + 2))

            # Go 2 squares to the right and 1 square above
            self.legal_moves.append((self.file + 2, self.rank + 1))

            # Go 2 squares to the left and 1 square above
            self.legal_moves.append((self.file - 2, self.rank + 1))

            # Go 2 squares to the right and 1 square below
            self.legal_moves.append((self.file + 2, self.rank - 1))

            # Go 2 squares to the left and 1 square below
            self.legal_moves.append((self.file - 2, self.rank - 1))

            # Go 1 squares to the right and 2 squares below
            self.legal_moves.append((self.file + 1, self.rank - 2))

            # Go 1 squares to the left and 2 squares below
            self.legal_moves.append((self.file - 1, self.rank - 2))

        for legal_move in self.legal_moves:
            
            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_move[0], legal_move[1]), 10)

class King(Piece):

    def __init__(self, file, rank):

        self.symbol = "k"

        super().__init__(file, rank)

    legal_moves = []
    
    def see_legal_moves(self):

        if len(self.legal_moves) == 0:

            self.legal_moves.append((self.file + 1, self.rank + 1))

            self.legal_moves.append((self.file + 1, self.rank - 1))

            self.legal_moves.append((self.file + 1, self.rank))

            self.legal_moves.append((self.file - 1, self.rank + 1))

            self.legal_moves.append((self.file - 1, self.rank - 1))

            self.legal_moves.append((self.file - 1, self.rank))

            self.legal_moves.append((self.file, self.rank + 1))

            self.legal_moves.append((self.file, self.rank - 1))

        for legal_moves in self.legal_moves:
            pygame.draw.circle(screen, green, convert_into_pos_for_circles(legal_moves[0], legal_moves[1]), 10)




queen = Queen(4, 5)

rook = Rook(4,5)

bishop = Bishop(4, 5)

knight = Knight(4, 6)

king = King(8, 7)

chess_game = ChessGame()

chess_game.run()

pygame.quit()

sys.exit()


