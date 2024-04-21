
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
import math

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# If there is at least 1 wall above or below and left or right, cell is in a corner
def is_corner(warehouse, x, y):
    """
    Check if a cell is a corner cell in the warehouse grid.
    
    A cell is considered a corner cell if it satisfies the following conditions:
    - It is not a wall ('#').
    - It has at least one wall adjacent to it in both horizontal and vertical directions.
    
    @param warehouse: a Warehouse object
    @param x: x-coordinate (column index) of the cell
    @param y: y-coordinate (row index) of the cell
    
    @return: True if the cell is a corner cell, False otherwise
    """

    # Check if the cell is not a wall
    if warehouse[y][x] != '#':

        # Check for walls above, below, left, and right of the cell
        up_down_walls = sum(1 for (dx, dy) in [(0, 1), (0, -1)] if warehouse[y + dy][x + dx] == '#')
        left_right_walls = sum(1 for (dx, dy) in [(1, 0), (-1, 0)] if warehouse[y + dy][x + dx] == '#')

        # Check if there is at least one wall adjacent in both horizontal and vertical directions
        return up_down_walls >= 1 and left_right_walls >= 1
    
    else:

        # Cell is a wall, not a corner
        return False

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    ''' 

    # Symbol
    wall_square = '#'
    taboo_square = 'X'
    target_squares = {'.', '!', '*'}

    # Copy the warehouse to avoid modifying the original
    warehouse_copy = str(warehouse.copy())

    remove_list = ['$', '@']
    # remove the things that aren't walls or targets
    for remove in remove_list:
        warehouse_copy = warehouse_copy.replace(remove, ' ')


    # Convert warehouse to a grid (2D list)
    grid = [[char for char in line] for line in warehouse_copy.split('\n')]

    # Apply Rule 1: Mark corner cells as taboo
    for y in range(1, len(grid) - 1):
        in_wall = False
        for x in range(1, len(grid[0]) - 1):
            if not in_wall:
                if grid[y][x] == wall_square:
                    in_wall = True
                elif grid[y][x] == ' ' and is_corner(grid, x, y) and grid[y][x] not in target_squares:
                    grid[y][x] = taboo_square

    # Apply Rule 2: Mark cells between corners along a wall as taboo
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[0]) - 1):
            if grid[y][x] == taboo_square and is_corner(grid, x, y):
                # Fill taboo cells to the right of the corner
                for x2 in range(x + 1, len(grid[0]) - 1):
                    if grid[y][x2] in target_squares or grid[y][x2] == wall_square:
                        break
                    if grid[y][x2] == taboo_square and is_corner(grid, x2, y):
                        for x3 in range(x + 1, x2):
                            grid[y][x3] = taboo_square
                        break
                # Fill taboo cells below the corner
                for y2 in range(y + 1, len(grid) - 1):
                    if grid[y2][x] in target_squares or grid[y2][x] == wall_square:
                        break
                    if grid[y2][x] == taboo_square and is_corner(grid, x, y2):
                        for y3 in range(y + 1, y2):
                            grid[y3][x] = taboo_square
                        break

    # Convert grid back to a string
    taboo_str = '\n'.join([''.join(row) for row in grid])

    # Remove the target_squares
    for target in target_squares:
        taboo_str = taboo_str.replace(target, ' ')

    return taboo_str


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Helper function for calculating distance:
def distance(point1, point2):
    return round(math.sqrt(pow(point2[0] - point1[0], 2) + pow(point2[1] - point1[1], 2)))

# Helper function for determining if a given cell is taboo:
def is_taboo(warehouse, coordinate):
    lines = taboo_cells(warehouse).split('\n')
    return lines[coordinate[1]][coordinate[0]] == 'X'

class SokobanProblem(search.Problem):
    def actions(self, state):
        legal_actions = []

        # Get the coordinates of the cells on each side of the worker
        left_coord = (state.worker[0] - 1, state.worker[1])
        right_coord = (state.worker[0] + 1, state.worker[1])
        up_coord = (state.worker[0], state.worker[1] - 1)
        down_coord = (state.worker[0], state.worker[1] + 1)

        # Check there is no wall blocking left movement
        if left_coord in state.walls:
            legal_actions.append('left')
        # Check there is no wall blocking right movement
        if right_coord in state.walls:
            legal_actions.append('right')
        # Check there is no wall blocking up movement
        if up_coord in state.walls:
            legal_actions.append('up')
        # Check there is no wall blocking down movement
        if down_coord in state.walls:
            legal_actions.append('down')
        return legal_actions
    
    def result(self, state, action):
        assert action in self.actions(state)
        next_state = state.copy()
        left_coord = (state.worker[0] - 1, state.worker[1])
        right_coord = (state.worker[0] + 1, state.worker[1])
        up_coord = (state.worker[0], state.worker[1] - 1)
        down_coord = (state.worker[0], state.worker[1] + 1)
        # Moving left
        if action == 'left':
            if left_coord in state.boxes:
                index = state.boxes.index(left_coord)
                next_state.boxes[index] = (left_coord[0] + 1, left_coord[1])
            next_state.worker = (next_state.worker[0] - 1, next_state.worker[1])
        # Moving right
        if action == 'right':
            if right_coord in state.boxes:
                index = state.boxes.index(right_coord)
                next_state.boxes[index] = (right_coord[0] + 1, right_coord[1])
            next_state.worker = (next_state.worker[0] + 1, next_state.worker[1])
        # Moving up
        if action == 'up':
            if up_coord in state.boxes:
                index = state.boxes.index(up_coord)
                next_state.boxes[index] = (up_coord[0] + 1, up_coord[1])
            next_state.worker = (next_state.worker[0], next_state.worker[1] - 1)
        # Moving down
        if action == 'down':
            if down_coord in state.boxes:
                index = state.boxes.index(down_coord)
                next_state.boxes[index] = (down_coord[0] + 1, down_coord[1])
            next_state.worker = (next_state.worker[0], next_state.worker[1] + 1)
        return next_state
    
    def h(self, node):
        '''
        Heuristic for goal state of the form range(k,-1,1) where k is a positive integer. 
        h(n) = 1 + the sum of the weights of the boxes not at a target + an additional factor based on whether 
        or not a box is in a taboo cell
        '''
        distance_factor = sum([distance(target, box) * weight for target, box, weight in zip(node.state.targets, node.state.boxes, node.state.weights)])
        taboo_factor = float('Inf') if (len(list(filter(lambda x: is_taboo(node.state.warehouse, x), node.state.boxes))) != 0) else 0
        return 1 + distance_factor + taboo_factor
    
    def print_solution(self, goal_node):
        path = goal_node.path()
        print("Solution takes {0} steps from the initial state\n".format(len(path) - 1))
        print(path[0].state)
        print("to the goal state\n")
        print(path[-1].state)
        print("Below is the sequence of moves\n")
        for node in path:
            self.print_node(node)

    def print_node(self, node):
        if node.action:
            print("Move " + node.action)
        print(node.state)

class SokobanState:
    def __init__(self, boxes, targets, walls, weights, worker, warehouse):
        self.boxes = boxes
        self.targets = targets
        self.walls = walls
        self.weights = weights
        self.worker = worker
        self.warehouse = warehouse
    
    def __str__(self):
        X,Y = zip(*self.walls)
        x_size, y_size = 1+max(X), 1+max(Y)
        
        vis = [[" "] * x_size for y in range(y_size)]
        for (x,y) in self.walls:
            vis[y][x] = "#"
        for (x,y) in self.targets:
            vis[y][x] = "."
        if vis[self.worker[1]][self.worker[0]] == ".":
            vis[self.worker[1]][self.worker[0]] = "!"
        else:
            vis[self.worker[1]][self.worker[0]] = "@"
        for (x,y) in self.boxes:
            if vis[y][x] == ".":
                vis[y][x] = "*"
            else:
                vis[y][x] = "$"
        return "\n".join(["".join(line) for line in vis])
    
    def __lt__(self, state):
        return str(self) < str(state)

    def copy(self):
        clone = SokobanState(self.boxes, self.targets, self.walls, self.weights, self.worker, self.warehouse)
        return clone

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    # Get Initial State:
    initial_state = SokobanState(warehouse.boxes, warehouse.targets, warehouse.walls, warehouse.weights, warehouse.worker, warehouse)
    # Get goal state:
    goal_str = str(warehouse)
    goal_str = goal_str.replace('$', ' ')
    goal_str = goal_str.replace('.', '*')
    goal_warehouse = sokoban.Warehouse()
    goal_warehouse.from_string(goal_str)
    goal_state = SokobanState(goal_warehouse.boxes, goal_warehouse.targets, goal_warehouse.walls, goal_warehouse.walls, goal_warehouse.worker, goal_warehouse)
    # Create problem
    problem = SokobanProblem(initial_state, goal=goal_state)
    # Find solution node via A* graph search
    solution_node = search.astar_graph_search(problem)
    problem.print_solution(solution_node)
    return ([], -1)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

