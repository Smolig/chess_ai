import numpy as np
import pygame

# create field positions
positions = []
colour = []
for i in range(0, 8):
    for y in range(0, 8):
        positions.append((55 + y * 75, 690 - i * 75))
        if i % 2 == 0:
            if y % 2 == 0:
                colour.append(False)
            else:
                colour.append(True)
        else:
            if y % 2 == 0:
                colour.append(True)
            else:
                colour.append(False)


# draws the pieces
def draw_state(screen, state):
    fig_name, fig_pos = state.get_all_fig()

    for x in range(0, 12):
        fig_state = fig_pos[x]
        fig_state = "{:064b}".format(fig_state, "b")
        fig_state = fig_state[::-1]

        result = []

        for i in range(0, 64):
            if fig_state[i] == "1":
                result.append(i)

        for i in range(0, len(result)):
            img = pygame.image.load(f"assets/{fig_name[x]}.png")
            img.convert()
            rect = img.get_rect(topleft=positions[result[i]])
            screen.blit(img, rect)


# change colour of selected field
def draw_select(screen, field_num):
    field = positions[field_num]

    if colour[field_num]:
        pygame.draw.rect(screen, (69, 130, 165), (field[0] - 5, field[1] - 5, 75, 75))
    else:
        pygame.draw.rect(screen, (191, 216, 242), (field[0] - 5, field[1] - 5, 75, 75))


# draws attacking piece
def draw_thread(screen, pattern):
    pattern = "{:064b}".format(pattern, "b")
    pattern = pattern[::-1]

    result = []

    for i in range(0, 64):
        if pattern[i] == "1":
            result.append(i)

    for i in range(0, len(result)):
        pygame.draw.rect(
            screen,
            (255, 200, 200),
            (positions[result[i]][0] - 5, positions[result[i]][1] - 5, 75, 75),
        )


# draws all moves
def draw_move(screen, pattern):
    pattern = "{:064b}".format(pattern, "b")
    pattern = pattern[::-1]

    result = []

    for i in range(0, 64):
        if pattern[i] == "1":
            result.append(i)

    for i in range(0, len(result)):
        pygame.draw.circle(
            screen,
            (200, 200, 200),
            (positions[result[i]][0] + 32.5, positions[result[i]][1] + 32.5),
            15,
            8,
        )


# draws attacks
def draw_attack(screen, pattern):
    pattern = "{:064b}".format(pattern, "b")
    pattern = pattern[::-1]

    result = []

    for i in range(0, 64):
        if pattern[i] == "1":
            result.append(i)

    for i in range(0, len(result)):
        pygame.draw.circle(
            screen,
            (255, 200, 200),
            (positions[result[i]][0] + 32.5, positions[result[i]][1] + 32.5),
            30,
            8,
        )


# draws castling
def draw_castling(screen, pattern):
    pattern = "{:064b}".format(pattern, "b")
    pattern = pattern[::-1]

    result = []

    for i in range(0, 64):
        if pattern[i] == "1":
            result.append(i)

    for i in range(0, len(result)):
        pygame.draw.circle(
            screen,
            (200, 200, 200),
            (positions[result[i]][0] + 32.5, positions[result[i]][1] + 32.5),
            30,
            8,
        )


# draws en passon
def draw_en_passon(screen, pattern):
    pattern = "{:064b}".format(pattern, "b")
    pattern = pattern[::-1]

    result = []

    for i in range(0, 64):
        if pattern[i] == "1":
            result.append(i)

    for i in range(0, len(result)):
        pygame.draw.circle(
            screen,
            (255, 200, 200),
            (positions[result[i]][0] + 32.5, positions[result[i]][1] + 32.5),
            15,
            8,
        )
