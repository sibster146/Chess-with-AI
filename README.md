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

*main.py*- starts the application, draws the board, manages the iteration of the game through each players turn

    initialize_images()- loads the images from the pieces png files

    draw_board()- draws the board

    draw_pieces()- draws the pieces on the board

    highlight()- highlights the spots on the board that is a valid move for a piece to go to

    draw_ops()- calls highlight(), draw_board(), draw_pieces()

    write_winner()- writes the winner

    main()- starts the iteration of the game. All above functions are called in here.

*move.py*- defines the move class object

    __init__()- attributes are the starting and ending positions, the piece being moved, and any potentially captured pieces

    __eq__()- two moves are considered equal if the start and ending positions are the same

    copy()- returns object

*piece.py*- defines the class objects for knight, rook, bishop, queen, king, and pawn

    Every class has get_possible_moves(), which returns the list of possible moves for that piece. The king has some extra functions.

    get_pins()- return the number of friendly pieces that are currently preventing check (we cannot move these pieces)
    
    is_check_by_direc()- checks if the king by one straight direction

    is_check_by _bishop()- checks if the king is in check by a bishop

    is_check_by_ortho_diag()- calls is_check_by_direc() with directions up, down, diagonal left and right

    in_check_pos()- calls is_check_by_ortho_diag and is_check_by_bishop()

*piece_factory.py*- creates piece classes

    PieceFactory class has one method. create_piece() which creates pieces

*smartmovefinder.py*- defines the AI player class that goes against the human player

    __init__()- loads the cached_moves.pkl file

    get_best_move()- returns the best move to do in a given game state. Parses the game state in a format that works with get_stockfish_move() and Calls get_stockfish_move() to do this

    get_stockfish_move()- takes the game state and returns the best move

    






    

    
  



