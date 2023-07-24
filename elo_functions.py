import positional_values
import numpy as np


mask_R1 = np.uint64(255)
mask_R8 = np.uint64(18374686479671623680)
mask_R2 = np.uint64(65280)
mask_R7 = np.uint64(71776119061217280)
mask_R5 = np.uint64(1095216660480)
mask_R4 = np.uint64(4278190080)
mask_R6 = np.uint64(280375465082880)
mask_R3 = np.uint64(16711680)

mask_A = np.uint64(72340172838076673)
mask_B = np.uint64(144680345676153346)
mask_C = np.uint64(289360691352306692)
mask_D = np.uint64(578721382704613384)
mask_E = np.uint64(1157442765409226768)
mask_F = np.uint64(2314885530818453536)
mask_G = np.uint64(4629771061636907072)
mask_H = np.uint64(9259542123273814144)
mask_bullseye = np.uint64(103481868288)     # innere 4 felder
mask_bull = np.uint64(66125924401152)       # äußerer ring der mitte (ohne mitte), 12 felder


def count_figures(self):
    colour = self.white
    king = bin(colour & self.king).count("1")
    queen = bin(colour & self.queen).count("1")
    bishop = bin(colour & self.bishop).count("1")
    knight = bin(colour & self.knight).count("1")
    rook = bin(colour & self.rook).count("1")
    pawn = bin(colour & self.pawn).count("1")

    colour = self.black
    king -= bin(colour & self.king).count("1")
    queen -= bin(colour & self.queen).count("1")
    bishop -= bin(colour & self.bishop).count("1")
    knight -= bin(colour & self.knight).count("1")
    rook -= bin(colour & self.rook).count("1")
    pawn -= bin(colour & self.pawn).count("1")

    return king, queen, bishop, knight, rook, pawn


def is_opening_phase(self):
    total_piece_count = bin(self.white | self.black).count("1")
    pawn_count = bin(self.white & self.pawn).count("1") + bin(self.black & self.pawn).count("1")
    open_lines_count = self.calculate_open_lines()
    if total_piece_count > 22 and pawn_count > 10 and open_lines_count <= 5:
        return True
    else:
        return False


def calculate_open_lines(self):
    open_lines_count = 0
    column_masks = [mask_R1, mask_R2, mask_R3, mask_R4, mask_R5, mask_R6, mask_R7, mask_R8]
    row_masks = [mask_A, mask_B, mask_C, mask_D, mask_E, mask_F, mask_G, mask_H]

    for row in row_masks:
        if (self.white & row == 0) and (self.black & row == 0):
            open_lines_count += 1
    for column in column_masks:
        if (self.white & column == 0) and (self.black & column == 0):
            open_lines_count += 1
    return open_lines_count


def calculate_doubled_pawns(self):
    doubled_pawns_count = 0
    row_masks = [mask_A, mask_B, mask_C, mask_D, mask_E, mask_F, mask_G, mask_H]

    for row in row_masks:
        white_pawns_line = bin(self.white & self.pawn & row).count("1")
        black_pawns_line = bin(self.black & self.pawn & row).count("1")
        if white_pawns_line > 1:
            doubled_pawns_count -= 3
        if black_pawns_line > 1:
            doubled_pawns_count += 3
    return doubled_pawns_count


def calculate_center_control(self, bitboard):
    control_count_bullseye = bin(bitboard & mask_bullseye).count("1")
    control_count_bull = bin(bitboard & mask_bull).count("1")
    return control_count_bullseye, control_count_bull


def is_endgame_phase(self):
    total_piece_count = bin(self.white | self.black).count("1")
    pawn_count = bin(self.white & self.pawn).count("1") + bin(self.black & self.pawn).count("1")
    open_lines_count = self.calculate_open_lines()
    if total_piece_count > 12 and pawn_count > 8 and open_lines_count < 8:
        return False
    else:
        return True


def get_score(self):
    material_values = {
        "king": 20000,
        "queen": 900,
        "rook": 500,
        "bishop": 300,
        "knight": 300,
        "pawn": 100
    }
    bullseye_bonus = 10
    bull_bonus = 5

    if self.is_opening_phase() and not self.is_endgame_phase():
        material_values["knight"] = 320
    elif self.is_endgame_phase() and not self.is_opening_phase():
        material_values["rook"] = 550
    elif not self.is_opening_phase() and not self.is_endgame_phase():
        pass
    score = (
            material_values["king"] * self.count_figures()[0]
            + positional_values.calculate_positional_value(self.white & self.king, positional_values.white_king)
            - positional_values.calculate_positional_value(self.black & self.king, positional_values.black_king)
            + material_values["queen"] * self.count_figures()[1]
            + positional_values.calculate_positional_value(self.white & self.queen, positional_values.white_queen)
            - positional_values.calculate_positional_value(self.black & self.queen, positional_values.black_queen)
            + material_values["rook"] * self.count_figures()[2]
            + positional_values.calculate_positional_value(self.white & self.rook, positional_values.white_rook)
            - positional_values.calculate_positional_value(self.black & self.rook, positional_values.black_rook)
            + material_values["bishop"] * self.count_figures()[3]
            + positional_values.calculate_positional_value(self.white & self.bishop, positional_values.white_bishop)
            - positional_values.calculate_positional_value(self.black & self.bishop, positional_values.black_bishop)
            + material_values["knight"] * self.count_figures()[4]
            + positional_values.calculate_positional_value(self.white & self.knight, positional_values.white_knight)
            - positional_values.calculate_positional_value(self.black & self.knight, positional_values.black_knight)
            + material_values["pawn"] * self.count_figures()[5]
            + positional_values.calculate_positional_value(self.white & self.pawn, positional_values.white_pawn)
            - positional_values.calculate_positional_value(self.black & self.pawn, positional_values.black_pawn)
            + bullseye_bonus * self.calculate_center_control(self.white)[0]
            + bull_bonus * self.calculate_center_control(self.white)[1]
            - bullseye_bonus * self.calculate_center_control(self.black)[0]
            - bull_bonus * self.calculate_center_control(self.black)[1]
            + self.calculate_doubled_pawns()
    )
    return score
