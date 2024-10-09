# maze.py
__version__ = "1.1.1"
import copy  # Importamos el módulo copy para hacer copias profundas

class Node:
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return not self.frontier

    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else:
            return self.frontier.pop(0)


class Maze:
    def __init__(self, filename):
        # Leer el archivo y configurar el laberinto
        with open(filename) as f:
            contents = f.read()

        # Validar punto de inicio y objetivo
        if contents.count("A") != 1:
            raise Exception("El laberinto debe tener exactamente un punto de inicio 'A'")
        if contents.count("B") != 1:
            raise Exception("El laberinto debe tener exactamente un punto objetivo 'B'")

        # Determinar altura y anchura
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Crear la cuadrícula de paredes
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)

        self.solution = None

    def __str__(self):
        output = []
        solution = self.solution[1] if self.solution else None
        for i, row in enumerate(self.walls):
            line = ""
            for j, col in enumerate(row):
                if col:
                    line += "█"
                elif (i, j) == self.start:
                    line += "A"
                elif (i, j) == self.goal:
                    line += "B"
                elif solution and (i, j) in solution:
                    line += "*"
                else:
                    line += " "
            output.append(line)
        return "\n".join(output)

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []
        for action, (r, c) in candidates:
            if (
                0 <= r < self.height
                and 0 <= c < self.width
                and not self.walls[r][c]
            ):
                result.append((action, (r, c)))
        return result

    def solve(self, method="DFS"):
        """Encuentra una solución al laberinto usando el método especificado ('DFS' o 'BFS')."""
        # Hacer una copia profunda de la instancia actual
        copy_maze = copy.deepcopy(self)

        # Inicializar contadores y conjuntos
        copy_maze.num_explored = 0
        copy_maze.explored = set()

        # Inicializar frontera
        start_node = Node(state=copy_maze.start, parent=None, action=None)
        if method == "DFS":
            frontier = StackFrontier()
        elif method == "BFS":
            frontier = QueueFrontier()
        else:
            raise ValueError("El método debe ser 'DFS' o 'BFS'")
        frontier.add(start_node)

        while True:
            if frontier.empty():
                raise Exception("No hay solución para este laberinto")

            node = frontier.remove()
            copy_maze.num_explored += 1

            if node.state == copy_maze.goal:
                # Se encontró la solución
                actions = []
                cells = []
                while node.parent:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                copy_maze.solution = (actions, cells)
                return copy_maze  # Devolvemos la copia resuelta

            copy_maze.explored.add(node.state)

            for action, state in copy_maze.neighbors(node.state):
                if not frontier.contains_state(state) and state not in copy_maze.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def to_img(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw

        cell_size = 50
        cell_border = 2
        img = Image.new(
            "RGBA", (self.width * cell_size, self.height * cell_size), "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    fill = (40, 40, 40)
                elif (i, j) == self.start:
                    fill = (255, 0, 0)
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)
                elif solution and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)
                elif show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)
                else:
                    fill = (237, 240, 252)

                draw.rectangle(
                    [
                        (
                            j * cell_size + cell_border,
                            i * cell_size + cell_border,
                        ),
                        (
                            (j + 1) * cell_size - cell_border,
                            (i + 1) * cell_size - cell_border,
                        ),
                    ],
                    fill=fill,
                )

        img.save(filename)


def read(filepath):
    return Maze(filepath)


import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

