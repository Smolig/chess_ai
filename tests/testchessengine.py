import unittest
import numpy as np
from engine_v1 import Engine
from tests.testcases import test


class TestChessEngine(unittest.TestCase):
    new_engine = Engine()

    def test_starting_position(self):
        Engine.new_game(self.new_engine)
        self.assertEqual(self.new_engine.white, 65535)
        self.assertEqual(self.new_engine.black, 18446462598732840960)
        self.assertEqual(self.new_engine.pawn, 71776119061282560)
        self.assertEqual(self.new_engine.knight, 4755801206503243842)
        self.assertEqual(self.new_engine.rook, 9295429630892703873)
        self.assertEqual(self.new_engine.bishop, 2594073385365405732)
        self.assertEqual(self.new_engine.queen, 576460752303423496)
        self.assertEqual(self.new_engine.king, 1152921504606846992)
        self.assertEqual(self.new_engine.turn, True)

    def test_opening_italian_game(self):
        Engine.new_game(self.new_engine)
        white = np.uint64(337702815)
        black = np.uint64(18297848277795602432)
        pawn = np.uint64(67272588421820160)
        knight = np.uint64(4611690416475996162)
        rook = np.uint64(9295429630892703873)
        bishop = np.uint64(2594073385432514564)
        queen = np.uint64(576460752303423496)
        king = np.uint64(1152921504606846992)
        turn = False
        self.assertEqual(
            test(
                pawn,
                rook,
                knight,
                bishop,
                queen,
                king,
                white,
                black,
                turn,
                self.new_engine,
            )[6],
            31,
        )  # schwarz am zug
        self.assertEqual(
            test(
                pawn,
                rook,
                knight,
                bishop,
                queen,
                king,
                white,
                black,
                True,
                self.new_engine,
            )[6],
            33,
        )  # weiß am zug

    def test_opening_queens_gambit(self):
        Engine.new_game(self.new_engine)
        white = np.uint64(201389055)
        black = np.uint64(18444210833278894080)
        pawn = np.uint64(69524353808659200)
        knight = np.uint64(4755801206503243842)
        rook = np.uint64(9295429630892703873)
        bishop = np.uint64(2594073385365405732)
        queen = np.uint64(576460752303423496)
        king = np.uint64(1152921504606846992)
        turn = False
        self.assertEqual(
            test(
                pawn,
                rook,
                knight,
                bishop,
                queen,
                king,
                white,
                black,
                turn,
                self.new_engine,
            )[6],
            28,
        )  # schwarz am zug
        self.assertEqual(
            test(
                pawn,
                rook,
                knight,
                bishop,
                queen,
                king,
                white,
                black,
                True,
                self.new_engine,
            )[6],
            30,
        )  # weiß am zug

    def test_midgame(self):
        Engine.new_game(self.new_engine)
        white = np.uint64(69390882737)
        black = np.uint64(15127327282726699008)
        pawn = np.uint64(65020720157087488)
        knight = np.uint64(4611686018427650048)
        rook = np.uint64(9295429630892703873)
        bishop = np.uint64(2251885713031200)
        queen = np.uint64(17592320262144)
        king = np.uint64(1152921504606846992)
        turn = True
        self.assertEqual(
            test(
                pawn,
                rook,
                knight,
                bishop,
                queen,
                king,
                white,
                black,
                turn,
                self.new_engine,
            )[6],
            43,
        )
