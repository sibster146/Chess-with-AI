import pygame as pg
import chess_engine
from smartmovefinder import AIPlayer
from move import Move

WIDTH = 512      # pixels along width of board
HEIGHT = 512     # pixels along height of board
DIMENSION = 8    # number of blocks per height/width
BLOCK = 64       # pixels along block side
FPS = 15
IMAGES = {}

def initialize_images():
    pieces = ['bR','bN','bB','bQ','bK','bP',
              'wR','wN','wB','wQ','wK','wP']
    for p in pieces:
        IMAGES[p] = pg.transform.scale(pg.image.load(f"images/{p}.png"),(BLOCK,BLOCK))

def draw_board(display):
    colors = [pg.Color("white"),pg.Color("dark grey")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c)%2]
            pg.draw.rect(display, color, pg.Rect(c*BLOCK,r*BLOCK, BLOCK, BLOCK))

def draw_pieces(display,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != '  ':
                display.blit(IMAGES[piece],pg.Rect(c*BLOCK,r*BLOCK, BLOCK, BLOCK))

def draw_ops(display,engine, valid_moves,move_stack):
    draw_board(display)
    highlight(display,engine,valid_moves,move_stack)
    draw_pieces(display,engine.board)


def highlight(display, engine,valid_moves, move_stack):
    if move_stack != ():
        r,c = move_stack
        if engine.board[r][c][0] == ('w' if engine.white_to_move else 'b'):
            s = pg.Surface((BLOCK, BLOCK))
            s.set_alpha(100)
            s.fill(pg.Color('blue'))
            display.blit(s,(c*BLOCK,r*BLOCK))
            s.fill(pg.Color('yellow'))
            for m in valid_moves:
                if m.start_r == r and m.start_c==c:
                    display.blit(s,(m.end_c*BLOCK,m.end_r*BLOCK))

def write_winner(white,num_check):
    if num_check:
        print("Black wins" if white else "White wins")
    else:
        print("Stalemate")

def main():
    pg.init()
    display = pg.display.set_mode((WIDTH, HEIGHT))
    display.fill(pg.Color("white"))
    clock = pg.time.Clock()
    engine = chess_engine.Engine()
    valid_moves,num_checks = engine.get_valid_moves()
    move_flag = False
    move_stack = ()
    player_clicks = []
    initialize_images()
    on = True
    player_one = True
    player_two = False
    undo_last_move = False
    aiplayer = AIPlayer()
    while on:
        human_turn = (engine.white_to_move and player_one) or (not engine.white_to_move and player_two)
        for e in pg.event.get():
            # COULD DO DESIGN PATTERN HERE
            if e.type == pg.QUIT:
                on = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if on and human_turn:
                    loc = pg.mouse.get_pos()
                    r,c = [loc[1]//BLOCK,loc[0]//BLOCK]
                    if move_stack == (r,c):
                        move_stack = ()
                        player_clicks.clear()
                    else:
                        move_stack = (r,c)
                        player_clicks.append(move_stack)

                    if len(player_clicks) == 2 and human_turn:
                        move = Move(player_clicks[0],player_clicks[1],engine.board)
                        for i in range(len(valid_moves)):
                            if move == valid_moves[i]:
                                engine.print_move(move)
                                engine.make_move(valid_moves[i])
                                move_flag = True
                                move_stack = ()
                                player_clicks.clear()
                        if not move_flag:
                            player_clicks.clear()
                            player_clicks.append(move_stack)
                    
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_z:
                    engine.undo_last_move()
                    undo_last_move = True
    
        if on and (not human_turn):
            startrow,startcol,endrow,endcol = aiplayer.get_best_move(engine.board,engine.white_to_move)
            AIMove = Move((startrow,startcol),(endrow,endcol),engine.board)
            engine.print_move(AIMove)
            engine.make_move(AIMove)
            move_flag = True

        if move_flag:
            valid_moves,num_checks = engine.get_valid_moves()

            if not valid_moves:
                on = False
                write_winner(engine.white_to_move,num_checks)
            move_flag = False
            undo_last_move = False
        draw_ops(display,engine,valid_moves,move_stack)
        clock.tick(FPS)
        pg.display.flip()

    aiplayer.update_cached_moves()


if __name__ == "__main__":
    main()