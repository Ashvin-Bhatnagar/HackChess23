import pygame as pg
import board_tracker
import math
import chess
from pygame.locals import *

chess_board = chess.Board()

WIDTH = HEIGHT = 512
DIM = 8
SQ_SIZE = (HEIGHT) // DIM
FPS = 15
IMAGES = {}

# Load Images Function


def load_Images():
    pieces = ['wP', "wR", "wN", "wB", "wQ",
              "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load(
            "images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# User Input


def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH + 40, HEIGHT))
    clock = pg.time.Clock()
    state = board_tracker.State()
    load_Images()
    running = True
    sq_from_move = ()
    playerClicks = []
    while running:
        if state.whiteTurn:
            screen.fill(pg.Color("white"))
        else:
            screen.fill(pg.Color("black"))
        for e in pg.event.get():
            if state.won:
                print("Checkmate!")
            if state.draw:
                print("Draw!")
            if e.type == pg.QUIT or state.won or state.draw:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
                if state.whiteTurn:
                    location = pg.mouse.get_pos()
                    col = math.floor(location[0] / SQ_SIZE)
                    row = math.floor(location[1] / SQ_SIZE)
                    if sq_from_move == (row, col):
                        sq_from_move = ()
                        playerClicks = []
                    else:
                        sq_from_move = (row, col)
                        playerClicks.append(sq_from_move)
                    if len(playerClicks) == 2:
                        move = board_tracker.Move(
                            playerClicks[0], playerClicks[1], state.board)
                        move.is_promotion()
                        move.en_passant()
                        if move.valid_promotion:
                            pg.event.clear()
                            while True:
                                event = pg.event.wait()
                                if event.type == QUIT:
                                    pg.quit()
                                elif event.type == KEYDOWN:
                                    if event.key == pg.K_q:
                                        move.promoted_to = "Q"
                                        break
                                    elif event.key == pg.K_r:
                                        move.promoted_to = "R"
                                        break
                                    elif event.key == pg.K_b:
                                        move.promoted_to = "B"
                                        break
                                    elif event.key == pg.K_n:
                                        move.promoted_to = "N"
                                        break
                                    else:
                                        running = False
                                        break
                        state.makeWhiteMove(move)
                        # print(state.board)

                        # print(move.getStandardChessNotation())

                        sq_from_move = ()
                        playerClicks = []

            state.makeBlackMove()


                # elif e.type == pg.KEYDOWN:
                #     if e.key == pg.K_z:
                #         state.undoMove()


        drawGame(screen, state)
        clock.tick(FPS)
        pg.display.flip()


def drawGame(screen, state):
    drawSquare(screen, state.board)


def drawSquare(screen, board):
    colors = [pg.Color((104, 81, 60)), pg.Color((180, 160, 127))]
    for row in range(DIM):
        for column in range(DIM):
            color = colors[(row + column) % 2]
            pg.draw.rect(screen, color, pg.Rect(
                column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[row][column]
            if piece != "  ":
                screen.blit(IMAGES[piece], pg.Rect(
                    column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


main()
