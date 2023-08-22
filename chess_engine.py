import numpy as np
from piece_factory import PieceFactory

piece_value = {
    'Q': 10,
    'R': 5,
    'B': 3.5,
    'N': 3.5,
    'P': 1,
    'K':0
}

class Engine:
    def __init__(self):
        self.board = np.array([
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['  ','  ','  ','  ','  ','  ','  ','  '],
            ['  ','  ','  ','  ','  ','  ','  ','  '],
            ['  ','  ','  ','  ','  ','  ','  ','  '],
            ['  ','  ','  ','  ','  ','  ','  ','  '],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR']
        ])
        self.white_to_move = True
        self.move_log = []
        self.ROWS = len(self.board)
        self.COLS = len(self.board[0])
        self.white_king_loc = [7,4]
        self.black_king_loc = [0,4]
        self.piece_factory = PieceFactory()
        self.checkmate = False
        self.stalemate = False
        self.score = 0

    def make_move(self,move):
        self.board[move.start_r][move.start_c] = "  "
        self.board[move.end_r][move.end_c] = move.piece_moved
        self.move_log.append(move)
        self.white_to_move = not (self.white_to_move)
        if move.piece_moved == 'wK':
            self.white_king_loc = [move.end_r,move.end_c]
        elif move.piece_moved == 'bK':
            self.black_king_loc = [move.end_r,move.end_c]

        if move.is_pawn_promo:
            self.board[move.end_r][move.end_c] = move.piece_moved[0] + 'Q'



    def print_move(self,move):
        print('\n')
        if self.white_to_move:
            print(f"White moves {move.piece_moved}: ({move.start_r},{move.start_c}) --> ({move.end_r},{move.end_c})")
        else:
            print(f"Black moves {move.piece_moved}: ({move.start_r},{move.start_c}) --> ({move.end_r},{move.end_c})")

        if move.captured_piece != "  ":
            print(f"{move.captured_piece} is captured")



    def undo_last_move(self):
        if not self.move_log:
            return
        move = self.move_log.pop()
        self.board[move.start_r][move.start_c] = move.piece_moved
        self.board[move.end_r][move.end_c] = move.captured_piece
        self.white_to_move = not(self.white_to_move)

        if move.piece_moved == 'wK':
            self.white_king_loc = [move.start_r,move.start_c]
        elif move.piece_moved == 'bK':
            self.black_king_loc = [move.start_r,move.start_c]


    def get_possible_moves(self):
        moves = []
        p,x,y = self.get_king()
        # Getting all the pins in the game
        king_piece = self.piece_factory.create_piece('K',p,x,y,self.board,False)
        pins = king_piece.get_pins()
        pin_dir_dict = {}
        for t,dir in pins:
            pin_dir_dict[t] = dir

        self.score = 0

        # Going through all the pieces on the board
        for r in range(self.ROWS):
            for c in range(self.COLS):
                player = self.board[r][c][0]
                if (player == 'w' and self.white_to_move) or (player == 'b' and not self.white_to_move):
                    piece_str = self.board[r][c][1]
                    piece = self.piece_factory.create_piece(piece_str,player,r,c,self.board, pin_dir_dict.get((r,c), False))
                    [piece_moves,piece_score] = piece.get_possible_moves()
                    self.score += (piece_score + piece_value[piece_str])
                    moves.extend(piece_moves)
        return moves
    

    
    def get_king(self):
        if self.white_to_move:
            return ['w'] + self.white_king_loc
        else:
            return ['b'] + self.black_king_loc



    def get_valid_moves(self):
        moves = self.get_possible_moves()
        p,x,y = self.get_king()
        king_piece = self.piece_factory.create_piece('K',p,x,y,self.board,False)
        num_check = king_piece.in_check_pos(x,y)

        if not moves and num_check:
            self.checkmate = True
        if not moves and not num_check:
            self.stalemate = True


        if num_check == 0:
            return [moves,num_check]
        elif num_check > 1:
            return [king_piece.get_possible_moves(), num_check]

        for i in range(len(moves)-1,-1,-1):
            self.make_move(moves[i])
            self.white_to_move = not(self.white_to_move)
            p,x,y = self.get_king()
            king_piece = self.piece_factory.create_piece('K',p,x,y,self.board,False)
            if king_piece.in_check_pos(x,y):
                moves.remove(moves[i])
            self.undo_last_move()
            self.white_to_move = not(self.white_to_move)
        return [moves,num_check]



            


        
