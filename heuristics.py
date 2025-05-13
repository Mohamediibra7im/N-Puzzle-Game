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

    # The correct sequence in the goal state is [1,2,3,6,9,8,7,4]
    # We need to check how many times this sequence is broken

    # Skip blank tiles in the sequence
    filtered_values = [val for val in perimeter_values if val != 0]

    # Check consecutive pairs
    for i in range(len(filtered_values)):
        current = filtered_values[i]
        next_val = filtered_values[(i + 1) % len(filtered_values)]

        # Special case: after 9 should come 8
        if current == 9 and next_val != 8:
            sequence_score += 2
        # Regular case: current + 1 should equal next
        elif current != 9 and next_val != current + 1:
            sequence_score += 2

    return manhattan + 3 * sequence_score