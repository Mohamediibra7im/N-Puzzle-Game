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
from heuristics import *


class NPuzzleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.size = 3  # Default puzzle size
        self.heuristic_fn = manhattan_distance  # Default heuristic
        self.max_nodes = 100000  # Default max nodes
        self.search_stats = {"nodes_expanded": 0}  # Store search statistics
        self.initUI()

    def initUI(self):
        self.setWindowTitle("N-Puzzle Game")
        self.setGeometry(100, 100, 400, 500)

        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Puzzle grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.layout.addWidget(self.grid_widget)

        # Board size selection dropdown
        self.size_dropdown = QComboBox()
        self.size_dropdown.addItems(["3x3", "4x4", "5x5"])
        self.size_dropdown.currentIndexChanged.connect(self.update_size)
        self.layout.addWidget(self.size_dropdown)

        # Heuristic selection dropdown
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

        # Shuffle and Solve buttons
        self.shuffle_button = QPushButton("Shuffle")
        self.shuffle_button.clicked.connect(self.shuffle_puzzle)
        self.layout.addWidget(self.shuffle_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.layout.addWidget(self.solve_button)

        # Plot button
        self.plot_button = QPushButton("Generate Plot")
        self.plot_button.clicked.connect(self.generate_plot)
        self.layout.addWidget(self.plot_button)

        # Status label
        self.status_label = QLabel("Welcome to N-Puzzle!")
        self.layout.addWidget(self.status_label)

        # Initialize puzzle state
        self.goal_state = PuzzleState(self.size)
        self.current_state = self.goal_state
        self.update_grid()

    def update_grid(self):
        """Update the puzzle grid display."""
        # Clear the existing grid
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
        """Shuffle the puzzle."""
        self.current_state = self.goal_state.shuffle(20)
        self.update_grid()
        self.status_label.setText("Puzzle shuffled!")

    def solve_puzzle(self):
        """Solve the puzzle using Best-First Search."""
        self.status_label.setText("Solving...")
        QApplication.processEvents()  # Update the UI immediately

        start_time = time.time()
        solution, stats = best_first_search(
            self.current_state, self.heuristic_fn, self.max_nodes
        )
        self.search_stats = stats  # Store the latest search statistics
        elapsed = time.time() - start_time

        if solution:
            self.status_label.setText(
                f"Solution found in {elapsed:.2f} seconds! Depth: {solution.depth}"
            )
            self.show_solution_path(solution)
        else:
            self.status_label.setText("No solution found within node limit.")

    def show_solution_path(self, solution):
        """Show the solution path step by step."""
        path = solution.get_path()
        for state in path:
            self.current_state = state
            self.update_grid()
            QApplication.processEvents()
            time.sleep(0.5)  # Pause to visualize each step

        QMessageBox.information(self, "Solution", "Solution path completed!")

    def update_heuristic(self):
        """Update the heuristic function based on user selection."""
        selected_heuristic = self.heuristic_dropdown.currentText()
        if selected_heuristic == "Manhattan Distance":
            self.heuristic_fn = manhattan_distance
        elif selected_heuristic == "Misplaced Tiles":
            self.heuristic_fn = misplaced_tiles
        elif selected_heuristic == "Linear Conflict":
            self.heuristic_fn = linear_conflict
        elif selected_heuristic == "Nilssons Sequence":
            self.heuristic_fn = nilssons_sequence

    def update_size(self):
        """Update the puzzle size based on user selection."""
        selected_size = self.size_dropdown.currentText()
        if selected_size == "3x3":
            self.size = 3
        elif selected_size == "4x4":
            self.size = 4
        elif selected_size == "5x5":
            self.size = 5

        # Reset the puzzle state
        self.goal_state = PuzzleState(self.size)
        self.current_state = self.goal_state
        self.update_grid()
        self.status_label.setText(f"Board size updated to {self.size}x{self.size}!")

    def generate_plot(self):
        """Generate a plot of nodes explored during the last search."""
        if not self.search_stats or "nodes_explored_at_steps" not in self.search_stats:
            self.status_label.setText("No search data available to plot!")
            return

        # Get the data from the search statistics
        nodes_explored = self.search_stats["nodes_explored_at_steps"]
        iterations = list(range(len(nodes_explored)))

        plt.figure(figsize=(8, 6))
        plt.plot(iterations, nodes_explored, "b-", label="Nodes Explored")
        plt.title("Nodes Explored vs. Iterations")
        plt.xlabel("Iterations")
        plt.ylabel("Number of Nodes Explored")
        plt.grid(True)
        plt.legend()

        # Save the plot to a file
        plt.savefig("nodes_explored.png")
        plt.close()

        self.status_label.setText("Plot generated as 'nodes_explored.png'!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = NPuzzleGame()
    game.show()
    sys.exit(app.exec_())
