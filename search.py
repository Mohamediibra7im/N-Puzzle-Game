import heapq

def best_first_search(start, heuristic_fn):
    frontier = []
    heapq.heappush(frontier, (heuristic_fn(start), start))
    explored = set()

    while frontier:
        _, current = heapq.heappop(frontier)

        if current.is_goal():
            return current.path + [current.state]

        state_tuple = tuple(tuple(row) for row in current.state)
        if state_tuple in explored:
            continue
        explored.add(state_tuple)

        for neighbor in current.get_neighbors():
            heapq.heappush(frontier, (heuristic_fn(neighbor), neighbor))

    return None


if __name__ == "__main__":
    from puzzle import Puzzle
    from heuristics import manhattan_distance

    size = int(input("Enter puzzle size (3 for 8-puzzle, 4 for 15-puzzle, 5 for 24-puzzle): "))
    total = size * size

    print(f"Enter the puzzle ({total} numbers from 0 to {total - 1}, row by row):")

    input_state = []
    for i in range(size):
        row = list(map(int, input().split()))
        input_state.append(row)

    start = Puzzle(input_state, size=size)
    path = best_first_search(start, manhattan_distance)

    if path:
        print(f"Solution found in {len(path) - 1} moves!")
        for step in path:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found.")
