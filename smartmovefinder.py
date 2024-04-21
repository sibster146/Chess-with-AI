import random
import subprocess
import sys
import numpy as np
import concurrent.futures
import pickle
import os

class AIPlayer:
    def __init__(self):

        self.rank_file_dict = {
            "a": 0, "b": 1, "c": 2, "d": 3, 
            "e": 4, "f": 5, "g": 6, "h": 7
        }
        if os.path.exists('cached_moves.pkl'):
            with open('cached_moves.pkl', 'rb') as file:
                self.data = pickle.load(file)
        else:
            self.data = {}

    def get_stockfish_move(self,board_string):
        # Start Stockfish engine and send FEN position
        stockfish = subprocess.Popen(
            "Chess-with-AI\stockfish",
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        stockfish.stdin.write(f"position fen {board_string}\n")
        stockfish.stdin.write(f"go movetime 3500\n")
        stockfish.stdin.flush()
        # Read and process Stockfish's responses until a valid move is found
        while True:
            line = stockfish.stdout.readline().strip()
            if line.startswith("bestmove"):
                suggested_move = line.split(" ")[1]
                break
        stockfish.terminate()
        startcol,startrow,endcol,endrow = list(suggested_move)
        startrow = 8 - int(startrow)
        endrow = 8 - int(endrow)
        startcol = self.rank_file_dict[startcol]
        endcol = self.rank_file_dict[endcol]
        return [startrow,startcol,endrow,endcol]    


    def get_best_move(self,board,player):

        player = "w" if player else "b"
        board_list = []
        for row in board:
            row_string = ""
            i = 0
            while i < 8:
                spot = row[i]
                if spot[0] == 'w':
                    row_string+= spot[1]
                elif spot[0] == 'b':
                    row_string += spot[1].lower()
                else:
                    c = 0
                    while i < 8 and row[i] == "  ":
                        i+=1
                        c+=1
                    row_string += str(c)
                    continue
                i+=1
            board_list.append(row_string)

        board_string = "/".join(board_list) + " " + player + " " + "- -"

        if board_string in self.data:
            return self.data[board_string]

        with concurrent.futures.ThreadPoolExecutor() as exec:
            future = exec.submit(self.get_stockfish_move,board_string)
            try:
                result = future.result(timeout=5)
                self.data[board_string] = result
                return result
            except concurrent.futures.TimeoutError:
                print("timeout")
                sys.exit(1)


    def update_cached_moves(self):
        with open('cached_moves.pkl', 'wb') as file:
            pickle.dump(self.data, file)



def find_random_move(valid_moves):
    r = random.randint(0,len(valid_moves)-1)
    return valid_moves[r]




