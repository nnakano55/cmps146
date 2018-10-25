
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_factor = 2.

def traverse_nodes(node, board, state, original_id, pointer_id):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2.

    Returns:        A node from which the next stage of the search can proceed.

    """
    '''ret_node = node                     # End result node. 
    if board.is_ended(state) or len(ret_node.untried_actions) != 0:           # Stop if the game has ended at this point.
        return ret_node
    else: 
        #while len(ret_node.untried_actions) == 0 and len(ret_nodes.child_nodes) != 0:
        ret_children = ret_node.child_nodes
        ret_weights = {}
        for act in ret_node.untried_actions:
            child = ret_children[act]
            if pointer_id == original_id:
                ret_weights[child] = child.wins/child.visits + sqrt(2*log(ret_node.visits)/child.visits)
            else:
                ret_weights[child] = (1 - (child.wins/child.visits)) + sqrt(2*log(ret_node.visits)/child.visits)
        #state = board.next_state(state, ret_node.parent_action)
        best_weight = float('-inf')
        for act in ret_weights:
            if ret_weights[act] > best_weight:
                ret_node = ret_children[act]
    return ret_node'''
    #print("ReCurse")
    ret_node = node                     # End result node. Determined recursively.
    ret_state = state
    ret_id = pointer_id
    pointer_state = state               # The game state of this node.  
    child_weights = {}                  # Action -> Weight (float chance for corresponding Action)
    
    if board.is_ended(state) or len(ret_node.untried_actions) != 0 or len(board.legal_actions(state)) == 0:           # Stop if the game has ended at this point.
        return ret_node, ret_state, ret_id
    else:                                       # Else, we do a weighted selection of child nodes.
        # Calculate the weights of every possible child traversal.
        child_weights = calculate_ucb(ret_node, original_id, pointer_id)
    
        # Now, based on weights calculated, choose an Action and run traverse_nodes with the chosen action.
        chosen_action = None
        chosen_weight = float('-inf')
        for action in child_weights:
            if child_weights[action] >= chosen_weight:
                chosen_action = action
                chosen_weight = child_weights[action]
        chosen_node = ret_node.child_nodes[chosen_action]

        # Explore the next chosen node recursively.
        #print("=========== CONTINUE! ===========")
        ret_node, ret_state, ret_id = traverse_nodes(chosen_node, board, board.next_state(state, chosen_action), original_id, 3 - pointer_id)

    return ret_node, ret_state, ret_id

def calculate_ucb(root_node, original_id, pointer_id):
    """ Take the given dictionary of nodes (Action -> Node), and calculate/map weights.
    
    Args:
        root_node:  parent node
        identity:   The bot's identity, either 'red' or 'blue'.
        
    Returns: a Dict of Action -> Float weights
    
    """
    #print("UCB")
    child_nodes = root_node.child_nodes
    child_weights = {}
    # For every child node of this node, gets weights of each.
    for child in child_nodes:      
        child_wins = child_nodes[child].wins
        child_visits = child_nodes[child].visits
        parent_visits = root_node.visits
        ex_factor = explore_factor
        if pointer_id == original_id:
            child_weights[child] = (child_wins / child_visits) + (ex_factor * sqrt(log(parent_visits) / child_visits))
        else:
            child_weights[child] = (1 - (child_wins / child_visits)) + (ex_factor * sqrt(log(parent_visits) / child_visits))
        
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
        print("Node has no possible action")
        return None 
    action = choice(node.untried_actions)
    act_list = board.legal_actions(board.next_state(state, action))
    new_node = MCTSNode(parent=node, parent_action = action, action_list = act_list)
    node.child_nodes[action] = new_node
    node.untried_actions.remove(action)
    state = board.next_state(state, action)
    return new_node
    # Hint: return new_node


def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    actions = board.legal_actions(state)
    action = choice(actions)
    #""" take middle rollout, the rollout will choose the middle when possible
    for act in actions:
        if act[2] == 1 and act[3] == 1:
            return board.next_state(state,act)
    #"""
    #print("state: ", state)
    """ intercept/finish rollout
    concat = []
    for act in actions:
        concat.append(act[2:4])
    full_action = ((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
    movement = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))

    for move in movement:
        counter = 0
        index = 0
        for i in move:
            if i in concat:
                counter += 1
                index = i
        
        if counter == 1:
            return board.next_state(state, actions[concat.index(move[index])])
    #"""

    return board.next_state(state, action)


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node:   A leaf node.
        won:    An indicator of whether the bot won or lost the game.

    """
    node.visits += 1
    node.wins += won
    pass


def think(board, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        state:  The state of the game.

    Returns:    The action to be taken.

    """
    identity_of_bot = board.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state))
    
    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node

        # Do MCTS - This is all you!
        # my guess of how its suppose to be run, might change later 
        
        # ==== TRAVERSE ==== #
        #print("Traverse")
        original_id = identity_of_bot
        pointer_id = identity_of_bot
        while len(node.untried_actions) == 0 and len(board.legal_actions(sampled_game)) > 0 and not board.is_ended(sampled_game):
            node, sampled_game, pointer_id = traverse_nodes(node, board, sampled_game, original_id, pointer_id)
            #sampled_game = board.next_state(sampled_game, node.parent_action)
                #chosen_action = node.parent_action
                #pointer_id = 3 - pointer_id
            
        # ==== EXPAND ==== #
        #print("Expand")
        if len(node.untried_actions) != 0:
            node = expand_leaf(node, board, sampled_game)
            sampled_game = board.next_state(sampled_game, node.parent_action)
            #if node.parent.parent_action == None:
                #chosen_action = node.parent_action
            #pointer_id = 3 - pointer_id
            
        # ==== ROLLOUT ==== #
        #print("Rollout")
        while not board.is_ended(sampled_game):
            #print("ORIGINAL STATE: " + str(sampled_game))
            sampled_game = rollout(board, sampled_game)
            #print("NEW STATE: " + str(sampled_game))
            #pointer_id = 3 - pointer_id
            
        # ==== BACKPROPGATE === #
        #print("BackProp")
        won = board.win_values(sampled_game)[identity_of_bot]
        while node != None:
            backpropagate(node, won)
            node = node.parent
            #pointer_id = 3 - pointer_id
        #print("Step: " + str(step))

    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    
    # With the completed tree, get the action with the best rate.
    node = root_node
    best_action = None
    best_rate = float('-inf')
    best_wins = 0
    highest_visits = 0
    for child in node.child_nodes:
        r = node.child_nodes[child]
        child_wins = r.wins
        child_visits = r.visits
        #print(str(child) + ": " + str(child_wins) + " / " + str(child_visits))
        #win_rate = child_wins / child_visits
        if best_action == None:
            best_action = child
        if child_wins > best_wins and child_visits >= highest_visits:
            best_action = child
            best_wins = child_wins
            #best_rate = child_wins
            #print("BEST: " + str(best_rate))
            highest_visits = child_visits
    print("MCTS Modified bot " + str(identity_of_bot) + " picking %s with expected win score %f" % (str(best_action), best_wins))
    return best_action
