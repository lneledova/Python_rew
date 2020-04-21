from typing import Optional

from .boardstate import BoardState


class PositionEvaluation:
    def __call__(self, board: BoardState, depth: int, now_player) -> float:
        if depth == 0:
            return self.evaluate(board)
        else:
            copy_b = board.copy()
            copy_b.current_player *= -1
            eat_moves = copy_b.get_possible_eat()
            if len(eat_moves) != 0:
                moves = eat_moves
            else:
                moves = copy_b.get_possible_moves()
            res = -10000
            for i in moves:
                res = max(res, self.__call__(i, depth - 1, now_player) * now_player)
        return res

    def evaluate(self, board):
        res = 0
        for i in range(8):
            for j in range(8):
                res += board.board[j, i]
                if board.board[j, i] == 2 * board.current_player:
                    res += 3 * board.current_player
                elif board.board[j, i] == 2 * (-1) * board.current_player:
                    res += 4 * board.current_player * (-1)
        return res

class AI:
    def __init__(self, position_evaluation: PositionEvaluation, search_depth: int, now_player: int):
        self.position_evaluation: PositionEvaluation = position_evaluation
        self.depth: int = search_depth
        self.now_player: int = now_player

    def next_move(self, board: BoardState) -> Optional[BoardState]:
        eat_moves = board.get_possible_eat()
        if len(eat_moves) != 0:
            moves = eat_moves
        else:
            moves = board.get_possible_moves()
        if len(moves) == 0:
            return None

        # todo better implementation
        return max(moves, key=lambda b: self.position_evaluation(b, self.depth, self.now_player) * b.current_player)
