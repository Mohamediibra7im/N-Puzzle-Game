import random
from typing import List, Tuple, Optional


class PuzzleState:
    def __init__(
        self,
        size: int,
        tiles: Optional[List[int]] = None,
        blank_pos: Optional[int] = None,
    ):
        self.size = size
        self.n = size * size
        if tiles is not None:
            self.tiles = tiles.copy()
            self.blank_pos = blank_pos if blank_pos is not None else self.tiles.index(0)
        else:
            self.tiles = list(range(1, self.n)) + [0]  # Goal state
            self.blank_pos = self.n - 1
        self.parent = None
        self.move_from_parent = None
        self.depth = 0

    def __str__(self) -> str:
        return "\n".join(
            " ".join(
                f"{x:2}" if x != 0 else "  "
                for x in self.tiles[i * self.size : (i + 1) * self.size]
            )
            for i in range(self.size)
        )

    def __eq__(self, other) -> bool:
        return self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(tuple(self.tiles))

    def copy(self) -> "PuzzleState":
        new_state = PuzzleState(self.size, self.tiles, self.blank_pos)
        new_state.parent = self.parent
        new_state.move_from_parent = self.move_from_parent
        new_state.depth = self.depth
        return new_state

    def move(self, direction: str) -> Optional["PuzzleState"]:
        row, col = divmod(self.blank_pos, self.size)

        if direction == "up" and row > 0:
            new_blank = self.blank_pos - self.size
        elif direction == "down" and row < self.size - 1:
            new_blank = self.blank_pos + self.size
        elif direction == "left" and col > 0:
            new_blank = self.blank_pos - 1
        elif direction == "right" and col < self.size - 1:
            new_blank = self.blank_pos + 1
        else:
            return None

        new_tiles = self.tiles.copy()
        new_tiles[self.blank_pos], new_tiles[new_blank] = (
            new_tiles[new_blank],
            new_tiles[self.blank_pos],
        )

        new_state = PuzzleState(self.size, new_tiles, new_blank)
        new_state.parent = self
        new_state.move_from_parent = direction
        new_state.depth = self.depth + 1
        return new_state

    def get_valid_moves(self) -> List[str]:
        valid_moves = []
        row, col = divmod(self.blank_pos, self.size)

        if row > 0:
            valid_moves.append("up")
        if row < self.size - 1:
            valid_moves.append("down")
        if col > 0:
            valid_moves.append("left")
        if col < self.size - 1:
            valid_moves.append("right")
        return valid_moves

    def is_goal(self) -> bool:
        return self.tiles == list(range(1, self.n)) + [0]

    def shuffle(self, moves: int = 100) -> "PuzzleState":
        current = self.copy()
        for _ in range(moves):
            valid_moves = current.get_valid_moves()
            move = random.choice(valid_moves)
            current = current.move(move)
        return current

    def get_path(self) -> List["PuzzleState"]:
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path[::-1]