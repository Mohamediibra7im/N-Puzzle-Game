import heapq
from typing import Callable, Optional, Tuple
from puzzle import PuzzleState


def best_first_search(
    initial_state: PuzzleState,
    heuristic_fn: Callable[[PuzzleState], int],
    max_nodes: int = 100000,
) -> Tuple[Optional[PuzzleState], dict]:
    """
    Implement Best-First Search using the given heuristic function.

    Args:
        initial_state: Starting puzzle state
        heuristic_fn: Heuristic function to use
        max_nodes: Maximum number of nodes to explore before giving up

    Returns:
        Tuple containing:
        - The goal state (with path information) if found, None otherwise
        - Dictionary with search statistics
    """
    # Priority queue: (heuristic value, node count, state)
    # Using node count as tie-breaker to ensure we don't compare states directly
    priority_queue = []
    node_count = 0
    heapq.heappush(
        priority_queue, (heuristic_fn(initial_state), node_count, initial_state)
    )
    node_count += 1

    explored = set()
    stats = {
        "nodes_expanded": 0,
        "max_queue_size": 1,
        "start_heuristic": heuristic_fn(initial_state),
    }

    while priority_queue:
        # Update max queue size
        if len(priority_queue) > stats["max_queue_size"]:
            stats["max_queue_size"] = len(priority_queue)

        # Get next state to explore
        _, _, current = heapq.heappop(priority_queue)
        stats["nodes_expanded"] += 1

        # Check if we've reached the goal
        if current.is_goal():
            stats["solution_depth"] = current.depth
            stats["end_heuristic"] = 0
            return current, stats

        # Skip if we've already explored this state
        state_hash = hash(tuple(current.tiles))
        if state_hash in explored:
            continue

        explored.add(state_hash)

        # Check node limit
        if stats["nodes_expanded"] >= max_nodes:
            stats["end_heuristic"] = heuristic_fn(current)
            return None, stats

        # Explore all valid moves
        for move in current.get_valid_moves():
            new_state = current.move(move)
            if new_state is not None and hash(tuple(new_state.tiles)) not in explored:
                heapq.heappush(
                    priority_queue, (heuristic_fn(new_state), node_count, new_state)
                )
                node_count += 1

    stats["end_heuristic"] = heuristic_fn(current)
    return None, stats
