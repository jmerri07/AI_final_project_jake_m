# COMP30024 Artificial Intelligence, Semester 1 2025
# Project Part B: Game Playing Agent

from referee.game import PlayerColor, Coord, Direction, \
    Action, MoveAction, GrowAction, board

## Class definitions
class node:
    def __init__(self, a_star_cost, coord: Coord, par_node: 'node'):
        self.a_star_cost = a_star_cost
        self.children = []
        self.coord = coord
        self.par_node = par_node

    def add_leaf(self, leaf):
        self.children.append(leaf)

class board_node:
    def __init__(self, alpha: float, beta: float, board: list[list[str]], 
                 action: Action, parent_node: 'board_node'):
        self.alpha = alpha
        self.beta = beta
        self.board = board
        self.action = action
        self.parent_node = parent_node

    def add_leaf(self, leaf):
        self.children.append(leaf)


## Constants
# Cell state constants
EMPTY = '.' # Cell is empty
LILY_PAD = '*' # Cell has a lily pad
RED_FROG = 'R' # Cell has a red frog
BLUE_FROG = 'B' # Cell has a blue frog

# Numerical constants
BOARD_DIM = 8 # Board dimensions
MOVE_DISTANCE = 1 # Distance of a move without jumps
INIT_I = 0 # Initial index

# Minimax constants
RED_CUT_OFF = 7
RED_START_B = 3
RED_GROWTH_FAC = (1/4)
RED_LATE = 5
BLUE_CUT_OFF = 7
BLUE_START_B = 3
BLUE_GROWTH_FAC = (1/4)
BLUE_LATE = 2


