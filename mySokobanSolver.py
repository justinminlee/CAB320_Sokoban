
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
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class SokobanProblem(search.Problem):
    def actions(self, state):
        legal_actions = []
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
                next_state.boxes.remove(left_coord)
                next_state.boxes.append((left_coord[0] + 1, left_coord[1]))
            next_state.worker = (next_state.worker[0] - 1, next_state.worker[1])
        # Moving right
        if action == 'right':
            if right_coord in state.boxes:
                next_state.boxes.remove(right_coord)
                next_state.boxes.append((right_coord[0] + 1, right_coord[1]))
            next_state.worker = (next_state.worker[0] + 1, next_state.worker[1])
        # Moving up
        if action == 'up':
            if up_coord in state.boxes:
                next_state.boxes.remove(up_coord)
                next_state.boxes.append((up_coord[0] + 1, up_coord[1]))
            next_state.worker = (next_state.worker[0], next_state.worker[1] - 1)
        # Moving down
        if action == 'down':
            if down_coord in state.boxes:
                next_state.boxes.remove(down_coord)
                next_state.boxes.append((down_coord[0] + 1, down_coord[1]))
            next_state.worker = (next_state.worker[0], next_state.worker[1] + 1)
        return next_state
    
    def h(self, node):
        '''
        Heuristic for goal state of the form range(k,-1,1) where k is a positive integer. 
        h(n) = 1 + the sum of the weights of the boxes not at a target
        '''
        return 1 + sum(node.state.weights)
    
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
    def __init__(self, boxes, targets, walls, weights, worker):
        self.boxes = boxes
        self.targets = targets
        self.walls = walls
        self.weights = weights
        self.worker = worker
    
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
        clone = SokobanState(self.boxes, self.targets, self.walls, self.weights, self.worker)
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
    #taboo = taboo_cells(str(warehouse))
    # Get Initial State:
    print(warehouse.walls)
    initial_state = SokobanState(warehouse.boxes, warehouse.targets, warehouse.walls, warehouse.weights, warehouse.worker)
    # Get goal state:
    goal_str = str(warehouse)
    goal_str = goal_str.replace('$', ' ')
    goal_str = goal_str.replace('.', '*')
    goal_warehouse = sokoban.Warehouse()
    goal_warehouse.from_string(goal_str)
    goal_state = SokobanState(goal_warehouse.boxes, goal_warehouse.targets, goal_warehouse.walls, goal_warehouse.walls, goal_warehouse.worker)
    # Create problem
    problem = SokobanProblem(initial_state, goal=goal_state)
    # Find solution node via A* graph search
    solution_node = search.astar_graph_search(problem)
    problem.print_solution(solution_node)
    return ([], -1)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

