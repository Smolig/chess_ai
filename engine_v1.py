import numpy as np
import math
import random
from time import sleep

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
        # stores the moves, attacks,... of the selected piece
        self.move = np.uint64(0)
        self.attack = np.uint64(0)
        self.castling = np.uint64(0)
        self.en_passon = np.uint64(0)
        # stores if a pawn did a double move that round
        self.double_pawn = np.uint64(0)
        self.fig_pos = np.uint64(0)
        self.thread = np.uint64(0)
        # stores figures that attack castling
        self.castling_block = np.uint64(0)
        # stores move history: (move_from, move_to, Name of removed figure / None, if has_moved has changed (boolean), if move was castling(boolean))
        self.move_history = []
        # Rooks and kings that have not moved
        self.not_moved = np.uint64(10448351135499550865)
        # Toggle Ui
        self.game_going = True
        self.main_menue = True
        # True: Player vs Player, False Player vs Ai
        self.game_mode = True

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
        print(
            "  white      black      pawn       rook       knight     bishop     queen      king     "
        )
        self.print_board(
            (
                self.white,
                self.black,
                self.pawn,
                self.rook,
                self.knight,
                self.bishop,
                self.queen,
                self.king,
            )
        )

    # returns the names and the fig boards
    def get_all_fig(self):
        fig_name = [
            "pawn_w",
            "rook_w",
            "knight_w",
            "bishop_w",
            "queen_w",
            "king_w",
            "pawn_b",
            "rook_b",
            "knight_b",
            "bishop_b",
            "queen_b",
            "king_b",
        ]
        fig_pos = [
            self.pawn & self.white,
            self.rook & self.white,
            self.knight & self.white,
            self.bishop & self.white,
            self.queen & self.white,
            self.king & self.white,
            self.pawn & self.black,
            self.rook & self.black,
            self.knight & self.black,
            self.bishop & self.black,
            self.queen & self.black,
            self.king & self.black,
        ]

        return fig_name, fig_pos

    # returns board with all fig
    def get_all(self):
        return self.white | self.black

    # gets a field and checks the type of fig on the field, returns the name of the fig
    def check_field(self, field):
        if field & self.pawn != 0:
            return "pawn"
        if field & self.rook != 0:
            return "rook"
        if field & self.knight != 0:
            return "knight"
        if field & self.bishop != 0:
            return "bishop"
        if field & self.queen != 0:
            return "queen"
        if field & self.king != 0:
            return "king"

    # get moves and attacks, filters it according to player turn and writes it in the state
    def write_moves(self, move, attack, field):
        if self.turn:
            self.attack = attack & self.black
        else:
            self.attack = attack & self.white

        self.move = (move & (self.white | self.black)) ^ move
        self.fig_pos = field

    # checks if the position is legal
    def check_legal(self):
        if self.turn:
            king = self.king & self.white
        else:
            king = self.king & self.black

        self.thread = self.check_is_attacked(king)
        if self.thread == 0:
            return True
        else:
            return False

    # gets last move from move_history and restores state
    def unmake_move(self):
        last_move = self.move_history.pop()
        move_from = last_move[0]
        move_to = last_move[1]
        removed = last_move[2]
        has_moved = last_move[3]
        was_castling = last_move[4]

        # moves the piece back to its last position
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

        # restores removed pieces
        if removed != None:
            if not self.turn:
                self.white = self.white | move_to
            else:
                self.black = self.black | move_to

        if removed == "pawn":
            self.pawn = self.pawn | move_to
        if removed == "rook":
            self.rook = self.rook | move_to
        if removed == "knight":
            self.knight = self.knight | move_to
        if removed == "bishop":
            self.bishop = self.bishop | move_to
        if removed == "queen":
            self.queen = self.queen | move_to

        # changes the has_moved state back
        if has_moved:
            self.not_moved = self.not_moved | move_from

        # undoes castling move
        if was_castling:
            king_old = (move_to >> np.uint(3) | move_to << np.uint(4)) & mask_R1_R8
            king_new = move_to >> np.uint(1) | move_to << np.uint(2) & mask_R1_R8
            self.king = (self.king ^ king_new) | king_old

            rook_new = (move_to >> np.uint(2) | move_to << np.uint(3)) & mask_R1_R8
            self.rook = (self.rook ^ rook_new) | move_to

            if move_to & mask_R1 != 0:
                self.white = (self.white ^ (rook_new | king_new)) | (king_old | move_to)
            elif move_to & mask_R8 != 0:
                self.black = (self.black ^ (rook_new | king_new)) | (king_old | move_to)

    # removes the figure at a field
    def remove_fig(self, field):
        if field & self.white != 0:
            self.white = self.white ^ field
        else:
            self.black = self.black ^ field
        if field & self.pawn != 0:
            self.pawn = self.pawn ^ field
            return "pawn"
        if field & self.rook != 0:
            self.rook = self.rook ^ field
            return "rook"
        if field & self.knight != 0:
            self.knight = self.knight ^ field
            return "knight"
        if field & self.bishop != 0:
            self.bishop = self.bishop ^ field
            return "bishop"
        if field & self.queen != 0:
            self.queen = self.queen ^ field
            return "queen"

    def store_move(self, field, removed, has_moved, was_castling):
        self.move_history.append(
            (self.fig_pos, field, removed, has_moved, was_castling)
        )

    # Returns attack pattern of pawn depending on player turn
    def attack_pattern_pawn(self, field):
        if self.turn:
            attack_right = (field & mask_notH) << np.uint(9)
            attack_left = (field & mask_notA) << np.uint(7)
        else:
            attack_right = (field & mask_notA) >> np.uint(9)
            attack_left = (field & mask_notH) >> np.uint(7)

        return attack_left | attack_right

    # returns the move pattern of pawn depending on player turn
    def move_pattern_pawn(self, field):
        if field & self.white != 0:
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

    # gets the pos and check all posible moves of a pawn
    def check_move_pawn(self, field):
        self.en_passon = (field << np.uint(1) & mask_notA) | (
            field >> np.uint(1) & mask_notH
        )
        self.en_passon = self.double_pawn & self.en_passon
        self.en_passon = (self.en_passon << np.uint(8) & mask_R6) | (
            self.en_passon >> np.uint(8) & mask_R3
        )
        move = self.move_pattern_pawn(field)
        attack = self.attack_pattern_pawn(field)
        self.write_moves(move, attack, field)

    # moves colour from saved pos to field
    def move_colour(self, field):
        if self.turn:
            self.white = (self.white ^ self.fig_pos) | field
        else:
            self.black = (self.black ^ self.fig_pos) | field

    # execute moves and attacks of the pawn
    def move_pawn(self, field):
        # checks moves
        if field & self.move != 0:
            if self.turn:
                self.double_pawn = self.fig_pos << np.uint(16) & mask_R4 & field
            else:
                self.double_pawn = self.fig_pos >> np.uint(16) & field & mask_R5
            self.pawn = (self.pawn ^ self.fig_pos) | field
            self.move_colour(field)
            self.store_move(field, None, False, False)
            if not self.check_legal():
                self.unmake_move()

        # checks attacks
        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.pawn = (self.pawn ^ self.fig_pos) | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)
            if not self.check_legal():
                self.unmake_move()

        # checks en passon
        if field & self.en_passon != 0:
            removed = self.remove_fig(self.double_pawn)
            self.pawn = (self.pawn ^ self.fig_pos) | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)
            if not self.check_legal():
                self.unmake_move()

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
        attack = self.attack_pattern_knight(field)
        self.write_moves(attack, attack, field)

    # execute moves and attacks of the knight
    def move_knight(self, field):
        if field & self.move != 0:
            self.knight = self.knight ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, None, False, False)
            if not self.check_legal():
                self.unmake_move()

        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.knight = self.knight ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)
            if not self.check_legal():
                self.unmake_move()

    # Returns move and attack pattern of rook
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

    # checks moves, attacks, castling of roook
    def check_move_rook(self, field):
        move, attack = self.attack_pattern_rook(field)
        self.write_moves(move, attack, field)
        self.castling = self.check_castling(field)

    # moves rook
    def move_rook(self, field):
        # move
        if field & self.move != 0:
            self.rook = self.rook ^ self.fig_pos | field
            self.not_moved = self.not_moved ^ self.fig_pos
            self.move_colour(field)
            self.store_move(field, None, self.not_moved & self.fig_pos == 0, False)

            if not self.check_legal():
                self.unmake_move()

        # attack
        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.rook = self.rook ^ self.fig_pos | self.fig_pos
            self.not_moved = self.not_moved ^ self.fig_pos
            self.move_colour(field)
            self.store_move(field, removed, self.not_moved & self.fig_pos == 0, False)

            if not self.check_legal():
                self.unmake_move()

        # castling
        if field & self.castling != 0:
            king_new = (
                self.fig_pos >> np.uint(1) | self.fig_pos << np.uint(2)
            ) & mask_R1_R8
            self.king = (self.king ^ field) | king_new

            rook_new = (
                self.fig_pos >> np.uint(2) | self.fig_pos << np.uint(3)
            ) & mask_R1_R8
            self.rook = (self.rook ^ self.fig_pos) | rook_new

            if self.turn:
                self.white = self.white ^ (field | self.fig_pos)
                self.white = self.white | king_new | rook_new
            else:
                self.black = self.black ^ (field | self.fig_pos)
                self.black = self.black | king_new | rook_new

            self.store_move(self.fig_pos, None, False, True)

            # checks if all castling fields are not attacked

            attacker = self.check_is_attacked(self.fig_pos >> np.uint(3) & mask_R1_R8)
            attacker = attacker | self.check_is_attacked(
                self.fig_pos << np.uint(4) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                self.fig_pos >> np.uint(1) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                self.fig_pos >> np.uint(2) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                self.fig_pos << np.uint(3) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                self.fig_pos << np.uint(2) & mask_R1_R8
            )

            # if they are attacked the move is undone
            if attacker != 0:
                self.castling_block = attacker
                self.unmake_move()
            else:
                self.not_moved = self.not_moved ^ (self.fig_pos | field)

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
        self.write_moves(move, attack, field)

    # moves bishop
    def move_bishop(self, field):
        if field & self.move != 0:
            self.bishop = self.bishop ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, None, False, False)
            if not self.check_legal():
                self.unmake_move()

        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.bishop = self.bishop ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)
            if not self.check_legal():
                self.unmake_move()

    # saves moves, attacks of queen
    def check_move_queen(self, field):
        move_rook, attack_rook = self.attack_pattern_rook(field)
        move_bishop, attack_bishop = self.attack_pattern_bishop(field)
        self.write_moves(move_rook | move_bishop, attack_rook | attack_bishop, field)

    # moves queen
    def move_queen(self, field):
        if field & self.move != 0:
            self.queen = self.queen ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, None, False, False)
            if not self.check_legal():
                self.unmake_move()

        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.queen = self.queen ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)
            if not self.check_legal():
                self.unmake_move()

    # returns attack pattern of king
    def attack_pattern_king(self, field):
        attack_right = field << np.uint(1) & mask_notA
        attack_left = field >> np.uint(1) & mask_notH
        attack_row = attack_right | attack_left | field
        attack = attack_row | attack_row << np.uint(8) | attack_row >> np.uint(8)

        return attack ^ field

    # checks if a field is attacked, saves in thread
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

    # checks if castling is possible
    def check_castling(self, field):
        field = field & self.not_moved

        _, attack = self.attack_pattern_rook(field)

        attack = (attack & mask_R1_R8) & self.not_moved

        return attack

    # checks all possible move and if the moves are legal, saves legal moves, attacks
    def check_move_king(self, field):
        move_1 = field << np.uint(1) & mask_notA
        move_2 = field >> np.uint(1) & mask_notH
        move_3 = field << np.uint(9) & mask_notA
        move_4 = field << np.uint(7) & mask_notH
        move_5 = field << np.uint(8)
        move_6 = field >> np.uint(7) & mask_notA
        move_7 = field >> np.uint(9) & mask_notH
        move_8 = field >> np.uint(8)

        move = np.uint(0)

        for i in range(1, 9):
            executable = "move_" + str(i)
            move_x = eval(executable)

            if not self.check_is_attacked(move_x) != 0:
                if self.turn:
                    move_x = (move_x & self.white) ^ move_x
                else:
                    move_x = (move_x & self.black) ^ move_x

                if move_x != 0:
                    self.write_moves(move_x, move_x, field)
                    self.simulate_move_king(move_x)
                    if not self.check_legal():
                        move_x = np.uint(0)
                    self.unmake_move()

                move = move | move_x

        self.write_moves(move, move, field)
        self.castling = self.check_castling(field)

    # castling ignored moving king
    def simulate_move_king(self, field):
        if field & self.move != 0:
            self.king = self.king ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, None, False, False)

        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.king = self.king ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, removed, False, False)

    # actual moving king, without legal checks
    def move_king(self, field):
        if field & self.move != 0:
            self.king = self.king ^ self.fig_pos | field
            self.not_moved = self.not_moved ^ self.fig_pos
            self.move_colour(field)
            self.store_move(field, None, self.not_moved & self.fig_pos == 0, False)

        if field & self.attack != 0:
            removed = self.remove_fig(field)
            self.king = self.king ^ self.fig_pos | field
            self.move_colour(field)
            self.store_move(field, removed, self.not_moved & self.fig_pos == 0, False)

        if field & self.castling != 0:
            king_new = (field >> np.uint(1) | field << np.uint(2)) & mask_R1_R8
            self.king = (self.king ^ self.fig_pos) | king_new

            rook_new = (field >> np.uint(2) | field << np.uint(3)) & mask_R1_R8
            self.rook = (self.rook ^ field) | rook_new

            if self.turn:
                self.white = self.white ^ (field | self.fig_pos)
                self.white = self.white | king_new | rook_new
            else:
                self.black = self.black ^ (field | self.fig_pos)
                self.black = self.black | king_new | rook_new

            self.store_move(field, None, False, True)

            attacker = self.check_is_attacked(self.fig_pos)
            attacker = attacker | self.check_is_attacked(
                field >> np.uint(1) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                field >> np.uint(2) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                field << np.uint(3) & mask_R1_R8
            )
            attacker = attacker | self.check_is_attacked(
                field << np.uint(2) & mask_R1_R8
            )

            if attacker != 0:
                self.castling_block = attacker
                self.unmake_move()
            else:
                self.not_moved = self.not_moved ^ (self.fig_pos | field)

    # checks if game ends
    # right now just king of the hill win condition
    def check_game_end(self):
        if self.king & mask_Hill != 0:
            self.game_going = False

    # reset state
    def new_game(self):
        self.white = np.uint64(65535)
        self.black = np.uint64(18446462598732840960)
        self.pawn = np.uint64(71776119061282560)
        self.knight = np.uint64(4755801206503243842)
        self.rook = np.uint64(9295429630892703873)
        self.bishop = np.uint64(2594073385365405732)
        self.queen = np.uint64(576460752303423496)
        self.king = np.uint64(1152921504606846992)
        self.turn = True
        self.move = np.uint64(0)
        self.attack = np.uint64(0)
        self.castling = np.uint64(0)
        self.en_passon = np.uint64(0)
        self.double_pawn = np.uint64(0)
        self.fig_pos = np.uint64(0)
        self.thread = np.uint64(0)
        self.castling_block = np.uint64(0)
        self.move_history = []
        self.not_moved = np.uint64(10448351135499550865)
        self.game_going = True
        self.main_menue = False

    def check_moves_all(self, field):
        if field & self.pawn != 0:
            self.check_move_pawn(field)
        if field & self.rook != 0:
            self.check_move_rook(field)
        if field & self.knight != 0:
            self.check_move_knight(field)
        if field & self.bishop != 0:
            self.check_move_bishop(field)
        if field & self.queen != 0:
            self.check_move_queen(field)
        if field & self.king != 0:
            self.check_move_king(field)

    def make_moves_all(self, field):
        if self.fig_pos & self.pawn != 0:
            self.move_pawn(field)
        if self.fig_pos & self.rook != 0:
            self.move_rook(field)
        if self.fig_pos & self.knight != 0:
            self.move_knight(field)
        if self.fig_pos & self.bishop != 0:
            self.move_bishop(field)
        if self.fig_pos & self.queen != 0:
            self.move_queen(field)
        if self.fig_pos & self.king != 0:
            self.move_king(field)

    def get_score(self):
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

        return (
            20000 * king
            + 900 * queen
            + 500 * rook
            + 300 * bishop
            + 300 * knight
            + 100 * pawn
        )

    def generate_move(self):
        best_move = []
        best_score = math.inf

        for i in range(64):
            field = self.black & np.uint64(1) << np.uint64(i)

            if field != 0:
                self.check_moves_all(field)
                moves = (
                    self.move
                    | self.castling
                    | self.en_passon
                    | self.castling
                    | self.attack
                )

                for j in range(64):
                    single_move = moves & np.uint64(1) << np.uint64(j)

                    if single_move != 0:
                        self.fig_pos = field
                        self.make_moves_all(single_move)
                        score = self.get_score()

                        if self.check_legal():
                            if score == best_score:
                                best_move.append((field, single_move, score))
                            if score < best_score:
                                best_score = score
                                best_move = [(field, single_move, score)]
                        self.unmake_move()

        if len(best_move) > 0:
            data = random.choice(best_move)
        else:
            data = (np.uint64(0), np.uint64(0), best_score)

        return data

    def copy_state(self, game_state):
        self.white = game_state.white
        self.black = game_state.black
        self.pawn = game_state.pawn
        self.knight = game_state.knight
        self.rook = game_state.rook
        self.bishop = game_state.bishop
        self.queen = game_state.queen
        self.king = game_state.king
        self.move_history = game_state.move_history
        self.double_pawn = game_state.double_pawn
        self.not_moved = game_state.not_moved
        self.turn = game_state.turn

    def give_moves(self):
        pawn = []
        rook = []
        knight = []
        bishop = []
        queen = []
        king = []
        fig_type = -1

        for i in range(64):
            if self.turn:
                field = self.white & np.uint64(1) << np.uint64(i)
            else:
                field = self.black & np.uint64(1) << np.uint64(i)

            if field != 0:
                if field & self.pawn != 0:
                    fig_type = 0
                    self.check_move_pawn(field)
                if field & self.rook != 0:
                    fig_type = 1
                    self.check_move_rook(field)
                if field & self.knight != 0:
                    fig_type = 2
                    self.check_move_knight(field)
                if field & self.bishop != 0:
                    fig_type = 3
                    self.check_move_bishop(field)
                if field & self.queen != 0:
                    fig_type = 4
                    self.check_move_queen(field)
                if field & self.king != 0:
                    fig_type = 5
                    self.check_move_king(field)

                moves = (
                    self.move
                    | self.castling
                    | self.en_passon
                    | self.castling
                    | self.attack
                )

                for j in range(64):
                    single_move = moves & np.uint64(1) << np.uint64(j)

                    if single_move != 0:
                        self.fig_pos = field
                        self.make_moves_all(single_move)

                        if not self.check_legal():
                            moves = moves ^ single_move
                        self.unmake_move()

                if moves != 0:
                    if fig_type == 0:
                        pawn.append(moves)
                    if fig_type == 1:
                        rook.append(moves)
                    if fig_type == 2:
                        knight.append(moves)
                    if fig_type == 3:
                        bishop.append(moves)
                    if fig_type == 4:
                        queen.append(moves)
                    if fig_type == 5:
                        king.append(moves)

        return pawn, rook, knight, bishop, queen, king
    
    def iterative_deepening(board, max_depth):
        best_move = None
        start_time = time.time()

        for i in range(1, max_depth + 1):
            elapsed_time = time.time() - start_time
            if elapsed_time > max_time:
                break

            best_move = board.alpha_beta_search(board, i, -math.inf, math.inf)

        return best_move
    
    def evaluate(board):
        score = 0
        score += bin(board.white).count("1") * 100
        score -= bin(board.black).count("1") * 100
        score += bin(board.pawn).count("1") * 10
        score += bin(board.rook).count("1") * 50
        score += bin(board.knight).count("1") * 30
        score += bin(board.bishop).count("1") * 30
        score += bin(board.queen).count("1") * 90
        score += bin(board.king).count("1") * 900
        return score
    
    def alpha_beta_search(board, depth, alpha, beta):
        if depth == 0:
            return evaluate(board)
        if board.turn:
            value = -math.inf
            for i in range(64):
                field = board.white & np.uint64(1) << np.uint64(i)
                if field != 0:
                    board.check_moves_all(field)
                    moves = (
                        board.move
                        | board.castling
                        | board.en_passon
                        | board.castling
                        | board.attack
                    )
                    for j in range(64):
                        single_move = moves & np.uint64(1) << np.uint64(j)
                        if single_move != 0:
                            board.fig_pos = field
                            board.make_moves_all(single_move)
                            value = max(value, board.alpha_beta_search(board, depth - 1, alpha, beta))
                            alpha = max(alpha, value)
                            board.unmake_move()
                            if alpha >= beta:
                                break
                    if alpha >= beta:
                        break
            return value
        else:
            value = math.inf
            for i in range(64):
                field = board.black & np.uint64(1) << np.uint64(i)
                if field != 0:
                    board.check_moves_all(field)
                    moves = (
                        board.move
                        | board.castling
                        | board.en_passon
                        | board.castling
                        | board.attack
                    )
                    for j in range(64):
                        single_move = moves & np.uint64(1) << np.uint64(j)
                        if single_move != 0:
                            board.fig_pos = field
                            board.make_moves_all(single_move)
                            value = min(value, board.alpha_beta_search(board, depth - 1, alpha, beta))
                            beta = min(beta, value)
                            board.unmake_move()
                            if alpha >= beta:
                                break
                    if alpha >= beta:
                        break
            return value