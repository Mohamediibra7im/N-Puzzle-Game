import unittest
from puzzle import PuzzleState
from heuristics import *
from search import best_first_search


class TestPuzzleState(unittest.TestCase):
    def setUp(self):
        self.size = 3
        self.goal_tiles = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        self.goal_state = PuzzleState(self.size, self.goal_tiles)

    def test_initialization(self):
        self.assertEqual(self.goal_state.tiles, self.goal_tiles)
        self.assertEqual(self.goal_state.blank_pos, 8)

    def test_move_valid(self):
        new_state = self.goal_state.move("up")
        self.assertEqual(new_state.tiles, [1, 2, 3, 4, 5, 0, 7, 8, 6])

        new_state = self.goal_state.move("left")
        self.assertEqual(new_state.tiles, [1, 2, 3, 4, 5, 6, 7, 0, 8])

    def test_move_invalid(self):
        self.assertIsNone(self.goal_state.move("down"))
        self.assertIsNone(self.goal_state.move("right"))

    def test_is_goal(self):
        self.assertTrue(self.goal_state.is_goal())
        not_goal = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 7, 0, 8])
        self.assertFalse(not_goal.is_goal())

    def test_get_valid_moves(self):
        self.assertEqual(set(self.goal_state.get_valid_moves()), {"up", "left"})
        center_blank = PuzzleState(self.size, [1, 2, 3, 4, 0, 5, 6, 7, 8])
        self.assertEqual(
            set(center_blank.get_valid_moves()), {"up", "down", "left", "right"}
        )

    def test_is_solvable(self):
        self.assertTrue(self.goal_state.is_solvable())
        unsolvable = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 8, 7, 0])
        self.assertFalse(unsolvable.is_solvable())


class TestHeuristics(unittest.TestCase):
    def setUp(self):
        self.size = 3
        self.goal_state = PuzzleState(self.size)

    def test_misplaced_tiles(self):
        self.assertEqual(misplaced_tiles(self.goal_state), 0)
        one_off = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 7, 0, 8])
        self.assertEqual(misplaced_tiles(one_off), 1)
        two_off = PuzzleState(self.size, [1, 2, 3, 4, 0, 6, 7, 5, 8])
        self.assertEqual(misplaced_tiles(two_off), 2)

    def test_manhattan_distance(self):
        self.assertEqual(manhattan_distance(self.goal_state), 0)
        one_move = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 7, 0, 8])
        self.assertEqual(manhattan_distance(one_move), 1)
        two_moves = PuzzleState(self.size, [1, 2, 3, 4, 0, 6, 7, 5, 8])
        self.assertEqual(manhattan_distance(two_moves), 2)

    def test_linear_conflict(self):
        self.assertEqual(linear_conflict(self.goal_state), 0)
        conflict_state = PuzzleState(self.size, [2, 1, 3, 4, 5, 6, 7, 8, 0])
        manhattan = manhattan_distance(conflict_state)
        self.assertEqual(linear_conflict(conflict_state), manhattan + 2)


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.size = 3
        self.goal_state = PuzzleState(self.size)

    def test_best_first_search(self):
        one_move_state = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 7, 0, 8])
        solution, stats = best_first_search(one_move_state, manhattan_distance)
        self.assertIsNotNone(solution)
        self.assertTrue(solution.is_goal())
        self.assertEqual(solution.depth, 1)

        harder_state = PuzzleState(self.size, [1, 2, 3, 0, 4, 6, 7, 5, 8])
        solution, stats = best_first_search(harder_state, manhattan_distance)
        self.assertIsNotNone(solution)
        self.assertTrue(solution.is_goal())
        self.assertGreaterEqual(solution.depth, 2)

    def test_unsolvable(self):
        unsolvable = PuzzleState(self.size, [1, 2, 3, 4, 5, 6, 8, 7, 0])
        solution, stats = best_first_search(unsolvable, manhattan_distance, max_nodes=1000)
        self.assertIsNone(solution)


if __name__ == "__main__":
    unittest.main()
