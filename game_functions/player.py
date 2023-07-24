from game_functions.draw import (
    draw_select,
    draw_move,
    draw_attack,
    draw_castling,
    draw_en_passon,
    draw_thread,
)
import numpy as np

mask4 = np.uint64(18446744073709551615)


class Player:
    def __init__(self):
        pass

    # calls the function to check the possible moves
    def player_click(self, screen, game_state, pos):
        if 50 <= pos[0] <= 650:
            if 160 <= pos[1] <= 760:
                x = int((pos[0] - 50) / 75) + 1
                y = int((pos[1] - 160) / 75) + 1
                field_num = (x - 1) + (8 - y) * 8
                field = np.uint64(2) ** np.uint64(field_num)

                game_state.check_moves(field, field_num)

                draw_thread(screen, game_state.castling_block)
                draw_thread(screen, game_state.thread)
                draw_castling(screen, game_state.castling)
                draw_move(screen, game_state.move)
                draw_attack(screen, game_state.attack)
                draw_select(screen, field_num)
                draw_en_passon(screen, game_state.en_passon)


    # executes move
    def player_submit(self, screen, game_state, pos):

        if 50 <= pos[0] <= 650:
            if 160 <= pos[1] <= 760:
                x = int((pos[0] - 50) / 75) + 1
                y = int((pos[1] - 160) / 75) + 1
                field_num = (x - 1) + (8 - y) * 8
                field = np.uint64(2) ** np.uint64(field_num)

                game_state.make_moves(field)

        game_state.castling = np.uint64(0)
        game_state.move = np.uint64(0)
        game_state.attack = np.uint64(0)
        game_state.en_passon = np.uint64(0)
        game_state.figure = None

    # buttons on the game over screen
    def game_over(self, screen, game_state, pos):
        if 430 <= pos[0] <= 620:
            if 35 <= pos[1] <= 75:
                game_state.new_game()
                game_state.score = 0

    # buttons in the main menue
    def main_menue(self, game_state, pos):
        if 40 <= pos[0] <= 380:
            if 400 <= pos[1] <= 480:
                game_state.main_menue = False
                return True
        if 60 <= pos[0] <= 360:
            if 525 <= pos[1] <= 585:
                
                    game_state.game_mode = 0
                    
            if 625 <= pos[1] <= 685:
                
                    game_state.game_mode = 1
                    
            if 725 <= pos[1] <= 785:
                
                    game_state.game_mode = 2
                    
        return False

    # buttons in the game
    def game_button(self, game_state, pos):
        if 595 <= pos[0] <= 650:
            if 85 <= pos[1] <= 120:
                game_state.new_game()
                game_state.main_menue = True
                game_state.score = 0
