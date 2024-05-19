import tkinter as tk
from tkinter import ttk
from grid_manager import GridManager
from robot import Robot
from package import Package
from goal import Goal
from pathfinding import Pathfinding

class WarehouseGUI:
    def __init__(self):
        self.algorithm_choice = None
        self.option_menu = None
        self.canvas = None

        self.button_pause = None
        self.button_start = None
        self.button_reset = None

        self.button_select_goal = None
        self.button_add_package = None
        self.button_add_robot = None

        self.left_frame = None

        self.root = tk.Tk()
        self.root.title("Warehouse Robot Simulation")

        # Set the theme
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')

        self.grid_manager = GridManager(width=15, height=15)
        self.pathfinder = Pathfinding(self.grid_manager)
        self.pathfinding_algorithm = 'a_star'

        self.current_action = None
        self.highlight_rect = None

        self.cell_size = 0
        self.simulation_running = False

        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

        self.robot_paths = {}
        self.counter = 0

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Initialize a frame for buttons
        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Add buttons to the frame
        self.button_add_robot = ttk.Button(self.left_frame, text="Add Robot", command=self.prepare_add_robot)
        self.button_add_robot.pack(side="top", padx=5, pady=5)

        self.button_add_package = ttk.Button(self.left_frame, text="Add Package", command=self.prepare_add_package)
        self.button_add_package.pack(side="top", padx=5, pady=5)

        self.button_select_goal = ttk.Button(self.left_frame, text="Select Goal", command=self.prepare_add_goal)
        self.button_select_goal.pack(side="top", padx=5, pady=5)

        self.button_start = ttk.Button(self.left_frame, text="Start", command=self.start_simulation)
        self.button_start.pack(side="top", padx=5, pady=5)

        self.button_pause = ttk.Button(self.left_frame, text="Pause", command=self.stop_simulation)
        self.button_pause.pack(side="top", padx=5, pady=5)

        self.button_reset = ttk.Button(self.left_frame, text="Reset", command=self.reset)
        self.button_reset.pack(side="top", padx=5, pady=5)

        self.algorithm_choice = tk.StringVar(value=self.pathfinding_algorithm)
        self.option_menu = ttk.OptionMenu(self.left_frame, self.algorithm_choice, 'a_star', 'dijkstra', 'bfs', 'dfs', 'greedy_best_first', command=self.set_algorithm)
        self.option_menu.pack(side="top", padx=5, pady=5)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def set_algorithm(self, algorithm):
        self.pathfinding_algorithm = algorithm

    def prepare_add_robot(self):
        self.current_action = 'add_robot'
        self.root.config(cursor="cross")

    def prepare_add_package(self):
        self.current_action = 'add_package'
        self.root.config(cursor="cross")

    def prepare_add_goal(self):
        self.current_action = 'add_goal'
        self.root.config(cursor="cross")

    def on_canvas_click(self, event):
        x = (event.x - self.padding_x) // self.cell_size
        y = (event.y - self.padding_y) // self.cell_size
        position = (x, y)

        if self.current_action == 'add_robot':
            robot = Robot(id=len(self.grid_manager.robots), position=position)
            self.grid_manager.add_robot(robot)
        elif self.current_action == 'add_package':
            package = Package(id=len(self.grid_manager.packages), position=position)
            self.grid_manager.add_package(package)
        elif self.current_action == 'add_goal':
            goal = Goal(id=len(self.grid_manager.goals), position=position)
            self.grid_manager.add_goal(goal)

        self.current_action = None
        self.root.config(cursor="")
        self.clear_highlight()
        self.update_canvas()

    def on_mouse_move(self, event):
        x = (event.x - self.padding_x) // self.cell_size
        y = (event.y - self.padding_y) // self.cell_size

        if self.current_action == 'add_robot':
            self.highlight_position((x, y), Robot.color)
        elif self.current_action == 'add_package':
            self.highlight_position((x, y), Package.color)
        elif self.current_action == 'add_goal':
            self.highlight_position((x, y), Goal.color)

    def highlight_position(self, position, color):
        if self.highlight_rect:
            self.canvas.delete(self.highlight_rect)
        x, y = position
        if 0 <= x < self.grid_manager.width and 0 <= y < self.grid_manager.height:
            self.highlight_rect = self.canvas.create_rectangle(
                x * self.cell_size + self.padding_x,
                y * self.cell_size + self.padding_y,
                (x + 1) * self.cell_size + self.padding_x,
                (y + 1) * self.cell_size + self.padding_y,
                outline=color,
                width=2
            )

    def clear_highlight(self):
        if self.highlight_rect:
            self.canvas.delete(self.highlight_rect)
            self.highlight_rect = None

    def reset(self):
        self.grid_manager.reset()
        self.update_canvas()

    def start_simulation(self):
        if (len(self.grid_manager.goals) > 0 and
                len(self.grid_manager.packages) > 0 and
                len(self.grid_manager.robots) > 0):

            print("[START] simulation_running being set to true and updating simulation")
            self.simulation_running = True
            self.update_simulation()
        else:
            print(f"Number of Robots: {len(self.grid_manager.robots)}")
            print(f"Number of Packages: {len(self.grid_manager.packages)}")
            print(f"Number of Goals: {len(self.grid_manager.goals)}")

    def stop_simulation(self):
        self.simulation_running = False

    def update_simulation(self):
        if self.simulation_running:
            for robot in self.grid_manager.robots:
                robot.calculate_path(self.grid_manager)

            self.grid_manager.move_robots()
            self.update_canvas()
            self.root.after(500, self.update_simulation)

    def update_canvas(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_size = min(width // self.grid_manager.width, height // self.grid_manager.height)

        self.padding_x = (width - self.cell_size * self.grid_manager.width) // 2
        self.padding_y = (height - self.cell_size * self.grid_manager.height) // 2

        for y in range(self.grid_manager.height):
            for x in range(self.grid_manager.width):
                x1 = x * self.cell_size + self.padding_x
                y1 = y * self.cell_size + self.padding_y
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                items = self.grid_manager.grid[y][x]

                if items:
                    item_height = self.cell_size // len(items)
                    for i, item in enumerate(items):
                        item_y1 = y1 + i * item_height
                        item_y2 = item_y1 + item_height
                        color = item.color if hasattr(item, 'color') else 'white'
                        self.canvas.create_rectangle(x1, item_y1, x2, item_y2, fill=color)
                        # Draw the item ID as text on top of the rectangle
                        if isinstance(item, Robot):
                            self.canvas.create_text((x1 + x2) // 2, (item_y1 + item_y2) // 2,
                                                    text=str(item.id)+","+str(len(item.packages)), fill="black")
                        elif isinstance(item, Package):
                            self.canvas.create_text((x1 + x2) // 2, (item_y1 + item_y2) // 2,
                                                    text=str(item.id), fill="black")
                        elif isinstance(item, Goal):
                            self.canvas.create_text((x1 + x2) // 2, (item_y1 + item_y2) // 2,
                                                    text=str(item.id) + "," + str(len(item.packages)), fill="black")

                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1, stipple="gray12")

    def on_resize(self, event):
        self.update_canvas()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WarehouseGUI()
    app.run()
