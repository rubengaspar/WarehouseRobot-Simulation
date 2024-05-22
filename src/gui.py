# gui.py
import tkinter as tk
from tkinter import ttk

from src.grid import Grid
from src.robot import Robot
from src.package import Package
from src.goal import Goal
from src.position import Position


class GUI:
    def __init__(self, grid: 'Grid'):
        self.root = tk.Tk()
        self.root.title("Warehouse Robot Simulation")

        self.grid = grid
        self.cell_size = 0
        self.current_action = None
        self.highlight_rect = None

        self.default_color = 'white'

        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        self.left_frame = ttk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.button_add_robot = ttk.Button(self.left_frame, text="Add Robot", command=self.prepare_add_robot)
        self.button_add_robot.pack(side="top", padx=5, pady=5)

        self.button_add_package = ttk.Button(self.left_frame, text="Add Package", command=self.prepare_add_package)
        self.button_add_package.pack(side="top", padx=5, pady=5)

        self.button_select_goal = ttk.Button(self.left_frame, text="Select Goal", command=self.prepare_add_goal)
        self.button_select_goal.pack(side="top", padx=5, pady=5)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

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
        position = Position(x, y)

        if self.current_action == 'add_robot':
            robot = Robot(id=len(self.grid.robots), position=position)
            self.grid.add_robot(position, robot)

        elif self.current_action == 'add_package':
            package = Package(id=len(self.grid.packages), position=position)
            self.grid.add_package(position, package)

        elif self.current_action == 'add_goal':
            goal = Goal(id=len(self.grid.goals), position=position)
            self.grid.add_goal(position, goal)

        self.current_action = None
        self.root.config(cursor="")
        self.update_canvas()

    def on_mouse_move(self, event):
        x = (event.x - self.padding_x) // self.cell_size
        y = (event.y - self.padding_y) // self.cell_size
        if self.current_action:
            position = Position(x, y)
            highlight_color = self.default_color
            if self.current_action == 'add_robot':
                highlight_color = Robot.color
            elif self.current_action == 'add_package':
                highlight_color = Package.color
            elif self.current_action == 'add_goal':
                highlight_color = Goal.color

            self.highlight_position(position, highlight_color)

    def highlight_position(self, position: 'Position', color: str):

        if self.highlight_rect:
            self.canvas.delete(self.highlight_rect)

        x, y = position.x, position.y
        if self.grid.is_within_limits(position):
            self.highlight_rect = self.canvas.create_rectangle(
                x * self.cell_size + self.padding_x,
                y * self.cell_size + self.padding_y,
                (x + 1) * self.cell_size + self.padding_x,
                (y + 1) * self.cell_size + self.padding_y,
                outline=color,
                width=2
            )

    def update_canvas(self):
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.cell_size = min(width // self.grid.width, height // self.grid.height)

        self.padding_x = (width - self.cell_size * self.grid.width) // 2
        self.padding_y = (height - self.cell_size * self.grid.height) // 2

        for row in self.grid.grid:
            for cell in row:
                x1 = cell.position.x * self.cell_size + self.padding_x
                y1 = cell.position.y * self.cell_size + self.padding_y
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if cell.robot:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=Robot.color, outline="gray")
                    self.canvas.create_text((x1 + x2) // 2,
                                            (y1 + y2) // 2,
                                            text=str(cell.robot.id),
                                            fill=self.default_color)
                elif cell.packages:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=Package.color, outline="gray")
                    self.canvas.create_text((x1 + x2) // 2,
                                            (y1 + y2) // 2,
                                            text=str(len(cell.packages)),
                                            fill=self.default_color)
                elif cell.goal:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=Goal.color, outline="gray")
                    self.canvas.create_text((x1 + x2) // 2,
                                            (y1 + y2) // 2,
                                            text=str(cell.goal.id),
                                            fill=self.default_color)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.default_color, outline="gray")

    def on_resize(self, event):
        self.update_canvas()

    def run(self):
        self.root.mainloop()
