import os
import json
import random


def generate_grid(file_name='../maps/default_map.json', width=10, height=10):

    # Check if file exists
    if os.path.exists(file_name):
        raise ValueError(f"File {file_name} already exists")

    grid_data = {
        "width": width,
        "height": height,
        "cells": [],
    }

    # Define positions and connections
    for y in range(height):
        for x in range(width):
            cell = {
                "position": {"x": x, "y": y},
                "connections": [],
                "robot": None,
                "goal": None,
                "maxLoad": 10,
                "packages": [],
            }
            if x > 0:  # Add connection to the left cell
                cell["connections"].append({"toCell": {"x": x - 1, "y": y}, "weight": 1})
            if x < width - 1:  # Add connection to the right cell
                cell["connections"].append({"toCell": {"x": x + 1, "y": y}, "weight": 1})
            if y > 0:  # Add connection to the top cell
                cell["connections"].append({"toCell": {"x": x, "y": y - 1}, "weight": 1})
            if y < height - 1:  # Add connection to the bottom cell
                cell["connections"].append({"toCell": {"x": x, "y": y + 1}, "weight": 1})
            grid_data["cells"].append(cell)

    with open(file_name, 'w') as grid_file:
        json.dump(grid_data, grid_file, indent=4)