def create(x=6, y=6, start='A', end='B', wall='#', empty=' '):
    """
    Create a maze interactively using a graphical interface.
    :param x: Width of the maze
    :param y: Height of the maze
    :param start: Character for the start position
    :param end: Character for the end position
    :param wall: Character for the walls
    :param empty: Character for empty spaces
    :return: Saves the maze as a .txt file
    """

    class MazeCreator:
        def __init__(self, x, y, start_char, end_char, wall_char, empty_char):
            self.root = tk.Tk()
            self.root.title("Maze Creator")
            self.x = x
            self.y = y
            self.start_char = start_char
            self.end_char = end_char
            self.wall_char = wall_char
            self.empty_char = empty_char
            self.start_pos = None
            self.end_pos = None
            self.grid = [[0 for _ in range(x)] for _ in range(y)]
            self.buttons = [[None for _ in range(x)] for _ in range(y)]
            self.current_tool = "wall"  # Default mode is wall
            self.create_widgets()

            # Set window to be on top
            self.root.attributes('-topmost', True)
            self.root.update()

        def create_widgets(self):
            # Frame for the maze grid with padding (margin around the grid)
            maze_frame = tk.Frame(self.root, padx=20, pady=20, bg='#f0f0f0')  # Background to make it modern
            maze_frame.pack()

            for i in range(self.y):
                for j in range(self.x):
                    btn = tk.Button(maze_frame, width=2, height=1, command=lambda i=i, j=j: self.on_cell_click(i, j))
                    btn.grid(row=i, column=j)
                    self.buttons[i][j] = btn

            # Frame for the controls with padding to create some space
            control_frame = tk.Frame(self.root, padx=20, pady=20, bg='#f0f0f0')
            control_frame.pack()

            # Styling for modern buttons (neutral colors, rounded corners)
            button_style = {
                "bg": "#E0E0E0",  # Light gray for a modern neutral look
                "fg": "black",  # Black text color
                "font": ("Segoe UI", 10),  # Font similar to Windows 11
                "bd": 0,  # No border
                "activebackground": "#C0C0C0",  # Slightly darker gray when clicked
                "relief": "flat",  # Flat style for modern look
                "padx": 10,  # Padding inside the button for more space
                "pady": 5
            }

            # Buttons to select start and end points with modern styling
            self.start_button = tk.Button(control_frame, text="Select Start", command=self.set_start_tool, **button_style)
            self.start_button.grid(row=0, column=0, padx=10, pady=10)

            self.end_button = tk.Button(control_frame, text="Select End", command=self.set_end_tool, **button_style)
            self.end_button.grid(row=0, column=1, padx=10, pady=10)

            # Button to save the maze with modern styling
            save_button = tk.Button(self.root, text="Save Maze", command=self.save_maze_as_txt, **button_style)
            save_button.pack(padx=20, pady=5)  # Adjusted padding to 5 to move it up

        def set_start_tool(self):
            self.current_tool = "start"
            self.highlight_button(self.start_button)
            self.unhighlight_button(self.end_button)

        def set_end_tool(self):
            self.current_tool = "end"
            self.highlight_button(self.end_button)
            self.unhighlight_button(self.start_button)

        def highlight_button(self, button):
            button.config(bg="lightgray")  # Highlight the selected button

        def unhighlight_button(self, button):
            button.config(bg="#E0E0E0")  # Reset the button to its neutral color

        def set_wall_tool(self):
            self.current_tool = "wall"
            # Reset button colors when returning to wall mode
            self.unhighlight_button(self.start_button)
            self.unhighlight_button(self.end_button)

        def on_cell_click(self, i, j):
            if self.current_tool == "start":
                if self.start_pos:
                    prev_i, prev_j = self.start_pos
                    self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.start_pos = (i, j)
                self.buttons[i][j].config(bg="green")
                self.grid[i][j] = 0
                # Automatically return to wall mode
                self.set_wall_tool()
            elif self.current_tool == "end":
                if self.end_pos:
                    prev_i, prev_j = self.end_pos
                    self.buttons[prev_i][prev_j].config(bg="SystemButtonFace")
                self.end_pos = (i, j)
                self.buttons[i][j].config(bg="red")
                self.grid[i][j] = 0
                # Automatically return to wall mode
                self.set_wall_tool()
            elif self.current_tool == "wall":
                if (i, j) != self.start_pos and (i, j) != self.end_pos:
                    current_color = self.buttons[i][j].cget("bg")
                    if current_color == "black":
                        self.buttons[i][j].config(bg="SystemButtonFace")
                        self.grid[i][j] = 0
                    else:
                        self.buttons[i][j].config(bg="black")
                        self.grid[i][j] = 1

        def generate_maze_str(self):
            maze_lines = []
            for i, row in enumerate(self.grid):
                line = ""
                for j, cell in enumerate(row):
                    if (i, j) == self.start_pos:
                        line += self.start_char
                    elif (i, j) == self.end_pos:
                        line += self.end_char
                    elif cell == 1:  # Wall
                        line += self.wall_char
                    else:  # Empty space
                        line += self.empty_char
                maze_lines.append(line)
            return "\n".join(maze_lines)

        def save_maze_as_txt(self):
            if not self.start_pos or not self.end_pos:
                messagebox.showwarning("Warning", "You must select a start and an end position.")
                return
            maze_str = self.generate_maze_str()

            # Get the directory of the current script
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Open file dialog to save the maze, defaulting to the script's directory
            file_path = filedialog.asksaveasfilename(initialdir=current_directory,
                                                     defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt")])
            if file_path:
                with open(file_path, "w") as f:
                    f.write(maze_str)
                print(f"Maze saved successfully to {file_path}.")
                self.root.destroy()

        def run(self):
            self.root.mainloop()

    maze_creator = MazeCreator(x, y, start, end, wall, empty)
    maze_creator.run()
