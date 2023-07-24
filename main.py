import pygame, sys
from game_wrapper import Wrapper
from game_functions.draw import *
from game_functions.player import Player
from engine_v3 import Engine
import numpy as np
from time import sleep


pygame.init()
game_engine = Engine()
game_state = Engine()
player_controle = Player()
game_wrapper = Wrapper(game_state)

clock = pygame.time.Clock()

move_sound = pygame.mixer.Sound("assets/move.wav")
start_game_sound = pygame.mixer.Sound("assets/start_game.wav")

positions = [(55, 690), (130, 690), (205, 690), (280, 690), (355, 690), (430, 690), (505, 690), (580, 690), 
             (55, 615), (130, 615), (205, 615), (280, 615), (355, 615), (430, 615), (505, 615), (580, 615), 
             (55, 540), (130, 540), (205, 540), (280, 540), (355, 540), (430, 540), (505, 540), (580, 540), 
             (55, 465), (130, 465), (205, 465), (280, 465), (355, 465), (430, 465), (505, 465), (580, 465), 
             (55, 390), (130, 390), (205, 390), (280, 390), (355, 390), (430, 390), (505, 390), (580, 390), 
             (55, 315), (130, 315), (205, 315), (280, 315), (355, 315), (430, 315), (505, 315), (580, 315), 
             (55, 240), (130, 240), (205, 240), (280, 240), (355, 240), (430, 240), (505, 240), (580, 240), 
             (55, 165), (130, 165), (205, 165), (280, 165), (355, 165), (430, 165), (505, 165), (580, 165)]

# set up the window
size = (670, 810)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("King of The Hill")
screen.fill((230, 230, 230))

# background of game
background = pygame.Surface((670, 810))
background.fill((230, 230, 230))

# set main menue
main_menue = pygame.Surface((670, 810))
img = pygame.image.load("assets/main_menue.jpg")
img.convert()
rect = img.get_rect(topleft=(0, 0))
main_menue_bg = pygame.Surface((670, 810))
main_menue_bg.blit(img, rect)
main_menue.blit(main_menue_bg, rect)
pygame.draw.rect(main_menue, (240, 240, 240), (40, 400, 340, 80))
font = pygame.font.SysFont("futura", 60)
main_menue.blit(font.render("New Game", True, (50, 50, 50)), (50, 400))
font = pygame.font.SysFont("futura", 30)
main_menue.blit(font.render("Player vs Player", True, (50, 50, 50)), (95, 537.5))
main_menue.blit(font.render("Player vs AI", True, (50, 50, 50)), (95, 637.5))

# set up the board
board = pygame.Surface((600, 600))
board.fill((249, 255, 250))

# game_wrapper.test_state()
# set up Move
move_dis = pygame.Surface((560, 120))
move_dis.fill((248, 248, 255))

# set up Performance
perform_dis = pygame.Surface((55, 120))
perform_dis.fill((230, 230, 230))


# draw the board
font = pygame.font.SysFont("futura", 25)
board_scale_x = []
board_scale_y = []
for i in ["1", "2", "3", "4", "5", "6", "7", "8"]:
    board_scale_y.append(font.render(i, True, (50, 50, 50)))
for i in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    board_scale_x.append(font.render(i, True, (50, 50, 50)))

for x in range(0, 8, 2):
    for y in range(0, 8, 2):
        pygame.draw.rect(board, (96, 165, 165), ((x + 1) * 75, (y + 1) * 75, 75, 75))
        pygame.draw.rect(board, (96, 165, 165), (x * 75, y * 75, 75, 75))

# draw game over
game_over_screen = pygame.Surface((630, 120))
game_over_screen.fill((249, 255, 250))

font = pygame.font.SysFont("futura", 25)
pygame.draw.rect(game_over_screen, (96, 165, 165), (410, 15, 190, 40))
game_over_screen.blit(font.render("New game", True, (249, 255, 250)), (430, 17.5))


pygame.display.flip()


# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # mouse events
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if game_wrapper.main_menue:
                has_pressed = player_controle.main_menue(game_wrapper, pos)
                # if has_pressed:
                    # start_game_sound.play()
            else:
                player_controle.game_button(game_wrapper, pos)
                if game_wrapper.game_mode != 2:
                    if game_wrapper.game_going:
                        if not game_wrapper.selection:
                            player_controle.player_click(screen, game_wrapper, pos)
                        else:
                            player_controle.player_submit(screen, game_wrapper, pos)
                    else:
                        player_controle.game_over(screen, game_wrapper, pos)

    # check if we are in the main menue
    if game_wrapper.main_menue:
        main_menue.blit(main_menue_bg, rect)
        pygame.draw.rect(main_menue, (240, 240, 240), (40, 400, 340, 80))
        font = pygame.font.SysFont("futura", 60)
        main_menue.blit(font.render("New Game", True, (50, 50, 50)), (50, 400))
        font = pygame.font.SysFont("futura", 30)

        # toggle game mode button
        if game_wrapper.game_mode == 0:
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 525, 300, 60))
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 625, 300, 60), 5)
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 725, 300, 60), 5)
        elif game_wrapper.game_mode == 1:
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 525, 300, 60), 5)
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 625, 300, 60))
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 725, 300, 60), 5)
        else:
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 525, 300, 60), 5)
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 625, 300, 60), 5)
            pygame.draw.rect(main_menue, (240, 240, 240), (60, 725, 300, 60))
        main_menue.blit(font.render("Player vs Player", True, (50, 50, 50)), (95, 537.5))
        main_menue.blit(font.render("Player vs AI", True, (50, 50, 50)), (95, 637.5))
        main_menue.blit(font.render("AI vs AI", True, (50, 50, 50)), (95, 737.5))
        screen.blit(main_menue, (0, 0))

        pygame.display.update()

    # in game
    else:
        screen.fill((230, 230, 230))
        
        for i in range(0, 8):
            screen.blit(board_scale_x[i], (20, 185 + i * 75))
            screen.blit(board_scale_y[i], (75 + i * 75, 770))
        
        # checks if game over
        if not game_wrapper.game_going:
            game_over_screen.fill((249, 255, 250))
            font = pygame.font.SysFont("futura", 25)
            pygame.draw.rect(game_over_screen, (96, 165, 165), (410, 15, 190, 40))
            game_over_screen.blit(font.render("New game", True, (249, 255, 250)), (430, 17.5))
            font = pygame.font.SysFont("futura", 30)
            game_over_screen.blit(font.render(game_wrapper.game_over_msg1, True, (50, 50, 50)), (25, 20))
            game_over_screen.blit(font.render(game_wrapper.game_over_msg2, True, (50, 50, 50)), (25, 60))
            screen.blit(game_over_screen, (20, 20))
        else:
            pygame.draw.rect(perform_dis, (248, 248, 255), (0, 65, 55, 55))
            font = pygame.font.SysFont("futura", 50)
            perform_dis.blit(font.render("X", True, (50, 50, 50)), (9, 62))
            font = pygame.font.SysFont("futura", 28)
            if game_wrapper.game_mode == 0:
                pygame.draw.rect(perform_dis, (248, 248, 255), (0, 0, 55, 55))
                perform_dis.blit(font.render("P-P", True, (50, 50, 50)), (8, 10))
            elif game_wrapper.game_mode == 1:
                pygame.draw.rect(perform_dis, (248, 248, 255), (0, 0, 55, 55))
                perform_dis.blit(font.render("P-AI", True, (50, 50, 50)), (0, 10))
            else:
                font = pygame.font.SysFont("futura", 20)
                pygame.draw.rect(perform_dis, (248, 248, 255), (0, 0, 55, 55))
                perform_dis.blit(font.render("AI-AI", True, (50, 50, 50)), (4, 15))

            screen.blit(perform_dis, (595, 20))
            # Puts performance
            font = pygame.font.SysFont("futura", 25)
            move_dis.fill((248, 248, 255))
            move_dis.blit(font.render(f"Search Level: {game_wrapper.depth}", True, (50, 50, 50)), (5, 5))
            move_dis.blit(
                font.render(f"Calculation Time: {game_wrapper.performance}s", True, (50, 50, 50)),
                (5, 35),
            )
            move_dis.blit(
                font.render(f"Score: {game_wrapper.score}", True, (50, 50, 50)),
                (5, 65),
            )
            screen.blit(move_dis, (20, 20))
        screen.blit(board, (50, 160))

        if game_wrapper.selection:
            draw_castling(screen, game_wrapper.castling)
            draw_move(screen, game_wrapper.move)
            draw_attack(screen, game_wrapper.attack)
            draw_select(screen, game_wrapper.field_num)
            draw_en_passon(screen, game_wrapper.en_passon)

        draw_thread(screen, game_wrapper.castling_block)
        draw_thread(screen, game_wrapper.thread)
        draw_state(screen, game_wrapper)
        pygame.draw.rect(screen, (50, 50, 50), (275, 385, 150, 150), 4)

        pygame.display.update()

        if game_wrapper.pos_change:
            game_wrapper.evaluate_position()
            move_sound.play()
            game_wrapper.pos_change = False

        # Ai play turn
        if game_wrapper.game_going:
            if (game_wrapper.game_mode == 1) & (not game_wrapper.get_turn()):
                game_wrapper.copy_state(game_state, game_engine)
                game_wrapper.ai_move(game_engine) 

            if game_wrapper.game_mode == 2:
                game_wrapper.copy_state(game_state, game_engine)
                game_wrapper.ai_move(game_engine) 
                

    clock.tick(30)
