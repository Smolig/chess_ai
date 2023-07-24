import numpy as np
from time import perf_counter


def test(pawn, rook, knight, bishop, queen, king, white, black, turn, engine):
    engine.white = white
    engine.black = black
    engine.pawn = pawn
    engine.knight = knight
    engine.bishop = bishop
    engine.queen = queen
    engine.king = king
    engine.rook = rook
    engine.turn = turn
    pawn, rook, knight, bishop, queen, king = engine.give_moves()
    chess_board = {
        1: "a1",
        2: "b1",
        3: "c1",
        4: "d1",
        5: "e1",
        6: "f1",
        7: "g1",
        8: "h1",
        9: "a2",
        10: "b2",
        11: "c2",
        12: "d2",
        13: "e2",
        14: "f2",
        15: "g2",
        16: "h2",
        17: "a3",
        18: "b3",
        19: "c3",
        20: "d3",
        21: "e3",
        22: "f3",
        23: "g3",
        24: "h3",
        25: "a4",
        26: "b4",
        27: "c4",
        28: "d4",
        29: "e4",
        30: "f4",
        31: "g4",
        32: "h4",
        33: "a5",
        34: "b5",
        35: "c5",
        36: "d5",
        37: "e5",
        38: "f5",
        39: "g5",
        40: "h5",
        41: "a6",
        42: "b6",
        43: "c6",
        44: "d6",
        45: "e6",
        46: "f6",
        47: "g6",
        48: "h6",
        49: "a7",
        50: "b7",
        51: "c7",
        52: "d7",
        53: "e7",
        54: "f7",
        55: "g7",
        56: "h7",
        57: "a8",
        58: "b8",
        59: "c8",
        60: "d8",
        61: "e8",
        62: "f8",
        63: "g8",
        64: "h8",
    }

    count = 0
    pawn_translate = []
    rook_translate = []
    knight_translate = []
    bishop_translate = []
    queen_translate = []
    king_translate = []
    for x in pawn:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    pawn_translate.append("P" + chess_board[j + 1])
                else:
                    pawn_translate.append("p" + chess_board[j + 1])

    for x in rook:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    rook_translate.append("R" + chess_board[j + 1])
                else:
                    rook_translate.append("r" + chess_board[j + 1])

    for x in knight:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    knight_translate.append("K" + chess_board[j + 1])
                else:
                    knight_translate.append("k" + chess_board[j + 1])

    for x in bishop:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    bishop_translate.append("B" + chess_board[j + 1])
                else:
                    bishop_translate.append("b" + chess_board[j + 1])

    for x in queen:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    queen_translate.append("Q" + chess_board[j + 1])
                else:
                    queen_translate.append("q" + chess_board[j + 1])

    for x in king:
        for j in range(64):
            single_move = np.uint(1) << np.uint(j)
            if x & single_move != 0:
                count += 1
                if engine.turn:
                    king_translate.append("K" + chess_board[j + 1])
                else:
                    king_translate.append("k" + chess_board[j + 1])

    # print("Pawn:", pawn_translate)
    # print("Rook:", rook_translate)
    # print("Knight:", knight_translate)
    # print("Bishop:", bishop_translate)
    # print("Queen:", queen_translate)
    # print("King:", king_translate)
    # print("Moves:", count)     #debugging
    return (
        pawn_translate,
        rook_translate,
        knight_translate,
        bishop_translate,
        queen_translate,
        king_translate,
        count,
    )


def benchmark(engine1):
    duration = 0

    for i in range(1000):
        start = perf_counter()
        engine1.give_moves()
        end = perf_counter()
        performance = end - start
        duration += performance

    duration = duration / 1000

    print(f"Average runtime: {duration}s")


def write_state(pawn, rook, knight, bishop, queen, king, white, black, turn, engine):
    engine.white = white
    engine.black = black
    engine.pawn = pawn
    engine.knight = knight
    engine.bishop = bishop
    engine.queen = queen
    engine.king = king
    engine.rook = rook
    engine.turn = turn


