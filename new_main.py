import pygame, sys
from game_wrapper import Wrapper
from game_functions.draw import *
from game_functions.player import Player
from engine_v3 import Engine


game_engine = Engine()
game_state = Engine()
player_controle = Player()
game_wrapper = Wrapper(game_state)
clock = pygame.time.Clock()


# main loop
while game_wrapper.game_going:

    game_wrapper.evaluate_position()
    game_wrapper.copy_state(game_state, game_engine)
    game_wrapper.ai_move(game_engine)
    game_state.print_state()
    print(game_state.turn)
    print(game_wrapper.score)


