from abc import ABC, abstractmethod
from move import Move

piece_value = {
    'Q': 10,
    'R': 5,
    'B': 3.5,
    'N': 3.5,
    'P': 1,
    'K':0
}

class Piece(ABC):
    def __init__(self,player,r,c,board,one_dir):
        self.player = player
        self.r = r
        self.c = c
        self.board = board
        self.one_dir = one_dir
        if self.player == 'w':
            self.enemy = 'b'
        else:
            self.enemy = 'w'
    
    @abstractmethod
    def get_possible_moves(self):
        pass

    def check_bounds(self,r,c):
        if r < 0 or c < 0 or r >= 8 or c >= 8:
            return False
        return True
    


class Rook(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)


    def get_possible_directions(self):
        if not self.one_dir:
            return [[0,1],[1,0],[-1,0],[0,-1]]
        elif self.one_dir in [[1,0],[-1,0]]:
            return  [[1,0],[-1,0]]
        elif self.one_dir in [[0,1],[0,-1]]:
            return [[0,1],[0,-1]]
        return []
        

    def get_possible_moves(self):
        moves = []
        positions = self.get_possible_directions()
        score = 0

        for x,y in positions:
            i = 1
            while (self.check_bounds(self.r+i*x,self.c+i*y) and self.board[self.r+i*x][self.c+i*y] == "  "):
                moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                i+=1
            # add score for threatening potential
            if self.check_bounds(self.r+i*x,self.c+i*y) and self.player == 'b' and self.board[self.r+i*x][self.c+i*y][0] == 'w':
                moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]
            elif self.check_bounds(self.r+i*x,self.c+i*y) and self.player == 'w' and self.board[self.r+i*x][self.c+i*y][0] == 'b':
                moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]

            # add score for protection potential
            elif self.check_bounds(self.r+i*x,self.c+i*y) and self.player == self.board[self.r+i*x][self.c+i*y][0]:
                score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]
            elif self.check_bounds(self.r+i*x,self.c+i*y) and self.player == self.board[self.r+i*x][self.c+i*y][0]:
                score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]


        return [moves,score]
        



class Pawn(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)

    def get_possible_directions(self):
        if not self.one_dir:
            return [[1,0],[1,1],[1,-1],[-1,0],[-1,-1],[-1,1]]
        
        return [self.one_dir]

    def get_possible_moves(self):
        moves = []
        positions = self.get_possible_directions()
        score = 0

        for i in range(len(positions)):
            x,y = positions[i]
            if self.player == 'b':
                # the pawn moves down one
                if self.check_bounds(self.r+x,self.c+y) and i == 0 and self.board[self.r+x][self.c+y]=="  ":
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                    #the pawn moves down two if still at original location
                    if self.r == 1 and self.board[self.r+x+1][self.c+y]=="  ":
                        moves.append(Move((self.r,self.c),(self.r+x+1,self.c+y),self.board))
                # the pawn captures if oppo is diagonal to it and add to score for capturing potential
                elif self.check_bounds(self.r+x,self.c+y) and 1<=i<=2 and self.board[self.r+x][self.c+y][0]==self.enemy:
                    score += piece_value[self.board[self.r+x][self.c+y][1]]
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                # add to score of protection potential
                elif self.check_bounds(self.r+x,self.c+y) and 1<=i<=2 and self.board[self.r+x][self.c+y][0]==self.player:
                    score += piece_value[self.board[self.r+x][self.c+y][1]]

            
            elif self.player == 'w':
                # the pawn moves up one
                if self.check_bounds(self.r+x,self.c+y) and i == 3 and self.board[self.r+x][self.c+y]=="  ":
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                    # the pawn moves up two if still at original location
                    if self.r == 6 and self.board[self.r+x-1][self.c+y]=="  ":
                        moves.append(Move((self.r,self.c),(self.r+x-1,self.c+y),self.board))
                # the pawn capures if oppo is diagonal to it
                elif self.check_bounds(self.r+x, self.c+y) and 4<=i<=5 and self.board[self.r+x][self.c+y][0]==self.enemy:
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                    score += piece_value[self.board[self.r+x][self.c+y][1]]
                # add to score of protection potential
                elif self.check_bounds(self.r+x,self.c+y) and 1<=i<=2 and self.board[self.r+x][self.c+y][0]==self.player:
                    score += piece_value[self.board[self.r+x][self.c+y][1]]


        return [moves,score]

    


class Knight(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)


    def get_possible_moves(self):
        moves = []
        score = 0

        if self.one_dir:
            return [moves,0]
        
        positions = [[-2,1],[-1,2],[1,2],[2,1],[2,-1],[1,-2],[-1,-2],[-2,-1]]

        for x,y in positions:
            if self.check_bounds(self.r+x,self.c+y):
                if self.board[self.r+x][self.c+y] == "  ":
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                elif (self.player == 'w' and self.board[self.r+x][self.c+y][0] == 'b' or 
                      self.player == 'b' and self.board[self.r+x][self.c+y][0] == 'w'):
                        moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                        score += piece_value[self.board[self.r+x][self.c+y][1]]
                elif self.board[self.r+x][self.c+y][0] == self.player:
                    score += piece_value[self.board[self.r+x][self.c+y][1]]

        return [moves,score]
    