def write_starting_position(engine1):
    white = np.uint64(65535)
    black = np.uint64(18446462598732840960)
    pawn = np.uint64(71776119061282560)
    knight = np.uint64(4755801206503243842)
    rook = np.uint64(9295429630892703873)
    bishop = np.uint64(2594073385365405732)
    queen = np.uint64(576460752303423496)
    king = np.uint64(1152921504606846992)
    # True: Whites' turn, false: black's turn
    turn = True
    # stores if a pawn did a double move that round
    double_pawn = np.uint64(0)
    # stores move history: (move_from, move_to, Name of removed figure / None, if has_moved has changed (boolean), if move was castling(boolean))
    move_history = []
    # Rooks and kings that have not moved
    not_moved = np.uint64(10448351135499550865)

    write_state(pawn, rook, knight, bishop, queen, king, white, black, turn, engine1)
    print("Opening italian game:")


def write_opening_italian_game(engine1):
    white = np.uint64(337702815)
    black = np.uint64(18297848277795602432)
    pawn = np.uint64(67272588421820160)
    knight = np.uint64(4611690416475996162)
    rook = np.uint64(9295429630892703873)
    bishop = np.uint64(2594073385432514564)
    queen = np.uint64(576460752303423496)
    king = np.uint64(1152921504606846992)
    turn = False

    write_state(pawn, rook, knight, bishop, queen, king, white, black, turn, engine1)
    print("Opening italian game:")


def write_opening_queens_gambit(engine1):
    white = np.uint64(201389055)
    black = np.uint64(18444210833278894080)
    pawn = np.uint64(69524353808659200)
    knight = np.uint64(4755801206503243842)
    rook = np.uint64(9295429630892703873)
    bishop = np.uint64(2594073385365405732)
    queen = np.uint64(576460752303423496)
    king = np.uint64(1152921504606846992)
    turn = False

    write_state(pawn, rook, knight, bishop, queen, king, white, black, turn, engine1)
    print("Opening queens gambit:")


def write_midgame(engine1):
    white = np.uint64(69390882737)
    black = np.uint64(15127327282726699008)
    pawn = np.uint64(65020720157087488)
    knight = np.uint64(4611686018427650048)
    rook = np.uint64(9295429630892703873)
    bishop = np.uint64(2251885713031200)
    queen = np.uint64(17592320262144)
    king = np.uint64(1152921504606846992)
    turn = True
    engine1.move = np.uint64(0)
    engine1.attack = np.uint64(0)
    engine1.castling = np.uint64(0)
    engine1.en_passon = np.uint64(0)
    # stores if a pawn did a double move that round
    engine1.double_pawn = np.uint64(0)
    engine1.fig_pos = np.uint64(0)
    engine1.thread = np.uint64(0)
    # stores figures that attack castling
    engine1.castling_block = np.uint64(0)
    # stores move history: (move_from, move_to, Name of removed figure / None, if has_moved has changed (boolean), if move was castling(boolean))
    engine1.move_history = []
    # Rooks and kings that have not moved
    engine1.not_moved = np.uint64(10448351135499550865)
    # Toggle Ui
    engine1.game_going = True
    engine1.main_menue = True
    # True: Player vs Player, False Player vs Ai
    engine1.game_mode = True

    write_state(pawn, rook, knight, bishop, queen, king, white, black, turn, engine1)

def benchmark_alpha_beta(engine):
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 0
    

    for i in range(20):
        write_midgame(engine)
        x = engine.iterativ()
        print(x)
        d1 += x[0][1]
        d2 += x[1][1]
        d3 += x[2][1]
        d4 += x[3][1]

    print(d1)
    print(d2)
    print(d3)
    print(d4)

    print(d1/20)
    print(d2/20)
    print(d3/20)
    print(d4/20)


def run_testcases():
    with open('testcases.txt', 'r') as file:
        for line in file:
        # Split the line into variables
            variables = line.split()
        # Call the override_variables method
            print("********Begin TestCase*******")
            engine = Engine()
            override_engine(variables, engine)
            engine.print_state()
            engine.iterativ()
            print("********End TestCase*******")
            
def override_engine(variables, engine):
    engine.white = np.uint64(variables[0])
    engine.black = np.uint64(variables[1])
    engine.pawn = np.uint64(variables[2])
    engine.knight = np.uint64(variables[3])
    engine.rook = np.uint64(variables[4])
    engine.bishop = np.uint64(variables[5])
    engine.queen = np.uint64(variables[6])
    engine.king = np.uint64(variables[7])
    engine.turn = variables[8]
   
