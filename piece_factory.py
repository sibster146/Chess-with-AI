from abc import ABC, abstractmethod
from piece import Pawn,Rook,Bishop,Knight,Queen, King

class ABSPieceFactory(ABC):
    def create_piece():
        pass


class PieceFactory(ABSPieceFactory):
    piece_class_mapping = {
        'P':Pawn,
        'R':Rook,
        'B':Bishop,
        'N':Knight,
        'Q':Queen,
        'K':King
    }

    def create_piece(self,piece_str,player,r,c,board,one_dir):
        piece_class = self.piece_class_mapping.get(piece_str)
        if piece_class:
            return piece_class(player,r,c,board,one_dir)
    