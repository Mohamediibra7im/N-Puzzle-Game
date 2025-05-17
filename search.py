import heapq
from typing import Callable, Optional, Tuple
from puzzle import PuzzleState

def best_first_search(
    initial_state: PuzzleState,
    heuristic_fn: Callable[[PuzzleState], int],
    max_nodes: int = 100000,
) -> Tuple[Optional[PuzzleState], dict]:
    """
    Implement Best-First Search using only the heuristic function h(n).

    Args:
        initial_state: Starting puzzle state.
        heuristic_fn: Heuristic function to estimate cost to goal.
        max_nodes: Maximum number of nodes to explore before giving up.

    Returns:
        Tuple containing:
        - The goal state (with path information) if found, None otherwise.
        - Dictionary with search statistics including nodes_explored_at_steps.
    """
    # Priority queue: (h(n), node count, state)
    priority_queue = []
    node_count = 0
    h = heuristic_fn(initial_state)
    heapq.heappush(priority_queue, (h, node_count, initial_state))
    node_count += 1

    explored = set()
    stats = {
        "nodes_expanded": 0,
        "max_queue_size": 1,
        "start_heuristic": h,
        "nodes_explored_at_steps": [0],
    }

    while priority_queue:
        if len(priority_queue) > stats["max_queue_size"]:
            stats["max_queue_size"] = len(priority_queue)

        _, _, current = heapq.heappop(priority_queue)
        stats["nodes_expanded"] += 1
        stats["nodes_explored_at_steps"].append(stats["nodes_expanded"])

        if current.is_goal():
            stats["solution_depth"] = current.depth
            stats["end_heuristic"] = 0
            return current, stats

        state_hash = hash(tuple(current.tiles))
        if state_hash in explored:
            continue

        explored.add(state_hash)

        if stats["nodes_expanded"] >= max_nodes:
            stats["end_heuristic"] = heuristic_fn(current)
            return None, stats

        for move in current.get_valid_moves():
            new_state = current.move(move)
            if new_state is not None and hash(tuple(new_state.tiles)) not in explored:
                h = heuristic_fn(new_state)
                heapq.heappush(priority_queue, (h, node_count, new_state))
                node_count += 1

    stats["end_heuristic"] = heuristic_fn(current)
    return None, stats