class Bishop(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)


    def get_possible_directions(self):
        if not self.one_dir:
            return [[1,1],[-1,-1],[-1,1],[1,-1]]
        elif self.one_dir in [[1,1],[-1,-1]]:
            return [[1,1],[-1,-1]]
        elif self.one_dir in [[-1,1],[1,-1]]:
            return [[-1,1],[1,-1]]
        return []

    def get_possible_moves(self):
        moves = []
        score = 0
        positions = self.get_possible_directions()

        for x,y in positions:
            i = 1
            while self.check_bounds(self.r+i*x,self.c+i*y) and self.board[self.r+i*x][self.c+i*y] == "  ":
                moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                i+=1
            if self.check_bounds(self.r+i*x,self.c+i*y):
                if self.player == 'w' and self.board[self.r+i*x][self.c+i*y][0] == 'b':
                    moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                    score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]
                elif self.player == 'b' and self.board[self.r+i*x][self.c+i*y][0] == 'w':
                    moves.append(Move((self.r,self.c),(self.r+i*x,self.c+i*y),self.board))
                    score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]
                elif self.board[self.r+i*x][self.c+i*y][0] == self.player:
                    score += piece_value[self.board[self.r+i*x][self.c+i*y][1]]

        return [moves,score]

class Queen(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)
        self.rook = Rook(player,r,c,board,one_dir)
        self.bishop = Bishop(player,r,c,board,one_dir)

    def get_possible_moves(self):
        moves = []
        [moves1,score1] = self.rook.get_possible_moves()
        [moves2,score2] = self.bishop.get_possible_moves()
        moves.extend(moves1)
        moves.extend(moves2)

        return [moves,score1+score2]
    
class King(Piece):
    def __init__(self,player,r,c,board,one_dir):
        super().__init__(player,r,c,board,one_dir)

    def get_pins(self):
        positions = [[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1]]

        possible_pin_locs = []
        for x,y in positions:
            i = 1
            while self.check_bounds(self.r+i*x,self.c+i*y):
                if self.board[self.r+i*x][self.c+i*y][0] == self.player:
                    possible_pin_locs.append([self.r+i*x,self.c+i*y,[x,y]])
                    break
                elif self.board[self.r+i*x][self.c+i*y][0] == self.enemy:
                    break
                i+=1

        pins = []
        for x,y,d in possible_pin_locs:
            temp = self.board[x][y]
            self.board[x][y] = "  "
            if self.is_check_by_direc(x,y,d):
                pins.append([(x,y),d])
            self.board[x][y] = temp
        return pins
    

    def is_check_by_direc(self,r,c,direction):

        x,y = direction
        r,c = self.r,self.c
        i = 1
        res = 0
        while self.check_bounds(r+i*x,c+i*y):
            if self.board[r+i*x][c+i*y][0] == self.player:
                    break
            elif self.board[r+i*x][c+i*y][0] == self.enemy:
                # If there is a pawn that could check
                if self.board[r+i*x][c+i*y][1]=='P' and i == 1:
                    # if enemy is black, [-1,1] [-1,-1]
                    if (self.enemy == 'b' and [x,y] in [[-1,1],[-1,-1]] or 
                        self.enemy == 'w' and [x,y] in [[1,1],[1,-1]]):
                        res+=1
                        break
                # if there is a king that could check
                if self.board[r+i*x][c+i*y][1]=='K' and i ==1:
                    res+=1
                    break
                # if there is a ROok or Queen that could check ortho
                elif self.board[r+i*x][c+i*y][1] in ['R','Q'] and [x,y] in [[-1,0],[1,0],[0,1],[0,-1]]:
                    res+=1
                    break
                #if there is a Bishop or Queen that could check diag
                elif self.board[r+i*x][c+i*y][1] in ['B','Q'] and [x,y] in [[1,1],[1,-1],[-1,1],[-1,-1]]:
                    res+=1
                    break
            i+=1
        return res


    def in_check_pos(self,r,c):
        return self.is_check_by_bishop(r,c) + self.is_check_by_ortho_diag(r,c)
    

    def is_check_by_bishop(self,r,c):
        n = 0
        bishop_positions = [[-1,-2],[1,2],[1,-2],[-1,2],[2,1],[-2,-1],[-2,1],[2,-1]]
        for x,y in bishop_positions:
            if self.check_bounds(r+x,c+y):
                if self.board[r+x][c+y] == self.enemy + 'N':
                    n+=1
        return n
    

    def is_check_by_ortho_diag(self,r,c):
        n = 0
        positions = [[-1,0],[1,0],[0,1],[0,-1],[1,1],[-1,1],[-1,-1],[1,-1]]
        for d in positions:
            n += self.is_check_by_direc(r,c,d)
        return n
    
    def get_possible_moves(self):
        moves = []
        positions = [[-1,0],[0,1],[1,0],[0,-1],[-1,1],[1,1],[1,-1],[-1,-1]]
        for x,y in positions:
            if self.check_bounds(self.r+x,self.c+y):
                if self.board[self.r+x][self.c+y]==self.player:
                    continue
                
                if self.in_check_pos(self.r+x,self.c+y):
                    continue
                if self.board[self.r+x][self.c+y] == "  ":
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                elif self.player == 'w' and self.board[self.r+x][self.c+y][0] == self.enemy:
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
                elif self.player == 'b' and self.board[self.r+x][self.c+y][0] == self.enemy:
                    moves.append(Move((self.r,self.c),(self.r+x,self.c+y),self.board))
        return [moves,0]