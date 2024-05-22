# connection.py

class Connection:
    def __init__(self, from_cell, to_cell, weight=1):
        self.from_cell = from_cell
        self.to_cell = to_cell
        self.weight = weight

    def __repr__(self):
        return f"Connection(from: {self.from_cell.position}, to: {self.to_cell.position}, weight: {self.weight})"
