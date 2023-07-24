import numpy as np
from time import perf_counter

class Wrapper:
    def __init__(self, game_state_engine):
        self.engine = game_state_engine

        self.move = np.uint64(0)
        self.attack = np.uint64(0)
        self.castling = np.uint64(0)
        self.en_passon = np.uint64(0)
        
        self.move_from = np.uint64(0)
        self.thread = np.uint64(0)

        self.castling_block = np.uint64(0)
       
        self.game_going = True
        self.main_menue = True
        self.game_mode = 0
        self.score = 0
        self.depth = 0
        self.game_over_msg1 = None
        self.game_over_msg2 = None

        self.score = 0

        self.selection = False
        self.field_num = -1
        self.performance = 0
        self.pos_change = False

        self.move = 0
        self.half_move = 0


    def get_all_fig(self):
        e = self.engine

        fig_name = ["pawn_w", "rook_w", "knight_w", "bishop_w", "queen_w", "king_w", "pawn_b", "rook_b", "knight_b",
                    "bishop_b", "queen_b", "king_b"]
        fig_pos = [e.pawn & e.white, e.rook & e.white, e.knight & e.white, e.bishop & e.white,
                e.queen & e.white, e.king & e.white,
                e.pawn & e.black, e.rook & e.black, e.knight & e.black, e.bishop & e.black,
                e.queen & e.black, e.king & e.black]
        return fig_name, fig_pos

    def get_turn(self):
        return self.engine.turn
    
    def get_colour(self):
        if self.engine.turn:
            return self.engine.white
        return self.engine.black

    def evaluate_position(self):
        self.score = self.engine.get_score()
        game_over_trigger, message1, message2 = self.engine.check_game_end()
        self.game_going = game_over_trigger
        self.game_over_msg1 = message1
        self.game_over_msg2 = message2


    def check_moves(self, field, field_num):
        
        field = field & self.get_colour()

        if field & self.engine.king != 0:
            move, attack, castling, en_passon = self.engine.state_helper_check_move_king(field)

            self.move_from = field
            self.move = move
            self.attack = attack
            self.en_passon = en_passon
            self.castling = castling
            self.selection = True
            self.field_num = field_num

            self.engine.print_board((self.move, self.attack, self.castling, self.en_passon))

            return

        if field != 0:

            move, attack, en_passon, castling = self.engine.check_moves_all(field)

            self.move_from = field
            self.move = move
            self.attack = attack
            self.en_passon = en_passon
            self.castling = castling
            self.selection = True
            self.field_num = field_num

    def make_moves(self, field):
        self.selection = False
        self.pos_change = False

        test = self.move | self.attack | self.en_passon | self.castling

        if test & field != 0:

            if self.move_from & self.engine.king != 0:
                self.engine.state_helper_make_move_king(self.move_from, field, self.move, self.attack, self.en_passon, self.castling)

            self.engine.make_moves_all(self.move_from, field, self.move, self.attack, self.en_passon, self.castling)

            self.move = np.uint64(0)
            self.attack = np.uint64(0)
            self.castling = np.uint64(0)
            self.en_passon = np.uint64(0)
            self.move_from = np.uint64(0)
            self.thread = np.uint64(0)
            self.castling_block = np.uint64(0)
            
            self.field_num = -1

            legal, thread = self.engine.state_helper_check_legal()
            self.thread = thread

            if not legal:
                self.engine.unmake_move()
                return
            
            self.score = self.engine.get_score()
            self.pos_change = True

            
    def new_game(self):
        self.move = np.uint64(0)
        self.attack = np.uint64(0)
        self.castling = np.uint64(0)
        self.en_passon = np.uint64(0)
        self.move_from = np.uint64(0)
        self.thread = np.uint64(0)
        self.castling_block = np.uint64(0)
        self.game_going = True
        self.main_menue = True
        self.game_mode = 0
        self.score = 0
        self.depth = 0
        self.game_over_msg1 = None
        self.game_over_msg2 = None
        self.score = 0
        self.selection = False
        self.field_num = -1
        self.performance = 0
        self.pos_change = False
        self.move = 0
        self.half_move = 0

        e = self.engine

        e.white = np.uint64(65535)
        e.black = np.uint64(18446462598732840960)
        e.pawn = np.uint64(71776119061282560)
        e.knight = np.uint64(4755801206503243842)
        e.rook = np.uint64(9295429630892703873)
        e.bishop = np.uint64(2594073385365405732)
        e.queen = np.uint64(576460752303423496)
        e.king = np.uint64(1152921504606846992)
        e.turn = True
        e.double_pawn = np.uint64(0)
        e.move_history = []
        e.not_moved = np.uint64(10448351135499550865)
        e.count_moves = 0
        e.count_half_moves = 0

    def copy_state(self, engine_from, engine_to):
        engine_to.white = engine_from.white
        engine_to.black = engine_from.black
        engine_to.pawn = engine_from.pawn
        engine_to.knight = engine_from.knight
        engine_to.rook = engine_from.rook
        engine_to.bishop = engine_from.bishop
        engine_to.queen = engine_from.queen
        engine_to.king = engine_from.king
        engine_to.turn = engine_from.turn
        engine_to.double_pawn = engine_from.double_pawn
        engine_to.move_history = engine_from.move_history
        engine_to.not_moved = engine_from.not_moved
        engine_to.count_moves = engine_from.count_moves
        engine_to.count_half_moves = engine_from.count_half_moves

    def ai_move(self, engine):
        
        start = perf_counter()
        move_from, move_to, score, depth = ai_move = engine.iterativ()
        end = perf_counter()

        self.depth = depth
        self.performance = round(end - start, 8)

        move, attack, en_passon, castling = self.engine.check_moves_all(move_from)
        self.engine.make_moves_all(move_from, move_to, move, attack, en_passon, castling)
        self.score = self.engine.get_score()
        self.pos_change = True

        