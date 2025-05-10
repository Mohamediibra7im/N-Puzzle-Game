class Puzzle:
    def __init__(self, state):
        self.state = state

    def find_zero(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    return i, j

    def is_valid_move(self, direction):
        i, j = self.find_zero()
        n = len(self.state)
        if direction == "up":
            return i > 0
        elif direction == "down":
            return i < n - 1
        elif direction == "left":
            return j > 0
        elif direction == "right":
            return j < n - 1
        return False

    def move(self, direction):
        if not self.is_valid_move(direction):
            return None

        i, j = self.find_zero()
        new_state = [row[:] for row in self.state]

        if direction == "up":
            new_state[i][j], new_state[i - 1][j] = new_state[i - 1][j], new_state[i][j]
        elif direction == "down":
            new_state[i][j], new_state[i + 1][j] = new_state[i + 1][j], new_state[i][j]
        elif direction == "left":
            new_state[i][j], new_state[i][j - 1] = new_state[i][j - 1], new_state[i][j]
        elif direction == "right":
            new_state[i][j], new_state[i][j + 1] = new_state[i][j + 1], new_state[i][j]

        return Puzzle(new_state)

    def is_goal(self):
        n = len(self.state)
        goal = list(range(1, n * n -1)) + [0]
        flat = [tile for row in self.state for tile in row]
        return flat == goal