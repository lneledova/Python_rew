from itertools import product

import numpy as np
from typing import Optional, List


class BoardState:

    def __init__(self, board: np.ndarray, current_player: int = 1):
        self.board: np.ndarray = board
        self.current_player: int = current_player

    def inverted(self) -> 'BoardState':
        return BoardState(board=self.board[::-1, ::-1] * -1, current_player=self.current_player * -1)

    def copy(self) -> 'BoardState':
        return BoardState(self.board.copy(), self.current_player)

    def change_player(self):
        self.current_player *= -1

    def do_move(self, from_x, from_y, to_x, to_y) -> Optional['BoardState']:
        """
        :return: new BoardState or None for invalid move
        """

        if (to_x + to_y) % 2 == 0:  # на белую встаёт
            return None

        if abs(to_x - from_x) != abs(to_y - from_y):
            return None  ## ходит не по диагонали

        if self.board[to_y, to_x] != 0:  ##встаёт на чужую
            return None

        result = self.copy()

        if abs(self.board[from_y, from_x]) == 1:  ## обычные ходят
            if abs(from_x - to_x) > 2:
                return None  ## обычная ходит больше

            eat = False

            if abs(from_x - to_x) == 2:
                if self.board[(from_y + to_y) // 2, (from_x + to_x) // 2] * self.board[from_y, from_x] >= 0:
                    return None  ## обычная перескакивает через свою или пустую
                else:
                    result.board[(from_y + to_y) // 2, (from_x + to_x) // 2] = 0  ## обычная кушает
                    eat = True

            if self.board[from_y, from_x] > 0 and not eat:  ## белая назад
                if to_y - from_y > 0:
                    return None
            if self.board[from_y, from_x] < 0 and not eat:  ## черная назад
                if to_y - from_y < 0:
                    return None
            if self.board[from_y, from_x] > 0 and to_y == 0:  ## белая дамка
                result.board[from_y, from_x] = 2

            if self.board[from_y, from_x] < 0 and to_y == 7:  ## черная дамка
                result.board[from_y, from_x] = -2

        if abs(self.board[from_y, from_x]) == 2:  ## ходят дамки
            x_to_bigger = 1
            y_to_bigger = 1
            if to_x < from_x:
                x_to_bigger = -1
            if to_y < from_y:
                y_to_bigger = -1

            now_x = from_x + 1 * x_to_bigger
            now_y = from_y + 1 * y_to_bigger
            dont_eat_two = True
            while now_x != to_x and now_y != to_y:
                if self.board[now_y, now_x] * self.board[from_y, from_x] > 0:
                    return None  ## своих не кушаем
                elif self.board[now_y, now_x] * self.board[from_y, from_x] < 0 and dont_eat_two:
                    result.board[now_y, now_x] = 0
                    dont_eat_two = False  ## дамка наелась и спит
                elif self.board[now_y, now_x] * self.board[from_y, from_x] < 0 and not dont_eat_two:
                    return None  ## кушаем по одной
                now_x += 1 * x_to_bigger
                now_y += 1 * y_to_bigger
        # todo more validation here

        result.board[to_y, to_x] = result.board[from_y, from_x]
        result.board[from_y, from_x] = 0
        return result

    def get_possible_eat(self) -> Optional[List['BoardState']]:
        eat_moves = []
        res = None
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i, j] == self.current_player:
                    for dx, dy in product((-2, 2), (-2, 2)):  ## ест пешка
                        if 0 <= i + dx < 8 and 0 <= j + dy < 8:
                            res = self.do_move(i + dx, j + dy)
                            if res is not None:
                                eat_moves.append(res)
                                res = None
                if abs(self.board[i, j]) == 2 and self.board[i, j] / 2 == self.current_player:
                    for to_x in range(j + 2, 8):
                        for to_y in range(i + 2, 8):
                            now_x = j + 1
                            now_y = i + 1
                            while now_x != to_x and now_y != to_y:
                                if self.board[now_y, now_x] != 0:
                                    res = self.do_move(j, i, to_x, to_y)
                                if res is not None:
                                    eat_moves.append(res)
                                    res = None
                                now_x += 1
                                now_y += 1
                    for to_x in range(j + 2, 8):
                        for to_y in range(i - 2, 0, -1):
                            now_x = j + 1
                            now_y = i - 1
                            while now_x != to_x and now_y != to_y:
                                if self.board[now_y, now_x] != 0:
                                    res = self.do_move(j, i, to_x, to_y)
                                if res is not None:
                                    eat_moves.append(res)
                                    res = None
                                now_x += 1
                                now_y -= 1
                    for to_x in range(j - 2, 0, -1):
                        for to_y in range(i + 2, 8, 1):
                            now_x = j - 1
                            now_y = i + 1
                            while now_x != to_x and now_y != to_y:
                                if self.board[now_y, now_x] != 0:
                                    res = self.do_move(j, i, to_x, to_y)
                                if res is not None:
                                    eat_moves.append(res)
                                    res = None
                                now_x -= 1
                                now_y += 1
                    for to_x in range(j - 2, 0, -1):
                        for to_y in range(i - 2, 0, -1):
                            now_x = j - 1
                            now_y = i - 1
                            while now_x != to_x and now_y != to_y:
                                if self.board[now_y, now_x] != 0:
                                    res = self.do_move(j, i, to_x, to_y)
                                if res is not None:
                                    eat_moves.append(res)
                                    res = None
                                now_x -= 1
                                now_y -= 1
        return eat_moves

    def get_possible_moves(self) -> List['BoardState']:
        moves = []
        res = None
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i, j] == self.current_player and self.board[i, j] == -1:  ## возможные ходы для черной
                    for dj in (-1, 1):
                        if i < 8 and 0 < j + dj < 8:
                            res = self.do_move(j, i, j + dj, i + 1)
                            if res is not None:
                                moves.append(res)
                                res = None
                if self.board[i, j] == 1 and self.current_player == 1:  ## белая пешка
                    for dj in (-1, 1):
                        if i > 0 and 0 < j + dj < 8:
                            res = self.do_move(j, i, j + dj, i - 1)
                            if res is not None:
                                moves.append(res)
                                res = None
                if self.board[i, j] == self.current_player:  ## ест пешка
                    for di, dj in product((-2, 2), (-2, 2)):
                        if 0 <= i + di < 8 and 0 <= j + dj < 8:
                            res = self.do_move(j, i, j + dj, i + di)
                            if res is not None:
                                moves.append(res)
                                res = None
                if self.board[i, j] == 2 and self.current_player == 1:  ## дамкa белая
                    for k in range(-i, 8 - i):
                        if j + k < 8 and j + k > -1:
                            res = self.do_move(j, i, j + k, i + k)
                        if res is not None:
                            moves.append(res)
                            res = None
                    for k in range(-j, 8 - j):
                        if i + k > -1 and i + k < 8:
                            res = self.do_move(j, i, j + k, i + k)
                        if res is not None:
                            moves.append(res)
                            res = None
                if self.board[i, j] == -2 and self.current_player == -1:  ## дамкa черная
                    for k in range(-i, 8 - i):
                        if j + k < 8 and j + k > -1:
                            res = self.do_move(j, i, j + k, i + k)
                        if res is not None:
                            moves.append(res)
                            res = None
                    for k in range(-j, 8 - j):
                        if i + k > -1 and i + k < 8:
                            res = self.do_move(j, i, j + k, i + k)
                        if res is not None:
                            moves.append(res)
                            res = None

        return moves

    @property
    def is_game_finished(self) -> bool:
        if len(self.get_possible_moves()) == 0:
            return True
        self.current_player *= -1
        if len(self.get_possible_moves()) == 0:
            self.current_player *= -1
            return True
        self.current_player *= -1
        return False

    @property
    def get_winner(self) -> Optional[int]:
        if self.is_game_finished:
            return self.current_player * (-1)
        return self.current_player

    @staticmethod
    def initial_state() -> 'BoardState':
        board = np.zeros(shape=(8, 8), dtype=np.int8)

        for i in range(0, 8, 2):
            board[7, i] = 1
            board[6, i + 1] = 1
            board[5, i] = 1
            board[0, i + 1] = -1
            board[1, i] = -1
            board[2, i + 1] = -1

        return BoardState(board, 1)


def checking_move(board, new_board, player_):
    moves = board.get_possible_moves()
    if new_board is not None:
        k = False  # валидный ход
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
        l = False  # скушал
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


def checking_move_ai(board, new_board, player_):
    eat_moves = board.get_possible_eat()
    l = False  ## скушал
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
