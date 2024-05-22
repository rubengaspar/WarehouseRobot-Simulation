# main.py
from gui import GUI
from src.grid import Grid

if __name__ == "__main__":
    grid = Grid(15, 15)
    app = GUI(grid)
    app.run()
