import numpy as np

def get_state(engine):
    result = [
                engine.white,
                engine.black,
                engine.pawn,
                engine.rook,
                engine.knight,
                engine.bishop,
                engine.queen,
                engine.king,
                engine.not_moved,
                engine.en_passon
            ]
    
    return result

def square_to_bitboard(square_name):
    # Validate input square name
    valid_names = ['a1', 'b1', 'c1', 'd1', 'e1', 'f1', 'g1', 'h1',
                   'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2',
                   'a3', 'b3', 'c3', 'd3', 'e3', 'f3', 'g3', 'h3',
                   'a4', 'b4', 'c4', 'd4', 'e4', 'f4', 'g4', 'h4',
                   'a5', 'b5', 'c5', 'd5', 'e5', 'f5', 'g5', 'h5',
                   'a6', 'b6', 'c6', 'd6', 'e6', 'f6', 'g6', 'h6',
                   'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7',
                   'a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

    # Convert square name to bitboard index
    file = ord(square_name[0]) - ord('a')
    rank = int(square_name[1]) - 1
    bitboard_index = rank * 8 + file

    # Generate bitboard for the square
    bitboard = 1 << bitboard_index

    return np.uint(bitboard)

def fen_to_bb(fen):

    piece_map = {'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
                 'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11}

    bitboards = [np.uint(0)] * 12

    # Split the FEN string into its components
    fen_parts = fen.split()
    board_rows = fen_parts[0].split('/')

    # Process each row of the board
    for rank, row in enumerate(reversed(board_rows)):
        file = np.uint(0)
        for char in row:
            if char.isdigit():
                # Skip empty squares
                file += int(char)
            else:
                # Get the corresponding bitboard index for the piece
                piece_index = piece_map[char]
                # Set the bit for the piece on the corresponding bitboard
                bitboards[piece_index] |= np.uint(1) << np.uint(rank * 8 + file)
                file += np.uint(1)

    black = bitboards[6] | bitboards[7] | bitboards[8] | bitboards[9] | bitboards[10] | bitboards[11]
    white = bitboards[0] | bitboards[1] | bitboards[2] | bitboards[3] | bitboards[4] | bitboards[5] 
    pawn = bitboards[0] | bitboards[6]
    rook = bitboards[1] | bitboards[7]
    knight = bitboards[2] | bitboards[8]
    bishop = bitboards[3] | bitboards[9]
    queen = bitboards[4] | bitboards[10]
    king = bitboards[5] | bitboards[11] 

    turn = True
    if fen_parts[1] == 'b':
        turn = False

    not_moved = np.uint(0)
    if "Q" in fen_parts[2]:
        not_moved = not_moved | np.uint(1224979098644774912)
    if "K" in fen_parts[2]:
        not_moved = not_moved | np.uint(10376293541461622784)
    if "k" in fen_parts[2]:
        not_moved = not_moved | np.uint(144)
    if "q" in fen_parts[2]:
        not_moved = not_moved | np.uint(17)


    en_passon = 0
    if fen_parts[3] != '-':
        en_passon = square_to_bitboard(fen_parts[3])

        if en_passon & np.uint64(16711680) != 0:
            en_passon = en_passon << np.uint(8)
        else:
            en_passon = en_passon >> np.uint(8)
    
    halfmove_clock = int(fen_parts[4])

    fullmove_number = int(fen_parts[5])  


    return white, black, pawn, rook, knight, bishop, queen, king, turn, not_moved, en_passon, halfmove_clock, fullmove_number


def bb_to_fen(white, black, pawn, rook, knight, bishop, queen, king, turn, not_moved, en_passon, halfmove_clock, fullmove_number):
    piece_map = {0: 'P', 1: 'N', 2: 'B', 3: 'R', 4: 'Q', 5: 'K',
                 6: 'p', 7: 'n', 8: 'b', 9: 'r', 10: 'q', 11: 'k'}

    # Generate FEN representation of the board
    board_fen = ""
    for rank in reversed(range(8)):
        empty_count = 0
        for file in range(8):
            bitboard = 1 << (rank * 8 + file)
            bitboard = np.uint(bitboard)
            if bitboard & pawn:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[0 if bitboard & white else 6]
            elif bitboard & rook:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[1 if bitboard & white else 7]
            elif bitboard & knight:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[2 if bitboard & white else 8]
            elif bitboard & bishop:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[3 if bitboard & white else 9]
            elif bitboard & queen:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[4 if bitboard & white else 10]
            elif bitboard & king:
                if empty_count > 0:
                    board_fen += str(empty_count)
                    empty_count = 0
                board_fen += piece_map[5 if bitboard & white else 11]
            else:
                empty_count += 1

        if empty_count > 0:
            board_fen += str(empty_count)

        if rank > 0:
            board_fen += '/'

    fen = board_fen

    # Add additional FEN components
    fen += " " + ("w" if turn else "b")  # Turn
    
    if not_moved == 0: 
        fen += " " + "-"
    
    fen += " "
    if not_moved & np.uint(10376293541461622784) ^ np.uint(10376293541461622784) == 0:
        fen += "K"
    if not_moved & np.uint(1224979098644774912) ^ np.uint(1224979098644774912) == 0:
        fen += "Q"
    if not_moved & np.uint(144) ^ np.uint(144) == 0:
        fen += "k"
    if not_moved & np.uint(17) ^ np.uint(17) == 0:
        fen += "q"
    fen += " -" if en_passon == 0 else " " + bitboard_to_square(en_passon)  # En passant target square
    fen += " " + str(halfmove_clock)  # Halfmove clock
    fen += " " + str(fullmove_number)  # Fullmove number

    return fen

def bitboard_to_square(bitboard):
    field_num = int(bitboard)
    file_index = field_num.bit_length() - 1
    rank = file_index // 8
    file_index = file_index % 8

    file = chr(ord('a') + file_index)

    return file+str(rank)