import sys
import time
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QGridLayout,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLabel,
    QMessageBox,
    QComboBox,
)
from PyQt5.QtCore import Qt
from puzzle import PuzzleState
from search import best_first_search
from heuristics import (
    manhattan_distance,
    misplaced_tiles,
    nilssons_sequence,
    linear_conflict,
)


class NPuzzleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.size = 3
        self.heuristic_fn = manhattan_distance
        self.max_nodes = 100000
        self.search_stats = {}
        self.initUI()

    def initUI(self):
        self.setWindowTitle("N-Puzzle Game")
        self.setGeometry(200, 200, 400, 500)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.layout.addWidget(self.grid_widget)
        self.size_dropdown = QComboBox()
        self.size_dropdown.addItems(["3x3", "4x4", "5x5"])
        self.size_dropdown.currentIndexChanged.connect(self.update_size)
        self.layout.addWidget(self.size_dropdown)
        self.heuristic_dropdown = QComboBox()
        self.heuristic_dropdown.addItems(
            [
                "Manhattan Distance",
                "Misplaced Tiles",
                "Nilssons Sequence",
                "Linear Conflict",
            ]
        )
        self.heuristic_dropdown.currentIndexChanged.connect(self.update_heuristic)
        self.layout.addWidget(self.heuristic_dropdown)
        self.shuffle_button = QPushButton("Shuffle")
        self.shuffle_button.clicked.connect(self.shuffle_puzzle)
        self.layout.addWidget(self.shuffle_button)
        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.layout.addWidget(self.solve_button)
        self.compare_button = QPushButton("Compare Heuristics")
        self.compare_button.clicked.connect(self.compare_heuristics)
        self.layout.addWidget(self.compare_button)
        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.generate_plot)
        self.layout.addWidget(self.plot_button)
        self.status_label = QLabel("Welcome to N-Puzzle!")
        self.layout.addWidget(self.status_label)
        self.goal_state = PuzzleState(self.size)
        self.current_state = self.goal_state
        self.update_grid()

    def update_grid(self):
        for i in reversed(range(self.grid_layout.count())):
            self.grid_layout.itemAt(i).widget().setParent(None)
        for i in range(self.size):
            for j in range(self.size):
                tile_value = self.current_state.tiles[i * self.size + j]
                button = QPushButton(str(tile_value) if tile_value != 0 else "")
                button.setFixedSize(80, 80)
                button.setStyleSheet("font-size: 20px;")
                self.grid_layout.addWidget(button, i, j)

    def shuffle_puzzle(self):
        moves = self.size * self.size * 10
        self.current_state = self.goal_state.shuffle(moves)
        self.update_grid()
        self.status_label.setText("Puzzle shuffled!")
        self.search_stats = {}

    def solve_puzzle(self):
        if not self.current_state.is_solvable():
            QMessageBox.warning(
                self, "Unsolvable Puzzle", "The current puzzle is unsolvable."
            )
            self.status_label.setText("Unsolvable puzzle!")
            return

        heuristic_name = self.heuristic_dropdown.currentText()
        self.status_label.setText(
            f"Solving with Best-First Search and {heuristic_name}..."
        )
        QApplication.processEvents()
        start_time = time.perf_counter()
        solution, stats = best_first_search(
            self.current_state, self.heuristic_fn, self.max_nodes
        )
        elapsed = time.perf_counter() - start_time
        self.search_stats[heuristic_name] = {
            "solution": solution,
            "stats": stats,
            "time": elapsed,
        }
        print(f"{heuristic_name}: {elapsed:.6f} seconds")

        if solution:
            self.status_label.setText("Solution found! Visualizing...")
            self.show_solution_path(solution)
        else:
            self.status_label.setText("No solution found within node limit.")

    def show_solution_path(self, solution):
        path = solution.get_path()
        for state in path:
            self.current_state = state
            self.update_grid()
            QApplication.processEvents()
            time.sleep(0.5)
        self.status_label.setText("Solution path completed!")

    def compare_heuristics(self):
        if not self.current_state.is_solvable():
            QMessageBox.warning(
                self, "Unsolvable Puzzle", "The current puzzle is unsolvable."
            )
            self.status_label.setText("Unsolvable puzzle!")
            return

        self.status_label.setText("Comparing all heuristics with Best-First Search...")
        QApplication.processEvents()
        heuristics = [
            ("Manhattan Distance", manhattan_distance),
            ("Misplaced Tiles", misplaced_tiles),
            ("Nilssons Sequence", nilssons_sequence),
            ("Linear Conflict", linear_conflict),
        ]
        self.search_stats = {}
        for heuristic_name, heuristic_fn in heuristics:
            self.status_label.setText(f"Solving with {heuristic_name}...")
            QApplication.processEvents()
            start_time = time.perf_counter()
            solution, stats = best_first_search(
                self.current_state, heuristic_fn, self.max_nodes
            )
            elapsed = time.perf_counter() - start_time
            self.search_stats[heuristic_name] = {
                "solution": solution,
                "stats": stats,
                "time": elapsed,
            }
            print(f"{heuristic_name}: {elapsed:.6f} seconds")

        results_text = "Heuristic Comparison Results (Best-First Search):\n\n"
        for heuristic_name, data in self.search_stats.items():
            stats = data["stats"]
            elapsed = data["time"]
            solution = data["solution"]
            if solution:
                results_text += (
                    f"{heuristic_name}:\n"
                    f"  Time: {elapsed:.4f} seconds\n"
                    f"  Depth: {solution.depth}\n"
                    f"  Nodes Expanded: {stats['nodes_expanded']}\n\n"
                )
            else:
                results_text += (
                    f"{heuristic_name}:\n"
                    f"  No solution found within node limit\n"
                    f"  Time: {elapsed:.4f} seconds\n"
                    f"  Nodes Expanded: {stats['nodes_expanded']}\n\n"
                )
        QMessageBox.information(self, "Heuristic Comparison", results_text)
        self.status_label.setText("Comparison results displayed.")

    def update_heuristic(self):
        selected_heuristic = self.heuristic_dropdown.currentText()
        if selected_heuristic == "Manhattan Distance":
            self.heuristic_fn = manhattan_distance
        elif selected_heuristic == "Misplaced Tiles":
            self.heuristic_fn = misplaced_tiles
        elif selected_heuristic == "Linear Conflict":
            self.heuristic_fn = linear_conflict
        elif selected_heuristic == "Nilssons Sequence":
            self.heuristic_fn = nilssons_sequence
        self.status_label.setText(f"Heuristic set to {selected_heuristic}")

    def update_size(self):
        selected_size = self.size_dropdown.currentText()
        if selected_size == "3x3":
            self.size = 3
        elif selected_size == "4x4":
            self.size = 4
        elif selected_size == "5x5":
            self.size = 5
        self.goal_state = PuzzleState(self.size)
        self.current_state = self.goal_state
        self.update_grid()
        self.status_label.setText(f"Board size updated to {selected_size}!")
        self.search_stats = {}

    def generate_plot(self):
        if not self.search_stats:
            QMessageBox.warning(self, "No Data", "No search data available to plot!")
            self.status_label.setText("No search data available to plot!")
            return
        plt.figure(figsize=(10, 6))
        for heuristic_name, data in self.search_stats.items():
            stats = data["stats"]
            if "nodes_explored_at_steps" not in stats:
                continue
            nodes_explored = stats["nodes_explored_at_steps"]
            iterations = list(range(len(nodes_explored)))
            plt.plot(
                iterations,
                nodes_explored,
                label=f"{heuristic_name} (Time: {data['time']:.4f}s)",
            )
        plt.title(
            "Nodes Explored vs. Iterations for Each Heuristic (Best-First Search)"
        )
        plt.xlabel("Iterations")
        plt.ylabel("Number of Nodes Explored")
        plt.grid(True)
        plt.legend()
        plt.savefig("./Diagrams/nodes_explored_comparison.png")
        plt.close()
        self.status_label.setText(
            "Comparison plot generated as 'nodes_explored_comparison.png'!"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NPuzzleGame()
    game.show()
    sys.exit(app.exec_())
