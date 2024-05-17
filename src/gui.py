import tkinter as tk
from grid_manager import GridManager
from robot import Robot
from package import Package
from src.goal import Goal


class WarehouseGUI:
    """WarehouseGUI class documentation

    This class represents a graphical user interface (GUI) for a warehouse robot simulation. The GUI allows users to interact with the simulation, such as adding robots and packages to the
    * warehouse grid, starting the simulation, and resetting the grid.

    Attributes:
        - root (Tk): The root tkinter window of the GUI.
        - grid_manager (GridManager): The grid manager object that handles the warehouse grid.
        - current_action (str): The current action selected by the user (e.g., 'add_robot', 'add_package').
        - highlight_rect (int): The ID of the highlighting rectangle on the canvas.
        - cell_size (int): The size of each grid cell in pixels.

    Methods:
        - __init__(): Initializes the GUI and grid manager.
        - create_widgets(): Creates and places the widgets in the GUI.
        - prepare_add_robot(): Prepares to add a robot on the next canvas click.
        - prepare_add_package(): Prepares to add a package on the next canvas click.
        - on_canvas_click(event): Handles canvas click events.
        - on_mouse_move(event): Handles mouse movement over the canvas to highlight grid cells.
        - highlight_position(position): Highlights the grid cell at the given position.
        - clear_highlight(): Clears the highlighted grid cell.
        - reset(): Resets the warehouse grid.
        - start(): Starts the simulation.
        - stop(): Stops the simulation.
        - update_simulation(): Updates the simulation by moving robots.
        - update_canvas(): Updates the canvas with the current grid state.
        - on_resize(event): Handles window resize events.
        - run(): Runs the GUI main loop.

    Example Usage:
        gui = WarehouseGUI()
        gui.run()
    """
    def __init__(self):
        """
        Initialize the Warehouse Robot Simulation.

        This method initializes the Tkinter root window, sets the title,
        creates a GridManager object, sets the current action and
        highlight_rect variables to None, and sets the default cell size.
        It also creates widgets and binds the on_resize method to the
        <Configure> event of the root window.

        Parameters:
            None

        Returns:
            None
        """
        self.root = tk.Tk()
        self.root.title("Warehouse Robot Simulation")

        self.grid_manager = GridManager(width=10, height=10)
        self.current_action = None
        self.highlight_rect = None
        self.cell_size = 50  # Default cell size
        self.simulation_running = False

        self.create_widgets()
        self.root.bind("<Configure>", self.on_resize)

    def create_widgets(self):
        """
        The create_widgets method is used to initialize and create the widgets for the GUI.
        :return: None
        """
        self.canvas = tk.Canvas(self.root)
        self.canvas.grid(row=0, column=1, columnspan=3, sticky="nsew", padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # Initialize a frame for buttons
        self.left_frame = tk.Frame(self.root)
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        # Add buttons to the frame
        self.button_add_robot = tk.Button(self.left_frame, text="Add Robot", command=self.prepare_add_robot)
        self.button_add_robot.pack(side="top", padx=5, pady=5)

        self.button_add_package = tk.Button(self.left_frame, text="Add Package", command=self.prepare_add_package)
        self.button_add_package.pack(side="top", padx=5, pady=5)

        self.button_select_goal = tk.Button(self.left_frame, text="Select Goal", command=self.prepare_add_goal)
        self.button_select_goal.pack(side="top", padx=5, pady=5)

        self.button_start = tk.Button(self.left_frame, text="Start", command=self.start_simulation)
        self.button_start.pack(side="top", padx=5, pady=5)

        self.button_pause = tk.Button(self.left_frame, text="Pause", command=self.stop_simulation)
        self.button_pause.pack(side="top", padx=5, pady=5)

        self.button_reset = tk.Button(self.left_frame, text="Reset", command=self.reset)
        self.button_reset.pack(side="top", padx=5, pady=5)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def prepare_add_robot(self):
        """
        Sets the current action as 'add_robot' and changes the cursor to a cross.

        :return: None
        """
        self.current_action = 'add_robot'
        self.root.config(cursor="cross")

    def prepare_add_package(self):
        """
        Sets the current action to 'add_package' and changes the cursor to a cross.

        :return: None
        """
        self.current_action = 'add_package'
        self.root.config(cursor="cross")

    def prepare_add_goal(self):
        """
        Sets the current action to 'add_goal' and changes the cursor to a cross.

        :return: None
        """
        self.current_action = 'add_goal'
        self.root.config(cursor='cross')

    def on_canvas_click(self, event):
        """
        Handle click event on the canvas.

        :param event: The event object representing the click event.
        :type event: tkinter.Event
        :return: None
        """
        x = (event.x - self.padding_x) // self.cell_size
        y = (event.y - self.padding_y) // self.cell_size
        position = (x, y)

        if self.current_action == 'add_robot':
            robot = Robot(id=len(self.grid_manager.robots), position=position)
            self.grid_manager.add_robot(robot)
        elif self.current_action == 'add_package':
            package = Package(position=position)
            self.grid_manager.add_package(package)
        elif self.current_action == 'add_goal':
            goal = Goal(position=position)
            self.grid_manager.add_goal(goal)

        self.current_action = None
        self.root.config(cursor="")
        self.clear_highlight()
        self.update_canvas()

    def on_mouse_move(self, event):
        """
        :param event: The mouse event that triggered the method.
        :return: None

        This method is called when the mouse is moved over the specified area. It calculates the position of the mouse cursor relative to the grid of cells, based on the event coordinates. It
        * then checks if the current action is either "add_robot" or "add_package". If so, it highlights the position on the grid corresponding to the calculated coordinates.
        """
        x = (event.x - self.padding_x) // self.cell_size
        y = (event.y - self.padding_y) // self.cell_size

        action_object_map = {
            'add_robot': self.robot,
            'add_package': self.package,
            'add_goal': self.goal
        }

        if self.current_action == 'add_robot':
            self.highlight_position((x, y), 'blue')
        elif self.current_action == 'add_package':
            self.highlight_position((x, y), 'red')
        elif self.current_action == 'add_goal':
            self.highlight_position((x, y), '')

    def highlight_position(self, position, color):
        """
        Highlight the given position on the canvas.

        :param position: The position to be highlighted. Should be a tuple in the format (x, y).
        :return: None
        """
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
        """
        Clears the highlighting rectangle on the canvas.

        :return: None
        """
        if self.highlight_rect:
            self.canvas.delete(self.highlight_rect)
            self.highlight_rect = None

    def reset(self):
        """
        Reset method to reset the grid manager and update the canvas.

        :return: None
        """
        self.grid_manager.reset()
        self.update_canvas()

    def start_simulation(self):
        """
        Starts the simulation by setting the simulation_running flag to True
        and calling the update_simulation method.

        :return: None
        """
        self.simulation_running = True
        self.update_simulation()

    def stop_simulation(self):
        """
        Stops the simulation by setting the simulation_running flag to False.

        :return: None
        """
        self.simulation_running = False

    def update_simulation(self):
        """
        Updates the simulation by moving robots. This method is called
        periodically as long as the simulation is running.

        :return: None
        """
        if self.simulation_running:
            # Example movement logic: move each robot to the right
            for robot in self.grid_manager.robots:
                robot.move()

            self.update_canvas()
            self.root.after(1000, self.update_simulation)  # Update every 1 second

    def update_canvas(self):
        """
        Update the canvas by redrawing the grid based on the grid manager's state.

        :return: None
        """
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
                if isinstance(self.grid_manager.grid[y][x], Robot):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue")
                elif isinstance(self.grid_manager.grid[y][x], Package):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="green")
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=1, stipple="gray12")

    def on_resize(self, event):
        """
        Handle the resize event.

        :param event: The resize event object.
        :type event: Event
        :return: None
        """
        self.update_canvas()

    def run(self):
        """
        Runs the main loop of the Tkinter application.

        :return: None
        """
        self.root.mainloop()

if __name__ == "__main__":
    app = WarehouseGUI()
    app.run()
