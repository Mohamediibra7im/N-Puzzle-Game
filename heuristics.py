from puzzle import PuzzleState

def misplaced_tiles(state: PuzzleState) -> int:
    """Count number of tiles not in their goal position (excluding blank)"""
    count = 0
    for i, tile in enumerate(state.tiles):
        if tile != 0 and tile != i + 1:
            count += 1
    return count

def manhattan_distance(state: PuzzleState) -> int:
    """Sum of Manhattan distances between each tile and its goal position"""
    total = 0
    size = state.size
    for i, tile in enumerate(state.tiles):
        if tile == 0:
            continue  # Skip blank tile
        goal_row, goal_col = divmod(tile - 1, size)
        current_row, current_col = divmod(i, size)
        total += abs(goal_row - current_row) + abs(goal_col - current_col)
    return total

def linear_conflict(state: PuzzleState) -> int:
    """Manhattan distance plus linear conflict penalty"""
    size = state.size
    manhattan = manhattan_distance(state)
    conflicts = 0

    # Check rows
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

        # Check for conflicts in this row
        for i in range(len(tiles_in_row)):
            for j in range(i + 1, len(tiles_in_row)):
                if tiles_in_row[i][0] > tiles_in_row[j][0]:
                    conflicts += 2

    # Check columns
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

        # Check for conflicts in this column
        for i in range(len(tiles_in_col)):
            for j in range(i + 1, len(tiles_in_col)):
                if tiles_in_col[i][0] > tiles_in_col[j][0]:
                    conflicts += 2

    return manhattan + conflicts

def nilssons_sequence(state: PuzzleState) -> int:
    """Correct implementation of Nilsson's sequence score heuristic"""
    size = state.size
    if size != 3:  # Only properly defined for 3x3 puzzles
        return manhattan_distance(state)

    # Manhattan distance component
    manhattan = manhattan_distance(state)
    sequence_score = 0

    # 1. Center tile check (position 4 should be 5)
    if state.tiles[4] != 5:
        sequence_score += 1

    # 2. Perimeter sequence check
    # Define perimeter positions in clockwise order (top, right, bottom, left)
    perimeter_positions = [0, 1, 2, 5, 8, 7, 6, 3]
    perimeter_values = [state.tiles[pos] for pos in perimeter_positions]

    # The correct sequence in the goal state is [1, 2, 3, 6, 9, 8, 7, 4]
    goal_sequence = [1, 2, 3, 6, 9, 8, 7, 4]
    # Create a mapping of values to their indices in the goal sequence
    value_to_goal_index = {val: idx for idx, val in enumerate(goal_sequence) if val != 0}

    # Filter out the blank tile (0) and get valid value-position pairs
    valid_pairs = [(val, idx) for idx, val in enumerate(perimeter_values) if val != 0]
    if len(valid_pairs) < 2:  # Not enough values to check sequence
        return manhattan + 3 * sequence_score

    # Check for sequence breaks by comparing with the goal sequence order
    for i in range(len(valid_pairs)):
        current_val, current_pos = valid_pairs[i]
        next_idx = (i + 1) % len(valid_pairs)
        next_val, _ = valid_pairs[next_idx]

        current_goal_idx = value_to_goal_index.get(current_val, -1)
        next_goal_idx = value_to_goal_index.get(next_val, -1)

        if current_goal_idx != -1 and next_goal_idx != -1:
            expected_next_idx = (current_goal_idx + 1) % 8
            if next_goal_idx != expected_next_idx and next_val != 0:
                sequence_score += 2

    return manhattan + 3 * sequence_score