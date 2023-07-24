import numpy as np
import math
import random
import positional_values
import elo_functions
from time import perf_counter

mask_notA = np.uint64(18374403900871474942)
mask_notAB = np.uint64(18229723555195321596)
mask_notH = np.uint64(9187201950435737471)
mask_notGH = np.uint64(4557430888798830399)
mask_R2 = np.uint64(65280)
mask_R7 = np.uint64(71776119061217280)
mask_R5 = np.uint64(1095216660480)
mask_R4 = np.uint64(4278190080)
mask_R6 = np.uint64(280375465082880)
mask_R3 = np.uint64(16711680)
mask_R1_R8 = np.uint64(18374686479671623935)
mask_castling = np.uint64(9223372036854775936)
mask_R1 = np.uint64(255)
mask_R8 = np.uint64(18374686479671623680)
mask_Hill = np.uint64(103481868288)
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
field_mask = [np.uint64(1), np.uint64(2), np.uint64(4), np.uint64(8), np.uint64(16), np.uint64(32), np.uint64(64), np.uint64(128), np.uint64(256), np.uint64(512), np.uint64(1024), np.uint64(2048), np.uint64(4096), np.uint64(8192), np.uint64(16384), np.uint64(32768), np.uint64(65536), np.uint64(131072), np.uint64(262144), np.uint64(524288), np.uint64(1048576), np.uint64(2097152), np.uint64(4194304), np.uint64(8388608), np.uint64(16777216), np.uint64(33554432), np.uint64(67108864), np.uint64(134217728), np.uint64(268435456), np.uint64(536870912), np.uint64(1073741824), np.uint64(2147483648), np.uint64(4294967296), np.uint64(8589934592), np.uint64(17179869184), np.uint64(34359738368), np.uint64(68719476736), np.uint64(137438953472), np.uint64(274877906944), np.uint64(549755813888), np.uint64(1099511627776), np.uint64(2199023255552), np.uint64(4398046511104), np.uint64(8796093022208), np.uint64(17592186044416), np.uint64(35184372088832), np.uint64(70368744177664), np.uint64(140737488355328), np.uint64(281474976710656), np.uint64(562949953421312), np.uint64(1125899906842624), np.uint64(2251799813685248), np.uint64(4503599627370496), np.uint64(9007199254740992), np.uint64(18014398509481984), np.uint64(36028797018963968), np.uint64(72057594037927936), np.uint64(144115188075855872), np.uint64(288230376151711744), np.uint64(576460752303423488), np.uint64(1152921504606846976), np.uint64(2305843009213693952), np.uint64(4611686018427387904), np.uint64(9223372036854775808)]



