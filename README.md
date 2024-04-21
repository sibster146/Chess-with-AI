## AI CHESS ENGINE

**PROJECT DESCRIPTION**

AI Chess Engine. One human vs One computer

**INSTALLATION AND RUN**

git clone repo into local repository. Install dependencies from requirements.txt. Then, run python main.py.

**MODULE OVERVIEW**

*image/*- contains images of all the chess pieces

*cached_moves.pkl*- contains dictionary of previously played game states with the best associated move

*chess_engine.py*- contains definition of engine class

    __init__- initializes the board state, where the pieces start, whose turn it is, kings' locations, stalemate, checkmake, etc

    make_move()- moves a piece on the board; if pawn moves to the end of board, replaces it with a queen

    print_move()- prints the move made

    undo_last_move()- undoes the last move made

    get_possible_moves()- returns the list of possible moves for the current player's turn BUT DOES NOT check of the current player's king is in check or if the move would lead to a king becoming in check

    get_king()- returns the position of the current player's king

    get_valid_moves()- takes the list of possible moves from get_possible_moves() and takes the number of opponent pieces checking the current player's king. The function sets the stalemate and checkmate boolean values appropriately from the list of possible moves and number of opponent pieces checking the current player's king. If moves list is empty and there is a check, it is checkmate. If there are no moves and there is no check, then stalemate. If there are no checkmates, but a nonempty list of moves, then all the possible moves are valid, so return the entire list of possible moves. If the number of check >1, then only the king can move to move out of check. Last, if there is only one check and nonempty list of possible moves, we have to evaluate every possible move to see if the move will result in the king moving out of check. If not, we remove that move from the list of moves. Then, we return the remaining list as the valid list of possible moves.

    

    
  



