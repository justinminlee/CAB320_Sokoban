
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (11198885, 'Minjae', 'Lee'), (10804072, 'Zaichic', 'Turner'), (11225271, 'Chanyoung', 'Kim') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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
    ##         "INSERT YOUR CODE HERE"    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        raise NotImplementedError

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
    
    # Define possible movements in terms of x, y coordinates
    directions = {
    'Left': (-1, 0),
    'Right': (1, 0),
    'Up': (0, -1),
    'Down': (0, 1),
    }
    
    # Initialize worker's starting position
    worker_x, worker_y = warehouse.worker
    
     # Convert box positions to a set for efficient manipulation and checks
    box_locations = set(warehouse.boxes) 

    # Ensure walls and targets are also treated as sets
    walls = set(warehouse.walls)
    targets = set(warehouse.targets)

    # Process each action in the sequence
    for action in action_seq:
        
        # Determine the change in coordinates after the action
        dx, dy = directions[action]
        
        # Calculate new worker position after movement
        new_worker_x, new_worker_y = worker_x + dx, worker_y + dy
        
        # Check if the new worker position hits a wall
        if (new_worker_x, new_worker_y) in walls:
            return "Impossible"
        
        # Check if the new worker position pushes a box
        if (new_worker_x, new_worker_y) in box_locations:
            new_box_x, new_box_y = new_worker_x + dx, new_worker_y + dy
            if (new_box_x, new_box_y) in walls or (new_box_x, new_box_y) in box_locations:
                return "Impossible"
            box_locations.remove((new_worker_x, new_worker_y))
            box_locations.add((new_box_x, new_box_y))
        
        worker_x, worker_y = new_worker_x, new_worker_y

    # Generate the final state of the warehouse after applying all actions
    return create_warehouse_representation(worker_x, worker_y, box_locations, walls, targets)

def create_warehouse_representation(worker_x, worker_y, boxes, walls, targets):
    
    # Calculate the maximum dimensions of the warehouse to size the grid
    max_x = max(x for x, _ in walls.union(boxes, targets, {(worker_x, worker_y)}))
    max_y = max(y for _, y in walls.union(boxes, targets, {(worker_x, worker_y)}))
    
    # Initialize the grid to represent the warehouse state
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Mark walls on the grid
    for x, y in walls:
        grid[y][x] = '#'
    for x, y in targets:
        grid[y][x] = '.' if (x, y) not in boxes else '*'
    for x, y in boxes:
        if (x, y) not in targets:
            grid[y][x] = '$'
            
    # Place the worker, mark as '!' if on target, otherwise '@'
    grid[worker_y][worker_x] = '!' if (worker_x, worker_y) in targets else '@'
    
    # Join the grid lines into a single string to represent the warehouse visually
    return "\n".join("".join(row) for row in grid)

    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