class Agent:
    """
    This class is the "entry point" for your agent, providing an interface to
    respond to various Freckers game events.
    """

    def __init__(self, color: PlayerColor, **referee: dict):
        """
        This constructor method runs when the referee instantiates the agent.
        Any setup and/or precomputation should be done here.
        """
        self._color = color
        if self._color == PlayerColor.RED:
            self._cut_off = RED_CUT_OFF
        else:
            self._cut_off = BLUE_CUT_OFF
        
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as RED")
                self._turn_count = 1
            case PlayerColor.BLUE:
                print("Testing: I am playing as BLUE")
                self._turn_count = 2
        self._board = self.initialise_board()

    def initialise_board(self) -> list[list[str]]:
        board = [[EMPTY for j in range(BOARD_DIM)]
                         for i in range(BOARD_DIM)]
        
        i = INIT_I
        for j in range(BOARD_DIM):
            if j == INIT_I or j == BOARD_DIM-1:
                board[i][j] = LILY_PAD
            else:
                board[i][j] = RED_FROG
                board[i+1][j] = LILY_PAD

        i = BOARD_DIM - 1
        for j in range(BOARD_DIM):
            if j == INIT_I or j == BOARD_DIM-1:
                board[i][j] = LILY_PAD
            else:
                board[i][j] = BLUE_FROG
                board[i-1][j] = LILY_PAD

        return board
    
    def action(self, **referee: dict) -> Action:
        """
        This method is called by the referee each time it is the agent's turn
        to take an action. It must always return an action object. 
        """

        self._nodes_visited = 0
        self._prunes = 0
        if self._turn_count < 17:
            if self._color == PlayerColor.RED:
                action = self.grid_opening(self._turn_count)
            if self._color == PlayerColor.BLUE:
                action = self.pedastal_opening(self._turn_count)
        else: 
            cut_off = self._cut_off
            action = self.minimax(self._board, cut_off)

        self._turn_count = self._turn_count + 2

        return action
        
    def grid_opening(self, turn_num: int) -> Action:
        if turn_num == 1:
            return MoveAction(Coord(0,5), Direction.Down)
        if turn_num == 2:
            return MoveAction(Coord(7,5), Direction.Up)
        if turn_num == 3:
            return MoveAction(Coord(0,2), Direction.Down)
        if turn_num == 4:
            return MoveAction(Coord(7,2), Direction.Up)
        if turn_num == 5:
            return GrowAction()
        if turn_num == 6:
            return GrowAction()
        if turn_num == 7:
            return MoveAction(Coord(0,6), Direction.DownLeft)
        if turn_num == 8:
            return MoveAction(Coord(7,6), Direction.UpLeft)
        if turn_num == 9:
            return MoveAction(Coord(0,1), Direction.DownRight)
        if turn_num == 10:
            return MoveAction(Coord(7,1), Direction.UpRight)
        if turn_num == 11:
            return MoveAction(Coord(1,5), Direction.Left)
        if turn_num == 12:
            return MoveAction(Coord(6,5), Direction.Left)
        if turn_num == 13:
            return MoveAction(Coord(1,2), Direction.Right)
        if turn_num == 14:
            return MoveAction(Coord(6,2), Direction.Right)
        else:
            return GrowAction()
        
    def pedastal_opening(self, turn_num: int) -> Action:
        if turn_num == 1:
            return MoveAction(Coord(0,5), Direction.Down)
        if turn_num == 2:
            return MoveAction(Coord(7,5), Direction.Up)
        if turn_num == 3:
            return MoveAction(Coord(0,2), Direction.Down)
        if turn_num == 4:
            return MoveAction(Coord(7,2), Direction.Up)
        if turn_num == 5:
            return GrowAction()
        if turn_num == 6:
            return GrowAction()
        if turn_num == 7:
            return MoveAction(Coord(0,3), Direction.Down)
        if turn_num == 8:
            return MoveAction(Coord(7,3), Direction.Up)
        if turn_num == 9:
            return MoveAction(Coord(0,4), Direction.Down)
        if turn_num == 10:
            return MoveAction(Coord(7,4), Direction.Up)
        if turn_num == 11:
            return MoveAction(Coord(0,1), Direction.DownRight)
        if turn_num == 12:
            return MoveAction(Coord(7,1), Direction.UpRight)
        if turn_num == 13:
            return MoveAction(Coord(0,6), Direction.DownLeft)
        if turn_num == 14:
            return MoveAction(Coord(7,6), Direction.UpLeft)
        else:
            return GrowAction()
        
    def xtend_opening(self, turn_num: int) -> Action:
        if turn_num == 1:
            return MoveAction(Coord(0,3), Direction.Down)
        if turn_num == 2:
            return MoveAction(Coord(7,3), Direction.Up)
        if turn_num == 3:
            return MoveAction(Coord(0,4), Direction.Down)
        if turn_num == 4:
            return MoveAction(Coord(7,4), Direction.Up)
        if turn_num == 5:
            return GrowAction()
        if turn_num == 6:
            return GrowAction()
        if turn_num == 7:
            return MoveAction(Coord(0,1), 
                              (Direction.Right, Direction.DownRight))
        if turn_num == 8:
            return MoveAction(Coord(7,1), (Direction.Right, Direction.UpRight))
        if turn_num == 9:
            return MoveAction(Coord(0,6), (Direction.Left, Direction.DownLeft))
        if turn_num == 10:
            return MoveAction(Coord(7,6), (Direction.Left, Direction.UpLeft))
        if turn_num == 11:
            return GrowAction()
        if turn_num == 12:
            return GrowAction()
        if turn_num == 13:
            return MoveAction(Coord(1,3), Direction.DownLeft)
        if turn_num == 14:
            return MoveAction(Coord(6,3), Direction.UpLeft)
        else:
            return GrowAction()
        
    def bottoms_out_opening(self, turn_num: int) -> Action:
        if turn_num == 1:
            return MoveAction(Coord(0,5), Direction.Down)
        if turn_num == 2:
            return MoveAction(Coord(7,5), Direction.Up)
        if turn_num == 3:
            return MoveAction(Coord(0,2), Direction.Down)
        if turn_num == 4:
            return MoveAction(Coord(7,2), Direction.Up)
        if turn_num == 5:
            return GrowAction()
        if turn_num == 6:
            return GrowAction()
        if turn_num == 7:
            return MoveAction(Coord(0,6), Direction.DownLeft)
        if turn_num == 8:
            return MoveAction(Coord(7,6), Direction.UpLeft)
        if turn_num == 9:
            return MoveAction(Coord(0,1), Direction.DownRight)
        if turn_num == 10:
            return MoveAction(Coord(7,1), Direction.UpRight)
        if turn_num == 11:
            return MoveAction(Coord(0,3), Direction.DownLeft)
        if turn_num == 12:
            return MoveAction(Coord(7,3), Direction.UpLeft)
        if turn_num == 13:
            return MoveAction(Coord(0,4), Direction.DownRight)
        if turn_num == 14:
            return MoveAction(Coord(7,4), Direction.UpRight)
        else:
            return GrowAction()

    def minimax(self, board: list[list[str]], cut_off: int) -> Action:
        self._nodes_visited += 1
        
        #create new node
        root = board_node(float('-inf'), float('inf'), board, GrowAction(), 
                          None)
        top_value = float('-inf')
        top_action = GrowAction()

        #color for generate possible boards
        if self._color == PlayerColor.RED:
            start_b = RED_START_B #progressive widening parameter
            b_grows_by = RED_GROWTH_FAC #progressive widening pararameter
            next_color = PlayerColor.BLUE
        else:
            start_b = BLUE_START_B
            b_grows_by = BLUE_GROWTH_FAC #progressive widening pararameter
            next_color = PlayerColor.RED #progressive widening pararameter

        #generates all possible actions for frogs that have not passed the late 
        #game threshold. If they are within the last three rows, they cannot be 
        #considered by the algorithm
        new_actions = []
        poss_boards_actions = self.generate_possible_boards(board, self._color)
        for pair in poss_boards_actions:
            if isinstance(pair[1], MoveAction):
                if self._color == PlayerColor.RED and \
                pair[1].coord.r >= RED_LATE:
                    continue
                if self._color == PlayerColor.BLUE and \
                    pair[1].coord.r <= BLUE_LATE:
                    continue
            new_actions.append(pair)
        
        #If we are in the late game, do not consider movement of frogs that are 
        #already finshed more of a safe guard, not completely necessary
        new_ordered_actions = []
        late_game = False
        if self.late_game(board, self._color):
            late_game = True
            ordered_actions = sorted(poss_boards_actions, 
                    key=lambda pba: self.evaluate_board(pba[0]), reverse=True)
            for pair in ordered_actions:
                if isinstance(pair[1], MoveAction):
                    if self._color == PlayerColor.RED and pair[1].coord.r < 7:
                        new_ordered_actions.append(pair)
                    if self._color == PlayerColor.BLUE and pair[1].coord.r > 0:
                        new_ordered_actions.append(pair)
                else: 
                    new_ordered_actions.append(pair)

            new_cut_off = 3
            width = len(new_ordered_actions)
            ordered_actions = new_ordered_actions
        else: #if it is not the late game, sort the actions using evaluate_board 
            ordered_actions = sorted(new_actions, 
                    key=lambda pba: self.evaluate_board(pba[0]), reverse=True)
            width = self.width_calc(cut_off, len(ordered_actions), start_b, 
                                    b_grows_by) #progressive widening
            new_cut_off = cut_off #keeps cut-off fed into function

        for board, action in ordered_actions[:width]:
            kid = board_node(float('-inf'), float('inf'), board, action, root)
            value = self.min(kid, new_cut_off, next_color) #enter into min/max
            if value > top_value:
                top_value = value
                top_action = action
        
        if late_game:
            return ordered_actions[0][1] #in the late game, we don't use minimax
        else:
            return top_action #return best option
    
    def generate_possible_boards(self, board: list[list[str]], 
                                 color: PlayerColor) -> \
    list[tuple[list[list[str]], Action]]:
        possible_results = []

        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if (color == PlayerColor.RED and board[i][j] == RED_FROG) or \
                (color == PlayerColor.BLUE and board[i][j] == BLUE_FROG):
                    possible_paths = self.find_possible_paths(board, color, 
                                                              Coord(i, j))
                    
                    # Convert paths to 'MoveAction's
                    possible_actions = []
                    for path in possible_paths:
                        possible_actions.append(self.convert_to_moveactions(
                            color, path))

                    for move, action in zip(possible_paths, possible_actions):
                        current_board = self.generate_board(board, color, 
                                                        Coord(i, j), move[-1])
                        if all(current_board != existing_board 
                               for existing_board, _ in possible_results):
                            possible_results.append((current_board, action))

        # Add grow action
        if color == PlayerColor.RED:
            col_str = "Red"
        else:
            col_str = "Blue"
        new_board = [row[:] for row in board]
        grow_action = self.grow(col_str, new_board)
        possible_results.append((grow_action, GrowAction()))

        return possible_results
    
    def find_possible_paths(self, board: list[list[str]], color: PlayerColor, 
                            frog_coord: Coord) -> list[list[Coord]]:
        possible_paths = []

        # Normal moves
        if color == PlayerColor.RED:
            directions = [
                (1, 0),    # down
                (1, -1),   # down-left
                (1, 1),    # down-right
                (0, -1),   # left
                (0, 1),    # right
            ]
        else:
            directions = [
                (-1, 0),    # up
                (-1, -1),   # up-left
                (-1, 1),    # up-right
                (0, -1),    # left
                (0, 1),     # right
            ]
        
        for dr, dc in directions:
            i = frog_coord.r + dr
            j = frog_coord.c + dc
            if 0 <= i < BOARD_DIM and 0 <= j < BOARD_DIM and \
            board[i][j] == LILY_PAD:
                possible_paths.append([frog_coord, Coord(i, j)])

        # Jump moves
        jump_paths = self.find_jump_paths(board, color, frog_coord, 
                                          [frog_coord], set())
        possible_paths.extend(jump_paths)
        
        return possible_paths

    def find_jump_paths(self, board: list[list[str]], color: PlayerColor, 
                        current: Coord, path: list[Coord], visited: set) -> \
    list[list[Coord]]:
        jump_paths = []

        if color == PlayerColor.RED:
            directions = [
                (2, 0),    # down
                (2, -2),   # down-left
                (2, 2),    # down-right
                (0, -2),   # left
                (0, 2),    # right
            ]
        else:
            directions = [
                (-2, 0),    # up
                (-2, -2),   # up-left
                (-2, 2),    # up-right
                (0, -2),    # left
                (0, 2),     # right
            ]

        for dr, dc in directions:
            over_r = current.r + dr//2 # r-coordinate of frog that's jumped over
            over_c = current.c + dc//2 # c-coordinate of frog that's jumped over
            dest_r = current.r + dr
            dest_c = current.c + dc

            if not (0 <= over_r < BOARD_DIM and 0 <= over_c < BOARD_DIM):
                # Frog that's jumped over has invalid coordinates
                continue
            if not (0 <= dest_r < BOARD_DIM and 0 <= dest_c < BOARD_DIM):
                # Destination has invalid coordinates
                continue
            if board[over_r][over_c] not in (RED_FROG, BLUE_FROG):
                # 'Coord' that's jumped over does not contain a frog
                continue
            if board[dest_r][dest_c] != LILY_PAD:
                # Destination 'Coord' does not contain a lily pad
                continue
            
            dest = Coord(dest_r, dest_c)
            if dest in path:
                # Destination 'Coord' already in 'path'
                continue
            
            # Perform jump
            new_board = [row[:] for row in board]
            new_board[current.r][current.c] = EMPTY
            if color == PlayerColor.RED:
                new_board[dest.r][dest.c] = RED_FROG
            else:
                new_board[dest.r][dest.c] = BLUE_FROG
            new_path = path + [dest]
            if new_path not in jump_paths:
                jump_paths.append(new_path)
            jump_paths.extend(self.find_jump_paths(new_board, color, dest, 
                                                   new_path, 
                                                   visited | {current}))

        return jump_paths
    
    def convert_to_moveactions(self, color: PlayerColor, path: list[Coord]) -> \
    list[MoveAction]:
        current_action = []
        start_coord = path[0]
        for i in range(len(path)-1):
            curr_coord = path[i]
            next_coord = path[i+1]
            if curr_coord.r == next_coord.r:  # left or right
                if curr_coord.c < next_coord.c:
                    current_action.append(Direction.Right)
                else:
                    current_action.append(Direction.Left)
            elif color == PlayerColor.RED:  # down, down-left, or down-right
                if curr_coord.c == next_coord.c:
                    current_action.append(Direction.Down)
                elif curr_coord.c < next_coord.c:
                    current_action.append(Direction.DownRight)
                else:
                    current_action.append(Direction.DownLeft)
            else: # up, up-left, or up-right
                if curr_coord.c == next_coord.c:
                    current_action.append(Direction.Up)
                elif curr_coord.c < next_coord.c:
                    current_action.append(Direction.UpRight)
                else:
                    current_action.append(Direction.UpLeft)
        
        return MoveAction(start_coord, current_action)
    
    def generate_board(self, board: list[list[str]], color: PlayerColor,
        frog_coord: Coord, move: Coord) -> list[list[str]]:
        new_board = [row[:] for row in board]
        new_board[frog_coord.r][frog_coord.c] = EMPTY
        if color == PlayerColor.RED:
            new_board[move.r][move.c] = RED_FROG
        else:
            new_board[move.r][move.c] = BLUE_FROG
        
        return new_board
    
    def grow(self, color: str, board: list[list[str]]) -> list[list[str]]:
        if color == "Red":
            letter = 'R'
        else:
            letter = 'B'
        i = 0
        j = 0
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if (board[i][j] == letter):
                    if ((i + 1) < 8) and ((j + 1) < 8):
                        if board[i + 1][j + 1] == EMPTY:
                            board[i + 1][j + 1] = LILY_PAD
                    if (i - 1) >= 0 and (j - 1) >= 0:
                        if board[i - 1][j - 1] == EMPTY:
                            board[i - 1][j - 1] = LILY_PAD
                    if (i + 1) < 8 and (j - 1) >= 0:
                        if board[i + 1][j - 1] == EMPTY:
                            board[i + 1][j - 1] = LILY_PAD
                    if (i - 1) >= 0 and (j + 1) < 8:
                        if board[i - 1][j + 1] == EMPTY:
                            board[i - 1][j + 1] = LILY_PAD
                    if (i + 1) < 8:
                        if board[i + 1][j] == EMPTY:
                            board[i + 1][j] = LILY_PAD
                    if (i - 1) >= 0:
                        if board[i - 1][j] == EMPTY:
                            board[i - 1][j] = LILY_PAD
                    if (j + 1) < 8:
                        if board[i][j + 1] == EMPTY:
                            board[i][j + 1] = LILY_PAD
                    if (j - 1) >= 0:
                        if board[i][j - 1] == EMPTY:
                            board[i][j - 1] = LILY_PAD
        
        return board
    
    def late_game(self, board: list[list[str]], color: PlayerColor) -> bool:
        num_frogs = 0
        if color == PlayerColor.RED:
            for i in range(RED_LATE, BOARD_DIM):
                for j in range(BOARD_DIM):
                    if board[i][j] == RED_FROG:
                        num_frogs += 1
        else:
            for i in range(BLUE_LATE + 1):
                for j in range(BOARD_DIM):
                    if board[i][j] == BLUE_FROG:
                        num_frogs += 1
        
        if num_frogs == 6:
            return True
        else:
            return False
    
    def width_calc(self, cut_off: int, num_poss_act: int, start_b: int, 
                   b_grows_by: float) -> int:
        depth = self._cut_off - cut_off
        return min(num_poss_act, int(start_b + b_grows_by * depth))
    
    def min(self, curr_node: board_node, cut_off: int, color: PlayerColor) -> \
    int:
        self._nodes_visited += 1
        cut_off -= 1 #descending one level

        if self.terminal_test(curr_node.board) or cut_off == 0 or \
        self._turn_count == 150:
            return self.evaluate_board(curr_node.board)
        
        #generate possible moves in the form of possible boards
        poss_boards_actions = self.generate_possible_boards(curr_node.board, 
                                                            color)
        ordered_actions = sorted(poss_boards_actions, 
                                 key=lambda pba: self.evaluate_board(pba[0]))

        if self._color == PlayerColor.RED:
            start_b = RED_START_B
            b_grows_by = RED_GROWTH_FAC #progressive widening paramenter
            next_color = PlayerColor.BLUE #progressive widening paramenter
        else:
            start_b = BLUE_START_B
            b_grows_by = BLUE_GROWTH_FAC #progressive widening paramenter
            next_color = PlayerColor.RED #progressive widening paramenter
        
        width = self.width_calc(cut_off, len(ordered_actions), start_b, 
                                b_grows_by)
        for board, action in ordered_actions[:width]:
            new_node = board_node(float('-inf'), float('inf'), board, action, 
                                  curr_node)
            curr_node.beta = min(curr_node.beta, 
                                 self.max(new_node, cut_off, next_color))
            if curr_node.beta <= curr_node.parent_node.alpha:
                self._prunes += 1
                break
            
        return curr_node.beta
    
    def terminal_test(self, board: list[list[str]]) -> bool:
        frog_count1 = 0
        frog_count2 = 0
        for j in range(BOARD_DIM):
            if board[0][j] == BLUE_FROG:
                frog_count1 += 1
            if board[7][j] == RED_FROG:
                frog_count2 += 1
        
        if frog_count1 == 6 or frog_count2 == 6:
            return True
        else:
            return False
    
    def evaluate_board(self, board: list[list[str]]) -> int:
        red_cost = 0
        blue_cost = 0
        for i in range(BOARD_DIM):
            for j in range(BOARD_DIM):
                if board[i][j] == RED_FROG:
                    red_cost += self.estimated_total_cost(board, Coord(i, j), 
                                                          PlayerColor.RED)
                elif board[i][j] == BLUE_FROG:
                    blue_cost += self.estimated_total_cost(board, Coord(i, j), 
                                                           PlayerColor.BLUE)
        
        if self._color == PlayerColor.RED:
            total_cost = blue_cost - red_cost
        elif self._color== PlayerColor.BLUE:
            total_cost = red_cost - blue_cost
        
        return total_cost
    
    def estimated_total_cost(self, board: list[list[str]], coord: Coord, 
                             color: PlayerColor) -> int:
        queue = []
        root = node(a_star_cost = 10, coord = coord, par_node = None)
        queue.append(root)
        keep_going = True
        seen = set()

        i = 0
        while keep_going:
            if len(queue) == 0: #if nodes is empty return failure
                keep_going = False
            else: #pop off top of queue but save node
                curr_node = queue[0]
                queue.pop(0)

            #goal test
            if (curr_node.coord.r == 7 and color == PlayerColor.RED) or \
            (curr_node.coord.r == INIT_I and color == PlayerColor.BLUE):
                keep_going = False
                queue.insert(0, curr_node)
            
            #expand_node
            queue = self.expand_node(curr_node, board, queue, seen)
            i += 1

        if len(queue) == 0:
            if color == PlayerColor.RED:
                solution = 7 - coord.r
            else:
                solution = coord.r
        else:
            solution = self.find_path(queue[0], root)
            solution.append(coord)
            solution = solution[::-1]
            solution = self.count_moveactions(solution)
        
        return solution
    
    def expand_node(self, Node: node, precomputed_board: list[list[str]], 
                queue: list[node], seen: set[tuple[int, int]]) -> list[node]:
        """
        Expands current node by finding possible lily pads and adding them to
        queue.

        Parameters:
            `Node`: 'node' instance representing current node.
            `precomputed_board`: 2D list representing precomputed board state.
            `queue`: List representing queue.
            `seen`: Set representing coordinates already seen.

        Returns:
            Updated queue as list.
        """

        if (Node.coord.r, Node.coord.c) in seen:
            return queue
        
        #Add to seen coord set
        seen.add((Node.coord.r, Node.coord.c))

        #expand tree
        options = self.find_possible_lilypads(precomputed_board, Node.coord)

        for i in range(len(options)):
            new_coords = (options[i].r, options[i].c)
            if new_coords not in seen:
                new_leaf = node(1 + self.compute_heur(options[i], 
                                                      precomputed_board), 
                                options[i], Node)
                Node.add_leaf(new_leaf)
                queue.append(new_leaf)
        
        #add to queue based on a_star cost
        queue = sorted(queue, key=lambda x: x.a_star_cost, reverse=False)
        
        return queue
    
    def find_possible_lilypads(self, precomputed_board: list[list[str]], 
                           red_frog_coord: Coord) -> list[Coord]:
        """
        Finds lily pad coordinates that red frog can move to in current turn.

        Parameters:
            `precomputed_board`: 2D list representing precomputed board state.
            `red_frog_coord`: `Coord` instance representing coordinates of red 
            frog.
        
        Returns:
            Possible lily pad coordinates as list of `Coord` instances.
        """

        possible_lilypads = []
        for i in range(red_frog_coord.r, red_frog_coord.r+MOVE_DISTANCE+1):
            if i not in range(BOARD_DIM):
                continue
            for j in range(red_frog_coord.c-MOVE_DISTANCE, 
                        red_frog_coord.c+MOVE_DISTANCE+1):
                if j not in range(BOARD_DIM):
                    continue
                if (i, j) == (red_frog_coord.r, red_frog_coord.c):
                    continue
                if precomputed_board[i][j] == LILY_PAD:
                    possible_lilypads.append(Coord(i, j))
                elif precomputed_board[i][j] == BLUE_FROG:
                    possible_lilypads.extend(self.attempt_jump(precomputed_board, 
                    red_frog_coord, Coord(i, j)))

        return possible_lilypads
    
    def attempt_jump(self, precomputed_board: list[list[str]], 
                     red_frog_coord: Coord, blue_frog_coord: Coord) -> \
    list[Coord]:
        """
        Red frog attempts to jump over blue frog to find possible lily pad 
        coordinates.

        Parameters:
            `precomputed_board`: 2D list representing precomputed board state.
            `red_frog_coord`: `Coord` instance representing coordinates of red 
            frog.
            `blue_frog_coord`: `Coord` instance representing coordinates of blue 
            frog.
        
        Returns:
            Possible lily pad coordinates as list of `Coord` instances.
        """

        # Calculate destination coordinates
        destination_coord_r = blue_frog_coord.r + (blue_frog_coord.r - 
                                                red_frog_coord.r)
        destination_coord_c = blue_frog_coord.c + (blue_frog_coord.c - 
                                                red_frog_coord.c)

        possible_lilypads = []

        # Check if jump is valid
        if destination_coord_r not in range(BOARD_DIM) or \
        destination_coord_c not in range(BOARD_DIM) or \
        precomputed_board[destination_coord_r][destination_coord_c] != LILY_PAD:
            return possible_lilypads
        
        # Perform jump
        precomputed_board[red_frog_coord.r][red_frog_coord.c] = EMPTY
        red_frog_coord = Coord(destination_coord_r, destination_coord_c)
        possible_lilypads.append(red_frog_coord)
        
        return possible_lilypads
    
    def compute_heur(self, coord: Coord, precomputed_board: list[list[str]]) \
    -> int:
        """
        Computes estimated cost of moving to a coordinate.

        Parameters:
            `coord` : 'Coord' instance representing coordinate cost is estimated
             for
            `precomputed_board`: 2D list representing precomputed board state.
        
        Returns:
            Minimum cost as 'int'
        """

        frogs_left = self.num_frogs(coord, precomputed_board, "left")
        frogs_down =  self.num_frogs(coord, precomputed_board, "down")
        frogs_right = self.num_frogs(coord, precomputed_board, "right")

        pairs_left = self.find_pairs(frogs_left)
        pairs_down = self.find_pairs(frogs_down)
        pairs_right= self.find_pairs(frogs_right)

        left_cost = (7 - coord.r) - (2*pairs_left)
        down_cost = (7 - coord.r) - (2*pairs_down)
        right_cost = (7 - coord.r) - (2*pairs_right)

        cost = []
        cost.append(left_cost)
        cost.append(down_cost)
        cost.append(right_cost)

        return min(cost)
    
    def num_frogs(self, coord: Coord, precomputed_board: list[list[str]], 
              dir: str) -> list[int]:
        """
        Finds number of blue frogs in a given direction from red frog.

        Parameters:
            `coord`: `Coord` instance representing coordinates of red frog.
            `precomputed_board`: 2D list representing precomputed board state.
            `dir`: String representing direction to check for blue frogs.

        Returns:
            Number of blue frogs in each row as list of integers.
        """

        frog_path = []
        if dir == "left":
            i = coord.r + 1 #start by looking at one below and to the left
            if coord.c != 0:
                j = coord.c - 1 #subtraction is left
            else: 
                j = coord.c

            while (i < 8):
                if precomputed_board[i][j] == BLUE_FROG:
                    frog_path.append(1)
                else:
                    frog_path.append(0)
                i += 1
                if j != 0:
                    j -= 1
        if dir == "right":
            i = coord.r + 1 #start by looking at one below and to the left
            if coord.c != 7:
                j = coord.c + 1 #addition is right
            else: 
                j = coord.c

            while (i < 8):
                if precomputed_board[i][j] == BLUE_FROG:
                    frog_path.append(1)
                else:
                    frog_path.append(0)
                if j != 7:
                    j += 1
                i += 1
        if dir == "down":
            i = coord.r + 1
            while (i < 8):
                if precomputed_board[i][coord.c] == BLUE_FROG:
                    frog_path.append(1)
                else:
                    frog_path.append(0)
                i += 1

        return frog_path
    
    def find_pairs(self, path: list[int]) -> int:
        """
        Finds number of pairs of blue frogs then lily pads in given path.

        Parameters:
            `path`: List of integers representing path.

        Returns:
            Number of pairs of blue frogs then lily pads as integer.
        """

        num_skips = 0
        for i in range(len(path) - 1):
            if path[i] == 1 and path[i + 1] == 0:
                num_skips += 1
        
        return num_skips
    
    def find_path(self, Node: node, root: node) -> list[node]:
        """
        Finds path from current node to root node.

        Parameters:
            `Node`: 'node' instance representing current node.
            `root`: 'node' instance representing root node.

        Returns:
            Path from current node to root node as list of `node` instances.
        """

        path = []
        while (Node!=root):
            path.append(Node.coord)
            Node = Node.par_node
        
        return path
    
    def count_moveactions(self, path: list[Coord]) -> int:
        moveactions = []
        current_action = []
        start_coord = path[0]
        for i in range(len(path)-1):
            curr_coord = path[i]
            next_coord = path[i+1]
            if curr_coord.r == next_coord.r:  # left or right
                if curr_coord.c < next_coord.c:
                    current_action.append(Direction.Right)
                else:
                    current_action.append(Direction.Left)
            else:  # down, down-left, or down-right
                if curr_coord.c == next_coord.c:
                    current_action.append(Direction.Down)
                elif curr_coord.c < next_coord.c:
                    current_action.append(Direction.DownRight)
                else:
                    current_action.append(Direction.DownLeft)
            
            # Check if this move is a jump
            is_jump = abs(curr_coord.r-next_coord.r) > 1 or \
            abs(curr_coord.c-next_coord.c) > 1

            # If not a jump, no next move or next move is not part of same move 
            # (not jump), finalise current action
            if not is_jump or (i+1 < len(path)-1 and 
                            abs(next_coord.r-path[i+2].r) <= 1 and 
                            abs(next_coord.c-path[i+2].c) <= 1):
                moveactions.append(MoveAction(start_coord, current_action))
                current_action = []
                start_coord = next_coord

        # Append last move action
        if current_action:
            moveactions.append(MoveAction(start_coord, current_action))
        
        return len(moveactions)
    
    def max(self, curr_node: board_node, cut_off: int, color: PlayerColor) -> \
    int:
        self._nodes_visited += 1
        cut_off -= 1 #descending one level

        if self.terminal_test(curr_node.board) or cut_off == 0 or \
            self._turn_count == 150:
            return self.evaluate_board(curr_node.board)

        #generate possible moves in the form of possible boards
        poss_boards_actions = self.generate_possible_boards(curr_node.board, 
                                                            color)
        ordered_actions = sorted(poss_boards_actions, 
                                 key=lambda pba: self.evaluate_board(pba[0]), 
                                 reverse=True)

        if self._color == PlayerColor.RED:
            start_b = RED_START_B #progressive widening paramenter
            b_grows_by = RED_GROWTH_FAC #progressive widening paramenter
            next_color = PlayerColor.BLUE
        else:
            start_b = BLUE_START_B
            b_grows_by = BLUE_GROWTH_FAC #progressive widening paramenter
            next_color = PlayerColor.RED #progressive widening paramenter

        #basically what this is doing is adjusting current alpha for max nodes 
        #based on beta nodes below and propogating values up for beta nodes 
        #above it
        width = self.width_calc(cut_off, len(ordered_actions), start_b, 
                                b_grows_by)
        for board, action in ordered_actions[:width]:
            new_node = board_node(float('-inf'), float('inf'), board, action, 
                                  curr_node)
            curr_node.alpha = max(curr_node.alpha, self.min(new_node, cut_off, 
                                                            next_color))
            if curr_node.alpha >= curr_node.parent_node.beta:
                self._prunes += 1
                break
            
        return curr_node.alpha
    
    def update(self, color: PlayerColor, action: Action, **referee: dict):
        """
        This method is called by the referee after a player has taken their
        turn. You should use it to update the agent's internal game state. 
        """

        match action:
            case MoveAction(coord, dirs):
                r = coord.r
                c = coord.c
                self._board[r][c] = EMPTY #make leaping from empty

                #normalize to tuple
                if isinstance(dirs, Direction):
                    dirs = (dirs,)
                directions = [str(dir) for dir in dirs]

                #turn directions into number specifying how frog is moving
                r_and_c_move = self.directions_to_num(directions)
                
                #Use these numbers to change board
                self._board = self.change_board(r, c, directions[0], 
                                            self._board, r_and_c_move, color)
            
            case GrowAction():
                if str(color) == "BLUE":
                    self._board = self.grow("Blue", self._board)
                else:
                    self._board = self.grow("Red", self._board)

            case _:
                raise ValueError(f"Unknown action type: {action}")
    
    def directions_to_num(self, directions: list[str]) -> list[int]:
        r_and_c = [0,0]
        for i in range(len(directions)):
            if directions[i] == "[↓]":
                r_and_c[0] += 1
            if directions[i] == "[↙]":
                r_and_c[0] += 1
                r_and_c[1] += -1
            if directions[i] == "[↘]":
                r_and_c[0] += 1
                r_and_c[1] += 1
            if directions[i] == "[↑]":
                r_and_c[0] += -1
            if directions[i] == "[↖]":
                r_and_c[0] += -1
                r_and_c[1] += -1
            if directions[i] == "[↗]":
                r_and_c[0] += -1
                r_and_c[1] += 1
            if directions[i] == "[→]":
                r_and_c[1] += 1
            if directions[i] == "[←]":
                r_and_c[1] += -1
        
        return r_and_c
    
    def change_board(self, r: int, c: int, direction: str, 
                     board: list[list[str]], move: list[int], 
                     color: PlayerColor)  -> list[list[str]]:
        #if we have multiple directions we're hopping so multiply by 2
        if move[0] > 1 or move[0] < -1 or move[1] > 1 or move[1] < -1:
            if color == PlayerColor.RED:
                board[r + move[0]*2][c + move[1]*2] = 'R'
            elif color == PlayerColor.BLUE:
                board[r + move[0]*2][c + move[1]*2] = 'B'
        elif self.check_frog(r, c, direction, board):
            if color == PlayerColor.RED:
                board[r + move[0]*2][c + move[1]*2] = 'R'
            elif color == PlayerColor.BLUE:
                board[r + move[0]*2][c + move[1]*2] = 'B'
        else:
            if color == PlayerColor.RED:
                board[r + move[0]][c + move[1]] = 'R'
            elif color == PlayerColor.BLUE:
                board[r + move[0]][c + move[1]] = 'B'
        
        return board

    def check_frog(self, r: int, c: int, direction: str, 
                   board: list[list[str]]) -> bool:
        if direction == "[↓]":
            if board[r + 1][c] == 'B' or board[r + 1][c] == 'R':
                return True
        if direction == "[↙]":
            if board[r + 1][c - 1] == 'B' or board[r + 1][c - 1] == 'R':
                return True
        if direction == "[↘]":
            if board[r + 1][c + 1] == 'B' or board[r + 1][c + 1] == 'R':
                return True
        if direction == "[↑]":
            if board[r - 1][c] == 'B' or board[r - 1][c] == 'R':
                return True
        if direction == "[↖]":
            if board[r - 1][c - 1] == 'B' or board[r - 1][c - 1] == 'R':
                return True
        if direction == "[↗]":
            if board[r - 1][c + 1] == 'B' or board[r - 1][c + 1] == 'R':
                return True
        if direction ==  "[→]":
            if board[r][c + 1] == 'B' or board[r][c + 1] == 'R':
                return True
        if direction == "[←]":
            if board[r][c - 1] == 'B' or board[r][c - 1] == 'R':
                return True
        
        return False

    def print_board(board: list[list[str]]):
        for row in board:
            print(" ".join(row))
        print()
