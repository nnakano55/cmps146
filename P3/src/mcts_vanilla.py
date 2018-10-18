
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_factor = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    ret_node = node                     # End result node. Determined recursively.
    pointer_state = state               # The game state of this node.  
    child_weights = {}                  # Action -> Weight (float chance for corresponding Action)
    
    if board.is_ended(pointer_state):           # Stop if the game has ended at this point.
        return ret_node
    elif len(ret_node.untried_actions) != 0:    # Stop if the current node has untried actions.
        return ret_node
    else:                                       # Else, we do a weighted selection of child nodes.
        # Calculate the weights of every possible child traversal.
        child_weights = calculate_ucb(ret_node, identity)
    
        # Now, based on weights calculated, choose an Action and run traverse_nodes with the chosen action.
        #============================================================================================================
        # TA QUESTION: Do we need weighted RNG choice, or does the UCB function already account for exploration rate?
        #============================================================================================================
        #chosen_action = choices(population=child_weights.keys(), weights=child_weights.values(), k=1)[0]
        chosen_action = None
        chosen_weight = float('-inf')
        for action in child_weights:
            if child_weights[action] > chosen_weight:
                #print("PREV WEIGHT: " + str(chosen_weight))
                chosen_action = action
                chosen_weight = child_weights[action]
                #print("BEST WEIGHT: " + str(chosen_weight))
        chosen_node = ret_node.child_nodes[chosen_action]
        #print("Chosen action: " + str(chosen_action))
        
        # Explore the next chosen node recursively.
        #print("=========== CONTINUE! ===========")
        ret_node = traverse_nodes(chosen_node, board, board.next_state(state, chosen_action), identity)

    return ret_node
    
def calculate_ucb(root_node, identity):
    """ Take the given dictionary of nodes (Action -> Node), and calculate/map weights.
    
    Args:
        root_node:  parent node
        identity:   The bot's identity, either 'red' or 'blue'.
        
    Returns: a Dict of Action -> Float weights
    
    """
    child_nodes = root_node.child_nodes
    child_weights = {}
    # For every child node of this node, gets weights of each.
    for child in child_nodes:     
        # Determine wins based on identity.
        # Wins of Player 1 are stored by default, so if the player is 2, p2_wins = visits - wins
        if identity == 2:
            child_wins = child_nodes[child].visits - child_nodes[child].wins
        else:
            child_wins = child_nodes[child].wins
            
        child_visits = child_nodes[child].visits
        parent_visits = root_node.visits
        ex_factor = explore_factor
        if child_visits == 0 or parent_visits == 0:
            #============================================================================================================
            # TA QUESTION: What do we do if the node has no wins or visits?
            #============================================================================================================
            child_weights[child] = 1.0     # this node is untouched and can be chosen randomly
        else:
            # Action (child) is mapped -> with a Weight (Upper Confidence Bounds equation).
            child_weights[child] = (child_wins / child_visits) + (ex_factor * sqrt(log(parent_visits) / child_visits))
        
    return child_weights

def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    if len(node.untried_actions) == 0:
        #print("Node has no possible action.")
        return None 
    action = choice(node.untried_actions)
    act_list = board.legal_actions(board.next_state(state, action))
    new_node = MCTSNode(parent=node, parent_action = action, action_list = act_list)
    node.child_nodes[action] = new_node
    #print("NEW CHILD NODE: " + str(node.child_nodes[action]))
    node.untried_actions.remove(action)
    return new_node
    # Hint: return new_node

def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    moves = board.legal_actions(state)
    win_game_red = False
    me = board.current_player(state)

    # Define a helper function to calculate the difference between the bot's score and the opponent's.
    # This is the outcome of whether or not player 1 / X / red will win.
    def outcome(owned_boxes, game_points):
        if game_points is not None:
            # Try to normalize it up?  Not so sure about this code anyhow.
            red_score = game_points[1]*9
            blue_score = game_points[2]*9
        else:
            red_score = len([v for v in owned_boxes.values() if v == 1])
            blue_score = len([v for v in owned_boxes.values() if v == 2])
        return red_score - blue_score 
        
    # Randomly choose a move from moves to proceed with.
    move = choice(moves)    # ERROR: May throw IndexError from not being able to choose from an empty sequence
    total_score = 0.0
    rollout_state = board.next_state(state, move)

    # Play to the end randomly, without heuristics.
    while True:
        if board.is_ended(rollout_state):
            break
        rollout_move = choice(board.legal_actions(rollout_state))
        rollout_state = board.next_state(rollout_state, rollout_move)

    # Get difference between outcomes.
    total_score += outcome(board.owned_boxes(rollout_state),
                           board.points_values(rollout_state))

    # The red player wins if they have a positive difference compared to the opponent
    if total_score > 0:
        win_game_red = True

    return win_game_red


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    while node.parent != None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)   # 1 = X / red, 2 = O / blue
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # my guess of how its suppose to be run, might change later 
        node = traverse_nodes(node, board, state, identity_of_bot)
        node = expand_leaf(node, board, state)
        if node:
            won = rollout(board, board.next_state(state, node.parent_action))
            backpropagate(node, won)
            node = root_node
        else:
            node = root_node
            break   # Game's over, stop.
        
        #print(node.child_nodes)

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    
    # With the completed tree, get the action with the best rate.
    best_action = None
    best_rate = float('-inf')
    highest_visits = 0
    #print(node.child_nodes)
    for child in node.child_nodes:
        if identity_of_bot == 2:
            child_wins = node.child_nodes[child].visits - node.child_nodes[child].wins
        else:
            child_wins = node.child_nodes[child].wins
        child_rate = child_wins / node.child_nodes[child].visits
        child_visits = node.child_nodes[child].visits
        if child_rate > best_rate and child_visits >= highest_visits:
            best_action = child
            best_rate = child_rate
            #print("BEST: " + str(best_rate))
            highest_visits = child_visits
    
    print("MCTS Vanilla bot " + str(identity_of_bot) + " picking %s with expected win rate %f" % (str(best_action), best_rate))
    return best_action
