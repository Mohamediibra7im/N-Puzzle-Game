from puzzle import PuzzleState

def misplaced_tiles(state: PuzzleState) -> int:
    count = 0
    for i, tile in enumerate(state.tiles):
        if tile != 0 and tile != i + 1:
            count += 1
    return count

def manhattan_distance(state: PuzzleState) -> int:
    total = 0
    size = state.size
    for i, tile in enumerate(state.tiles):
        if tile == 0:
            continue
        goal_row, goal_col = divmod(tile - 1, size)
        current_row, current_col = divmod(i, size)
        total += abs(goal_row - current_row) + abs(goal_col - current_col)
    return total

def linear_conflict(state: PuzzleState) -> int:
    size = state.size
    manhattan = manhattan_distance(state)
    conflicts = 0
    for row in range(size):
        tiles_in_row = []
        for col in range(size):
            pos = row * size + col
            tile = state.tiles[pos]
            if tile == 0:
                continue
            goal_row, _ = divmod(tile - 1, size)
            if goal_row == row:
                tiles_in_row.append((tile, col))
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                if (
                    tiles_in_row[i][0] > tiles_in_row[j][0]
                    and tiles_in_row[i][1] < tiles_in_row[j][1]
                ):
                    conflicts += 2
    for col in range(size):
        tiles_in_col = []
        for row in range(size):
            pos = row * size + col
            tile = state.tiles[pos]
            if tile == 0:
                continue
            _, goal_col = divmod(tile - 1, size)
            if goal_col == col:
                tiles_in_col.append((tile, row))
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                if (
                    tiles_in_col[i][0] > tiles_in_col[j][0]
                    and tiles_in_col[i][1] < tiles_in_col[j][1]
                ):
                    conflicts += 2
    return manhattan + conflicts

def nilssons_sequence(state: PuzzleState) -> int:
    size = state.size
    if size != 3:
        return manhattan_distance(state)
    manhattan = manhattan_distance(state)
    sequence_score = 0
    if state.tiles[4] != 5:
        sequence_score += 1
    perimeter_positions = [0, 1, 2, 5, 8, 7, 6, 3]
    perimeter_values = [state.tiles[pos] for pos in perimeter_positions]
    goal_sequence = [1, 2, 3, 6, 9, 8, 7, 4]
    value_to_goal_index = {
        val: idx for idx, val in enumerate(goal_sequence) if val != 0
    }
    for i in range(len(perimeter_values)):
        if perimeter_values[i] == 0:
            continue
        current_val = perimeter_values[i]
        next_val = perimeter_values[(i + 1) % len(perimeter_values)]
        if next_val == 0:
            continue
        current_goal_idx = value_to_goal_index.get(current_val, -1)
        next_goal_idx = value_to_goal_index.get(next_val, -1)
        if current_goal_idx != -1 and next_goal_idx != -1:
            expected_next_idx = (current_goal_idx + 1) % 8
            if next_goal_idx != expected_next_idx:
                sequence_score += 2
    return manhattan + 3 * sequence_score
