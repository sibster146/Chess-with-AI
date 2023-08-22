from abc import ABC, abstractmethod

class Move_Abs(ABC):
    def __init__(self,start,end,board):
        self.start_r,self.start_c = start
        self.end_r,self.end_c = end
        self.piece_moved = board[self.start_r][self.start_c]
        self.captured_piece = board[self.end_r][self.end_c]

    def __eq__(self,other):
        pass


class Move(Move_Abs):
    def __init__(self,start,end,board):
        self.start_r,self.start_c = start
        self.end_r,self.end_c = end
        self.piece_moved = board[self.start_r][self.start_c]
        self.captured_piece = board[self.end_r][self.end_c]

        self.is_pawn_promo = False
        if ((self.piece_moved == 'wP' and self.end_r == 0) or
            (self.piece_moved == 'bP' and self.end_r == 7)):
            self.is_pawn_promo = True

    def __eq__(self,other):
        if not isinstance(other, Move):
            return False
        return (self.start_r==other.start_r and
                self.start_c==other.start_c and
                self.end_r==other.end_r and
                self.end_c==other.end_c)
    
    def copy(self):
        return self