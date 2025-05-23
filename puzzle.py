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
            self.tiles = list(range(1, self.n)) + [0]
            self.blank_pos = self.n - 1
        self.parent = None
        self.move_from_parent = None
        self.depth = 0
        self._path_cache = None

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

    def is_solvable(self) -> bool:
        inversions = 0
        for i in range(len(self.tiles)):
            if self.tiles[i] == 0:
                continue
            for j in range(i + 1, len(self.tiles)):
                if self.tiles[j] == 0:
                    continue
                if self.tiles[i] > self.tiles[j]:
                    inversions += 1

        blank_row_from_bottom = self.size - (self.blank_pos // self.size)

        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            return (inversions + blank_row_from_bottom) % 2 == 0

    def shuffle(self, moves: int = 100) -> "PuzzleState":
        import random

        tiles = list(range(1, self.n)) + [0]
        random.shuffle(tiles)

        inversions = 0
        for i in range(len(tiles)):
            if tiles[i] == 0:
                continue
            for j in range(i + 1, len(tiles)):
                if tiles[j] == 0:
                    continue
                if tiles[i] > tiles[j]:
                    inversions += 1

        blank_pos = tiles.index(0)
        blank_row_from_bottom = self.size - (blank_pos // self.size)

        if self.size % 2 == 0:
            if (inversions + blank_row_from_bottom) % 2 != 0:
                for i in range(len(tiles)):
                    if tiles[i] != 0:
                        for j in range(i + 1, len(tiles)):
                            if tiles[j] != 0:
                                tiles[i], tiles[j] = tiles[j], tiles[i]
                                break
                        break
        else:
            if inversions % 2 != 0:
                for i in range(len(tiles)):
                    if tiles[i] != 0:
                        for j in range(i + 1, len(tiles)):
                            if tiles[j] != 0:
                                tiles[i], tiles[j] = tiles[j], tiles[i]
                                break
                        break


        new_state = PuzzleState(self.size, tiles)
        return new_state

    def get_path(self) -> List["PuzzleState"]:
        if self._path_cache is not None:
            return self._path_cache

        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent
        self._path_cache = path[::-1]
        return self._path_cache