class Engine:
    def __init__(self):
        # 8 Bitboards to save the state
        self.white = np.uint64(65535)
        self.black = np.uint64(18446462598732840960)
        self.pawn = np.uint64(71776119061282560)
        self.knight = np.uint64(4755801206503243842)
        self.rook = np.uint64(9295429630892703873)
        self.bishop = np.uint64(2594073385365405732)
        self.queen = np.uint64(576460752303423496)
        self.king = np.uint64(1152921504606846992)
        # True: Whites' turn, false: black's turn
        self.turn = True
        # stores if a pawn did a double move that round
        self.double_pawn = np.uint64(0)
        # stores move history: (move_from, move_to, Name of removed figure / None, if has_moved has changed (boolean), if move was castling(boolean))
        self.move_history = []
        # Rooks and kings that have not moved
        self.not_moved = np.uint64(10448351135499550865)
        self.count_moves = 0
        self.count_half_moves = 0

    def state_helper_check_legal(self):
        if self.turn:
            king = self.king & self.black
        else:
            king = self.king & self.white

        self.turn = not self.turn

        thread = self.check_is_attacked(king)

        self.turn = not self.turn

        if thread != 0:
            return False, thread
        return True, thread
    
    def state_helper_check_move_king(self, field):
        move, attack, _, en_passon = self.check_move_king(field)
        
        
        if self.turn:
            rooks = self.white & self.rook
        else:
            rooks = self.black & self.rook

        castling = np.uint(0)

        while rooks:
            field_num = int(rooks)
            field_num = field_num.bit_length()-1
            move_from = field_mask[field_num]
            rooks ^= move_from

            if self.check_castling(move_from):
                castling = castling | move_from

        return move, attack, castling, en_passon
    
    def state_helper_make_move_king(self, move_from, move_to, move, attack, en_passon, castling):

        if move_to & castling != 0:
            temp = move_to
            castling = move_from
            move_to = move_from
            move_from = temp
            

        self.make_moves_all(move_from, move_to, move, attack, en_passon, castling)

        
    # Takes unsigned 64 int and prints it out. Input one or a Tuple of ints
    def print_board(self, boards):
        bin_boards = []

        if isinstance(boards, tuple):
            length = len(boards)
            for i in range(0, length):
                bin_boards.append(bin(np.uint64(boards[i]))[2:].zfill(64))
        else:
            length = 1
            bin_boards.append(bin(np.uint64(boards))[2:].zfill(64))

        print("  ", end="")
        for i in range(0, length):
            print("ABCDEFGH", end="")
            print("   ", end="")

        print("\n8 ", end="")
        for i in range(0, length):
            print(bin_boards[i][7::-1], end="")
            print(" 8 ", end="")

        print("\n7 ", end="")
        for i in range(0, length):
            print(bin_boards[i][15:7:-1], end="")
            print(" 7 ", end="")

        print("\n6 ", end="")
        for i in range(0, length):
            print(bin_boards[i][23:15:-1], end="")
            print(" 6 ", end="")

        print("\n5 ", end="")
        for i in range(0, length):
            print(bin_boards[i][31:23:-1], end="")
            print(" 5 ", end="")

        print("\n4 ", end="")
        for i in range(0, length):
            print(bin_boards[i][39:31:-1], end="")
            print(" 4 ", end="")

        print("\n3 ", end="")
        for i in range(0, length):
            print(bin_boards[i][47:39:-1], end="")
            print(" 3 ", end="")

        print("\n2 ", end="")
        for i in range(0, length):
            print(bin_boards[i][55:47:-1], end="")
            print(" 2 ", end="")

        print("\n1 ", end="")
        for i in range(0, length):
            print(bin_boards[i][64:55:-1], end="")
            print(" 1 ", end="")

        print("\n  ", end="")
        for i in range(0, length):
            print("ABCDEFGH", end="")
            print("   ", end="")

        print("")

    # prints the state bitboards
    def print_state(self):
        print("  white      black      pawn       rook       knight     bishop     queen      king     ")
        self.print_board((self.white, self.black, self.pawn, self.rook, self.knight, self.bishop, self.queen, self.king))

    def move_colour(self, move_from, move_to):
        if self.turn:
            self.white = (self.white ^ move_from) | move_to
        else:
            self.black = (self.black ^ move_from) | move_to

    # removes the figure at a field
    def remove_fig(self, field):
        if field & self.white != 0:
            self.white = self.white ^ field
        else:
            self.black = self.black ^ field
        if field & self.pawn != 0:
            self.pawn = self.pawn ^ field
            return 0
        if field & self.rook != 0:
            self.rook = self.rook ^ field
            return 1
        if field & self.knight != 0:
            self.knight = self.knight ^ field
            return 2
        if field & self.bishop != 0:
            self.bishop = self.bishop ^ field
            return 3
        if field & self.queen != 0:
            self.queen = self.queen ^ field
            return 4

    def store_move(self, move_from, move_to, removed, move_type):
        self.move_history.append(
            (move_from, move_to, removed, move_type, self.double_pawn, self.not_moved)
        )

    # gets last move from move_history and restores state
    def unmake_move(self):
        last_move = self.move_history.pop()
        move_from = last_move[0]
        move_to = last_move[1]
        removed = last_move[2]
        move_type = last_move[3]
        self.double_pawn = last_move[4]
        self.turn = not self.turn

        if move_type == "move":
            self.not_moved = last_move[5]

            if self.turn:
                self.white = (self.white ^ move_to) | move_from
            else:
                self.black = (self.black ^ move_to) | move_from

            if move_to & self.pawn != 0:
                self.pawn = (self.pawn ^ move_to) | move_from
            if move_to & self.rook != 0:
                self.rook = (self.rook ^ move_to) | move_from
            if move_to & self.knight != 0:
                self.knight = (self.knight ^ move_to) | move_from
            if move_to & self.bishop != 0:
                self.bishop = (self.bishop ^ move_to) | move_from
            if move_to & self.queen != 0:
                self.queen = (self.queen ^ move_to) | move_from
            if move_to & self.king != 0:
                self.king = (self.king ^ move_to) | move_from

            return

        if move_type == "attack":
            self.not_moved = last_move[5]

            if self.turn:
                self.white = (self.white ^ move_to) | move_from
            else:
                self.black = (self.black ^ move_to) | move_from

            if move_to & self.pawn != 0:
                self.pawn = (self.pawn ^ move_to) | move_from
            if move_to & self.rook != 0:
                self.rook = (self.rook ^ move_to) | move_from
            if move_to & self.knight != 0:
                self.knight = (self.knight ^ move_to) | move_from
            if move_to & self.bishop != 0:
                self.bishop = (self.bishop ^ move_to) | move_from
            if move_to & self.queen != 0:
                self.queen = (self.queen ^ move_to) | move_from
            if move_to & self.king != 0:
                self.king = (self.king ^ move_to) | move_from

            if self.turn:
                self.black = self.black | move_to
            else:
                self.white = self.white | move_to

            if removed == 0:
                self.pawn = self.pawn | move_to
            if removed == 1:
                self.rook = self.rook | move_to
            if removed == 2:
                self.knight = self.knight | move_to
            if removed == 3:
                self.bishop = self.bishop | move_to
            if removed == 4:
                self.queen = self.queen | move_to

            return

        if move_type == "castling":
            self.not_moved = last_move[5]

            king_l = move_from << np.uint(2) & mask_notAB
            king_r = move_from >> np.uint(1) & mask_notH

            rook_l = king_l << np.uint(1)
            rook_r = king_r >> np.uint(1)

            self.king = (self.king ^ king_r ^ king_l) | move_to
            self.rook = (self.rook ^ rook_r ^ rook_l) | move_from

            if self.turn:
                self.white = (self.white ^ king_r ^ king_l) | move_to
                self.white = (self.white ^ rook_r ^ rook_l) | move_from
            else:
                self.black = (self.black ^ king_r ^ king_l) | move_to
                self.black = (self.black ^ rook_r ^ rook_l) | move_from

        if move_type == "en_passon":
            self.not_moved = last_move[5]

            if self.turn:
                self.white = (self.white ^ move_to) | move_from
                self.black = self.black | removed
            else:
                self.black = (self.black ^ move_to) | move_from
                self.white = self.white | removed

            self.pawn = (self.pawn ^ move_to) | move_from
            self.pawn = self.pawn | removed


    # Returns attack pattern of knight
    def attack_pattern_knight(self, field):
        attack_right_1 = (field << np.uint(17) | field >> np.uint(15)) & mask_notA
        attack_left_1 = (field << np.uint(15) | field >> np.uint(17)) & mask_notH
        attack_right_2 = (field << np.uint(10) | field >> np.uint(6)) & mask_notAB
        attack_left_2 = (field << np.uint(6) | field >> np.uint(10)) & mask_notGH

        attack = attack_right_1 | attack_left_1 | attack_right_2 | attack_left_2
        return attack

    # gets the pos and check all posible moves of a knight
    def check_move_knight(self, field):
        move = self.attack_pattern_knight(field)

        if self.turn:
            attack = move & self.black
        else:
            attack = move & self.white

        move = move ^ (move & (self.white | self.black))

        return move, attack, np.uint(0), np.uint(0)

    # execute moves and attacks of the knight
    def move_knight(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.knight = (self.knight ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.knight = (self.knight ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

    # sreturns attack and moves of bishop
    def attack_pattern_bishop(self, field):
        move_no = field << np.uint(9) & mask_notA
        attack_no = move_no
        move_no = (move_no & (self.white | self.black)) ^ move_no

        move_sw = field >> np.uint(9) & mask_notH
        attack_sw = move_sw
        move_sw = (move_sw & (self.white | self.black)) ^ move_sw

        move_nw = field << np.uint(7) & mask_notH
        attack_nw = move_nw
        move_nw = (move_nw & (self.white | self.black)) ^ move_nw

        move_so = field >> np.uint(7) & mask_notA
        attack_so = move_so
        move_so = (move_so & (self.white | self.black)) ^ move_so

        for i in range(6):
            move_no = move_no | ((move_no << np.uint(9)) & mask_notA)
            move_no = (move_no & (self.white | self.black)) ^ move_no

            move_sw = move_sw | ((move_sw >> np.uint(9)) & mask_notH)
            move_sw = (move_sw & (self.white | self.black)) ^ move_sw

            move_nw = move_nw | (move_nw << np.uint(7) & mask_notH)
            move_nw = (move_nw & (self.white | self.black)) ^ move_nw

            move_so = move_so | (move_so >> np.uint(7) & mask_notA)
            move_so = (move_so & (self.white | self.black)) ^ move_so

        attack_no = (attack_no | move_no << np.uint(9) & mask_notA) ^ move_no

        attack_sw = (attack_sw | move_sw >> np.uint(9) & mask_notH) ^ move_sw

        attack_nw = (attack_nw | move_nw << np.uint(7) & mask_notH) ^ move_nw

        attack_so = (attack_so | move_so >> np.uint(7) & mask_notA) ^ move_so

        attack = attack_sw | attack_no | attack_nw | attack_so
        move = move_sw | move_no | move_nw | move_so

        return move, attack

    # saves attack and moves of bishop
    def check_move_bishop(self, field):
        move, attack = self.attack_pattern_bishop(field)

        if self.turn:
            attack = attack & self.black
        else:
            attack = attack & self.white

        return move, attack, np.uint(0), np.uint(0)

    # moves bishop
    def move_bishop(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.bishop = (self.bishop ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.bishop = (self.bishop ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

    def attack_pattern_pawn(self, field):
        
        if self.turn:
            attack_right = (field & mask_notH) << np.uint(9)
            attack_left = (field & mask_notA) << np.uint(7)
        else:
            attack_right = (field & mask_notA) >> np.uint(9)
            attack_left = (field & mask_notH) >> np.uint(7)

        return attack_left | attack_right

    def move_pattern_pawn(self, field):
        if self.turn:
            move = field << np.uint(8)
            if (
                (field & mask_R2 != 0)
                and ((move & (self.black | self.white)) == 0)
                and ((field << np.uint(16)) & (self.black | self.white)) == 0
            ):
                move |= move << np.uint(8)
            move = move ^ (move & (self.black | self.white))
            return move

        else:
            move = field >> np.uint(8)
            if (
                (field & mask_R7 != 0)
                and ((move & (self.black | self.white)) == 0)
                and ((field >> np.uint(16)) & (self.black | self.white)) == 0
            ):
                move = move | move >> np.uint(8)
            move = move ^ (move & (self.black | self.white))
            return move

    def check_move_pawn(self, field):
        move = self.move_pattern_pawn(field)
        attack = self.attack_pattern_pawn(field)

        if self.turn:
            attack = attack & self.black
            colour = self.black
        else:
            attack = attack & self.white
            colour = self.white

        en_passon = (field << np.uint(1) & mask_notA) | (
            field >> np.uint(1) & mask_notH
        )
        en_passon = self.double_pawn & en_passon & colour
        en_passon = (en_passon << np.uint(8) & mask_R6) | (
            en_passon >> np.uint(8) & mask_R3
        )

        return move, attack, en_passon, np.uint(0)

    def move_pawn(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.pawn = (self.pawn ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")

            if self.turn:
                self.double_pawn = (move_from << np.uint(16) & mask_R4 & move_to)
            else:
                self.double_pawn = move_from >> np.uint(16) & move_to & mask_R5
            self.turn = not self.turn
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.pawn = (self.pawn ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

        if move_to & en_passon != 0:
            removed = self.remove_fig(self.double_pawn)
            self.pawn = (self.pawn ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, self.double_pawn, "en_passon")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

    def check_move_queen(self, field):
        move_rook, attack_rook = self.attack_pattern_rook(field)
        move_bishop, attack_bishop = self.attack_pattern_bishop(field)

        move = move_bishop | move_rook
        attack = attack_bishop | attack_rook

        if self.turn:
            attack = attack & self.black
        else:
            attack = attack & self.white

        return move, attack, np.uint(0), np.uint(0)

    def move_queen(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.queen = (self.queen ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.queen = (self.queen ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            return

    def attack_pattern_rook(self, field):
        move_right = field << np.uint(1) & mask_notA
        attack_right = move_right
        move_right = (move_right & (self.white | self.black)) ^ move_right

        move_left = field >> np.uint(1) & mask_notH
        attack_left = move_left
        move_left = (move_left & (self.white | self.black)) ^ move_left

        move_up = field << np.uint(8)
        attack_up = move_up
        move_up = (move_up & (self.white | self.black)) ^ move_up

        move_down = field >> np.uint(8)
        attack_down = move_down
        move_down = (move_down & (self.white | self.black)) ^ move_down

        for i in range(6):
            move_right = move_right | ((move_right << np.uint(1)) & mask_notA)
            move_right = (move_right & (self.white | self.black)) ^ move_right

            move_left = move_left | ((move_left >> np.uint(1)) & mask_notH)
            move_left = (move_left & (self.white | self.black)) ^ move_left

            move_up = move_up | (move_up << np.uint(8))
            move_up = (move_up & (self.white | self.black)) ^ move_up

            move_down = move_down | (move_down >> np.uint(8))
            move_down = (move_down & (self.white | self.black)) ^ move_down

        attack_right = (
            attack_right | move_right << np.uint(1) & mask_notA
        ) ^ move_right

        attack_left = (attack_left | move_left >> np.uint(1) & mask_notH) ^ move_left

        attack_up = (attack_up | move_up << np.uint(8)) ^ move_up

        attack_down = (attack_down | move_down >> np.uint(8)) ^ move_down

        attack = attack_left | attack_right | attack_up | attack_down
        move = move_left | move_right | move_up | move_down

        return move, attack

    def check_castling(self, field):
        field = field & self.not_moved
        move_right = field << np.uint(1) & mask_notA
        attack_right = move_right
        move_right = (move_right & (self.white | self.black)) ^ move_right

        move_left = field >> np.uint(1) & mask_notH
        attack_left = move_left
        move_left = (move_left & (self.white | self.black)) ^ move_left

        for i in range(2):
            move_right = move_right | ((move_right << np.uint(1)) & mask_notA)
            move_right = (move_right & (self.white | self.black)) ^ move_right

            move_left = move_left | ((move_left >> np.uint(1)) & mask_notH)
            move_left = (move_left & (self.white | self.black)) ^ move_left

        attack_right = (
            attack_right | move_right << np.uint(1) & mask_notA
        ) ^ move_right
        attack_left = (attack_left | move_left >> np.uint(1) & mask_notH) ^ move_left

        attack = attack_left | attack_right
        move = move_left | move_right

        moves = attack | move

        if self.check_is_attacked(moves) != 0:
            return np.uint(0)

        castling = attack & self.king & self.not_moved

        return castling

    def check_move_rook(self, field):
        move, attack = self.attack_pattern_rook(field)

        if self.turn:
            attack = attack & self.black
        else:
            attack = attack & self.white

        castling = self.check_castling(field)

        return move, attack, np.uint(0), castling

    # moves rook
    def move_rook(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.rook = (self.rook ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            self.not_moved = self.not_moved ^ (self.not_moved & move_from)
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.rook = (self.rook ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            self.not_moved = self.not_moved ^ (self.not_moved & move_from)
            return

        # castling
        if move_to & castling != 0:
            king_new = (move_from >> np.uint(1) | move_from << np.uint(2)) & mask_R1_R8
            self.king = (self.king ^ move_to) | king_new

            rook_new = (move_from >> np.uint(2) | move_from << np.uint(3)) & mask_R1_R8
            self.rook = (self.rook ^ move_from) | rook_new

            if self.turn:
                self.white = self.white ^ (move_to | move_from)
                self.white = self.white | king_new | rook_new
            else:
                self.black = self.black ^ (move_to | move_from)
                self.black = self.black | king_new | rook_new

            removed = None
            self.store_move(move_from, move_to, removed, "castling")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            self.not_moved = self.not_moved ^ move_from ^ move_to
            return

    # returns attack pattern of king
    def attack_pattern_king(self, field):
        attack_right = field << np.uint(1) & mask_notA
        attack_left = field >> np.uint(1) & mask_notH
        attack_row = attack_right | attack_left | field
        attack = attack_row | attack_row << np.uint(8) | attack_row >> np.uint(8)

        return attack ^ field

    def check_move_king(self, field):
        attack = self.attack_pattern_king(field)

        move = attack & (self.white | self.black)
        move = attack ^ move

        if self.turn:
            attack = attack & self.black
        else:
            attack = attack & self.white

        return move, attack, np.uint(0), np.uint(0)

    def move_king(self, move_from, move_to, move, attack, en_passon, castling):
        if move_to & move != 0:
            self.king = (self.king ^ move_from) | move_to
            self.move_colour(move_from, move_to)
            removed = None

            self.store_move(move_from, move_to, removed, "move")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            self.not_moved = self.not_moved ^ (self.not_moved & move_from)
            return

        if move_to & attack != 0:
            removed = self.remove_fig(move_to)
            self.king = (self.king ^ move_from) | move_to
            self.move_colour(move_from, move_to)

            self.store_move(move_from, move_to, removed, "attack")
            self.turn = not self.turn
            self.double_pawn = np.uint64(0)
            self.not_moved = self.not_moved ^ (self.not_moved & move_from)
            return

    def check_is_attacked(self, field):
        pawn = self.attack_pattern_pawn(field)
        _, rook = self.attack_pattern_rook(field)
        knight = self.attack_pattern_knight(field)
        _, bishop = self.attack_pattern_bishop(field)
        king = self.attack_pattern_king(field)


        pawn = pawn & self.pawn
        rook = rook & (self.rook | self.queen)
        knight = knight & self.knight
        bishop = bishop & (self.bishop | self.queen)
        king = king & self.king

        thread = pawn | rook | knight | bishop | king

        if self.turn:
            thread = thread & self.black
        else:
            thread = thread & self.white

        return thread

    def copy_state(self, game_state):
        self.white = game_state.white
        self.black = game_state.black
        self.pawn = game_state.pawn
        self.knight = game_state.knight
        self.rook = game_state.rook
        self.bishop = game_state.bishop
        self.queen = game_state.queen
        self.king = game_state.king
        self.move_history = []
        self.double_pawn = game_state.double_pawn
        self.not_moved = game_state.not_moved
        self.turn = game_state.turn

    def calculate_open_lines(self):
        return elo_functions.calculate_open_lines(self)

    def calculate_doubled_pawns(self):
        return elo_functions.calculate_doubled_pawns(self)

    def calculate_center_control(self, bitboard):
        return elo_functions.calculate_center_control(self, bitboard)

    def is_opening_phase(self):
        return elo_functions.is_opening_phase(self)

    def is_endgame_phase(self):
        return elo_functions.is_endgame_phase(self)

    def count_figures(self):
        return elo_functions.count_figures(self)

    def get_score(self):
        return elo_functions.get_score(self)

    def check_legal(self):
        if self.turn:
            king = self.king & self.black
        else:
            king = self.king & self.white

        self.turn = not self.turn

        thread = self.check_is_attacked(king)

        self.turn = not self.turn

        if thread != 0:
            return False
        else:
            return True

    def check_moves_all(self, field):
        if field & self.pawn != 0:
            return self.check_move_pawn(field)
        if field & self.rook != 0:
            return self.check_move_rook(field)
        if field & self.knight != 0:
            return self.check_move_knight(field)
        if field & self.bishop != 0:
            return self.check_move_bishop(field)
        if field & self.queen != 0:
            return self.check_move_queen(field)
        if field & self.king != 0:
            return self.check_move_king(field)

    def make_moves_all(self, move_from, move_to, move, attack, en_passon, castling):
        if move_from & self.pawn != 0:
            self.move_pawn(move_from, move_to, move, attack, en_passon, castling)
            return
        if move_from & self.rook != 0:
            self.move_rook(move_from, move_to, move, attack, en_passon, castling)
            return
        if move_from & self.knight != 0:
            self.move_knight(move_from, move_to, move, attack, en_passon, castling)
            return
        if move_from & self.bishop != 0:
            self.move_bishop(move_from, move_to, move, attack, en_passon, castling)
            return
        if move_from & self.queen != 0:
            self.move_queen(move_from, move_to, move, attack, en_passon, castling)
            return
        if move_from & self.king != 0:
            self.move_king(move_from, move_to, move, attack, en_passon, castling)
            return

    def generate_move(self):
        best_move = []
        
        colour = self.black
        beta = math.inf

        for i in range(64):
            move_from = np.uint(1) << np.uint(i)

            if move_from & colour != 0:

                move, attack, en_passon, castling = self.check_moves_all(move_from)
                moves = move | attack | en_passon | castling

                for j in range(64):
                    move_to = np.uint(1) << np.uint(j)

                    if move_to & moves != 0:

                        # self.print_board((move_from, move_to, self.not_moved))
                        self.make_moves_all(move_from, move_to, move, attack, en_passon, castling)
                        # self.print_state()
                        score = self.get_score()
                        # self.unmake_move()
                        # self.print_board((move_from, move_to, self.not_moved))
                        print(self.check_legal())
                        if self.check_legal():
                            if score == beta:
                                best_move = [(move_from, move_to)]
                            if score < beta:
                                beta = score
                                best_move.append((move_from, move_to))
                        self.unmake_move()
        
        data = random.choice(best_move)
        return data[0], data[1], beta

    def iterativ(self):
        alpha = -math.inf
        beta = math.inf

        time_limit = 6

        if elo_functions.is_endgame_phase(self) or elo_functions.is_opening_phase(self):
            time_limit = 4
        

        end_time = perf_counter() + time_limit

        depth = 1

        last_score = 0
        last_best_moves = []

        print("------------------------------------------------")
        
        if self.turn:
            while(1):
                start = perf_counter()
                score, best_moves, did_break, counter = self.alphaBetaMax(alpha, beta, depth, end_time)
                end = perf_counter()
                if did_break:
                    break
                last_score = score
                last_best_moves = best_moves
                depth += 1
                print(f"Suchtiefe: {depth-1}")
                print(f"Suchzeit: {end-start}")
                print(f"Untersuchte Zustände: {counter}")
                print("Beste Züge:")
                print(best_moves)
                print("------------------------------------------------")

                if best_moves == None or score >= 9999999:
                    score = last_score
                    best_moves = last_best_moves
                    break

        else:
            while(1):
                start = perf_counter()
                score, best_moves, did_break, counter = self.alphaBetaMin(alpha, beta, depth, end_time)
                end = perf_counter()
                if did_break:
                    break
                last_score = score
                last_best_moves = best_moves
                depth += 1
                print(f"Suchtiefe: {depth-1}")
                print(f"Suchzeit: {end-start}")
                print(f"Untersuchte Zustände: {counter}")
                print("Beste Züge:")
                print(best_moves)
                print("------------------------------------------------")

                if best_moves == None or score <= -9999999:
                    score = last_score
                    best_moves = last_best_moves
                    break
 
        data = random.choice(last_best_moves)

        return data[0], data[1], last_score, depth-1, 

    def alphaBetaMax(self, alpha, beta, depth, end_time):
        if perf_counter() > end_time:
            return None, None, True, 0
        
        if depth == 0:
            return self.get_score(), None, False, 0
        
        if self.turn:
            colour = self.white
        else:
            colour = self.black

        best_moves = []
        counter = 0

        while colour:
            field_num = int(colour)
            field_num = field_num.bit_length()-1
            move_from = field_mask[field_num]
            colour ^= move_from

            move, attack, en_passon, castling = self.check_moves_all(move_from)
            moves = move | attack | en_passon | castling

            while moves:
                field_num = int(moves)
                field_num = field_num.bit_length()-1
                move_to = field_mask[field_num]
                moves ^= move_to

                counter += 1
                #testing
                # s1 = self.compareState()

                self.make_moves_all(move_from, move_to, move, attack, en_passon, castling)
                score = -math.inf
                if self.check_legal():
                    score, next_moves, break_condition, leaf_counter = self.alphaBetaMin( alpha, beta, depth-1, end_time)
                    counter += leaf_counter
                    if break_condition:
                        return None, None, True, counter
                    
                self.unmake_move()

                # testing
                # s2 = self.compareState()
                # if s1 != s2:
                #     print("--------------------before-------------------")
                #     self.print_board(s1[1])
                #     self.print_board((move_from, move_to, move, attack, en_passon, castling))
                #     print("--------------------after-------------------")
                #     self.print_board(s2[1])
                #     print("fehler")
                #     self.find_error(s1, self.compareState())
                #     exit()

                if score >= beta:
                    return beta, None, False, counter
                # if score == alpha:
                #     best_moves.append((move_from, move_to))
                if score > alpha:
                    alpha = score
                    best_moves = [(move_from, move_to)]
                
        if alpha == math.inf:
            return -9999999999, None, False, counter
        return alpha, best_moves, False, counter


    def alphaBetaMin(self, alpha, beta, depth, end_time):
        if perf_counter() > end_time:
            return None, None, True, 0

        if depth == 0:
            # x = self.get_score()
            # if x > 99999:
            #     print(x)
            #     self.print_state()
            return self.get_score(), None, False, 0
        
        if self.turn:
            colour = self.white
        else:
            colour = self.black

        best_moves = []
        counter = 0

        while colour:
            field_num = int(colour)
            field_num = field_num.bit_length()-1
            move_from = field_mask[field_num]
            colour ^= move_from

            move, attack, en_passon, castling = self.check_moves_all(move_from)
            moves = move | attack | en_passon | castling

            while moves:
                field_num = int(moves)
                field_num = field_num.bit_length()-1
                move_to = field_mask[field_num]
                moves ^= move_to

        
                counter += 1
                #testing
                # s1 = self.compareState()
                
                self.make_moves_all(move_from, move_to, move, attack, en_passon, castling)
                
                score = math.inf
                if self.check_legal():
                    score, next_moves, break_condition, leaf_counter = self.alphaBetaMax( alpha, beta, depth-1, end_time)
                    counter += leaf_counter
                    if break_condition:
                        return None, None, True, counter
                    
                self.unmake_move()

                #testing
                # s2 = self.compareState()
                # if s1 != s2:
                #     print("--------------------before-------------------")
                #     self.print_board(s1[1])
                #     self.print_board((move_from, move_to, move, attack, en_passon, castling))
                #     print("--------------------after-------------------")
                #     self.print_board(s2[1])
                #     print("fehler")
                #     self.find_error(s1, self.compareState())
                #     exit()

                

                if score <= alpha:
                    return alpha, None, False, counter
                # if score == beta:
                #     best_moves.append((move_from, move_to))
                if score < beta:
                    beta = score
                    best_moves = [(move_from, move_to)]
        
        if beta == math.inf:
            return 9999999999, None, False, counter
        return beta, best_moves, False, counter



    def compareState(self):
        return self.turn, (self.white, self.black, self.pawn, self.rook, self.knight, self.bishop, self.queen, self.king, self.double_pawn, self.not_moved)


    def find_error(self, x, y):
        if x[0] != y[0]:
            print(x[0],y[0])
        
        for i in range (10):
            if x[1][i] != y[1][i]:
                if i == 0:
                    print("White")
                if i == 1:
                    print("Black")
                if i == 2:
                    print("Pawn")
                if i == 3:
                    print("Rook")
                if i == 4:
                    print("Knight")
                if i == 5:
                    print("Bishop")
                if i == 6:
                    print("Queen")
                if i == 7:
                    print("King")
                if i == 8:
                    print("Double Pawn")
                if i == 9:
                    print("Not Moved")
                self.print_board((x[1][i], y[1][i]))

    
    def check_game_end(self):
        if self.turn:
            winner = "Black"
        else: 
            winner = "White"

        ## check kill of the hill condition
        if self.king & mask_Hill != 0:
            return False, winner+" won:", "King of the hill condition!"
        
        self.turn = not self.turn
        if self.no_moves():
            if self.check_legal():
                self.turn = not self.turn
                return False, winner+ " won:", "Stalemate! Draw!"
            
            self.turn = not self.turn
            return False, winner+" won:", "Checkmate!"
        
        self.turn = not self.turn
        return True, None, None
    
    def no_moves(self):
        
        if self.turn:
            colour = self.white
        else:
            colour = self.black

        while colour:
            field_num = int(colour)
            field_num = field_num.bit_length()-1
            move_from = field_mask[field_num]
            colour ^= move_from

            move, attack, en_passon, castling = self.check_moves_all(move_from)
            moves = move | attack | en_passon | castling

            while moves:
                field_num = int(moves)
                field_num = field_num.bit_length()-1
                move_to = field_mask[field_num]
                moves ^= move_to

                self.make_moves_all(move_from, move_to, move, attack, en_passon, castling)
                if self.check_legal():
                    self.unmake_move()
                    return False

        return True
    
