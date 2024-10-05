# vror/__init__.py

"""
VROR: A package for solving various optimization problems.

Modules:
- CPM: Critical Path Method
- Graphical Method: Linear Programming via Graphical Methods
- Simplex Method: Linear Programming via Simplex Method
- Transportation: Solve Transportation Problems
- Assignment: Solve Assignment Problems
"""

from .cpm import create_graph, add_event, find_critical_path, visualize_graph
from .graphical_method import graphical_method
from .simplex_method import simplex_method
from .transportation_problem  import transportation_problem 
from .assignment_problem  import assignment_problem 
from .augmentations import rotate, flip_horizontal, flip_vertical, adjust_brightness, add_noise, apply_augmentations, process_dataset