from itertools import product

import pygame
from pygame import Surface

from src.ai import AI, PositionEvaluation
from src.boardstate import BoardState
player_ = 1
ai_ = -1


def draw_board(screen: Surface, pos_x: int, pos_y: int, elem_size: int, board: BoardState):
    dark = (5, 5, 15)
    white = (240, 248, 255)

    for y, x in product(range(8), range(8)):
        color = white if (x + y) % 2 == 0 else dark
        position = pos_x + x * elem_size, pos_y + y * elem_size, elem_size, elem_size
        pygame.draw.rect(screen, color, position)

        figure = board.board[y, x]

        if figure == 0:
            continue

        if figure > 0:
            figure_color = 230, 230, 250
        else:
            figure_color = 72, 61, 139
        r = elem_size // 2 - 10

        sec_figure_color = 147, 112, 219

        pygame.draw.circle(screen, figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
        pygame.draw.circle(screen, sec_figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r + 2, 2)
        if abs(figure) == 2:
            r = 5
            if figure > 0:
                th_figure_color = 72, 61, 139
            else:
                th_figure_color = 230, 230, 250

            pygame.draw.circle(screen, sec_figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r)
            pygame.draw.circle(screen, th_figure_color, (position[0] + elem_size // 2, position[1] + elem_size // 2), r + 1, 1)


def game_loop(screen: Surface, board: BoardState, ai: AI):
    grid_size = screen.get_size()[0] // 8

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click_position = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and board.current_player == player_:
                new_x, new_y = [p // grid_size for p in event.pos]
                old_x, old_y = [p // grid_size for p in mouse_click_position]

                new_board = board.do_move(old_x, old_y, new_x, new_y)
                moves = board.get_possible_moves()
                if new_board is not None:
                    k = False # валидный ход
                    for i in range(len(moves)):
                        comp = True
                        for x in range(8):
                            for y in range(8):
                                if new_board.board[x, y] != moves[i].board[x, y]:
                                    comp = False
                        if comp:
                            k = True
                            break
                    eat_moves = board.get_possible_eat()
                    l = False # скушал
                    for i in range(len(eat_moves)):
                        comp = True
                        for x in range(8):
                            for y in range(8):
                                if new_board.board[x, y] != eat_moves[i].board[x, y]:
                                    comp = False
                        if comp:
                            l = True
                            break
                    if k:
                        if len(eat_moves) != 0 and l:
                            board = new_board
                            if len(new_board.get_possible_eat()) == 0:
                                board.change_player()
                        elif not l and len(eat_moves) == 0:
                            board = new_board
                            board.change_player()
                    if board.is_game_finished:
                        if board.get_winner == player_:
                            print("Win")
                        else:
                            print("Lose")
                        return

            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                x, y = [p // grid_size for p in event.pos]
                board.board[y, x] = (board.board[y, x] + 1 + 2) % 5 - 2  # change figure

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = board.inverted()

                if event.key == pygame.K_SPACE and board.current_player == ai_:
                    new_board = ai.next_move(board)
                    eat_moves = board.get_possible_eat()
                    l = False ## скушал
                    for i in range(len(eat_moves)):
                        comp = True
                        for x in range(8):
                            for y in range(8):
                                if new_board.board[x, y] != eat_moves[i].board[x, y]:
                                    comp = False
                        if comp:
                            l = True
                            break
                    if len(eat_moves) != 0 and l:
                        board = new_board
                        if len(new_board.get_possible_eat()) == 0:
                            board.change_player()
                    elif not l and len(eat_moves) == 0:
                        board = new_board
                        board.change_player()
                    if board.is_game_finished:
                        if board.get_winner == player_:
                            print("Win")
                        else:
                            print("Lose")
                        return



        draw_board(screen, 0, 0, grid_size, board)
        pygame.display.flip()



pygame.init()

screen: Surface = pygame.display.set_mode([512, 512])
ai = AI(PositionEvaluation(), search_depth=4, now_player=ai_)

game_loop(screen, BoardState.initial_state(), ai)

pygame.quit()
