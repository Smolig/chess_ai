from util import *
from engine_v3 import Engine

e = Engine()

fen = "rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq e3 0 1"
white, black, pawn, rook, knight, bishop, queen, king, turn, not_moved, en_passon, halfmove_clock, fullmove_number = fen_to_bb(fen)

e.print_board((en_passon))

fen2 = bb_to_fen(white, black, pawn, rook, knight, bishop, queen, king, turn, not_moved, en_passon, halfmove_clock, fullmove_number)

print(fen)
print(fen2)
