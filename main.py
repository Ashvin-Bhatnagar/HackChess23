import pygame as pg
import engine
import math

WIDTH = HEIGHT = 512
DIM = 8
SQ_SIZE = HEIGHT // DIM
FPS = 15
IMAGES = {}

# Load Images Function

def load_Images():
    pieces = ['wP', "wR", "wN", "wB", "wQ", "wK", "bP", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = pg.transform.scale(pg.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

# User Input
def main():
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    screen.fill(pg.Color("white"))
    state = engine.State()
    load_Images()
    running = True
    sq_from_move = ()
    playerClicks = []
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
            elif e.type == pg.MOUSEBUTTONDOWN:
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
                    move = engine.Move(playerClicks[0], playerClicks[1], state.board)
                    print(move.getChessNotation())
                    state.makeMove(move)
                    sq_from_move = ()
                    playerClicks = []

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
            pg.draw.rect(screen, color, pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            piece = board[row][column]
            if piece != "  ":
                screen.blit(IMAGES[piece], pg.Rect(column*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))



main()
