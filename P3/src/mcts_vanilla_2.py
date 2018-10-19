
from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node, board, state, identity):
    """ Traverses the tree until the end criterion are met.

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 'red' or 'blue'.

    Returns:        A node from which the next stage of the search can proceed.

    """
    c_node = node
    while len(c_node.untried_actions) == 0 and len(c_node.child_nodes) != 0:
        c_weights = UTB_calculation(c_node, identity)
        chosen_action = list(c_weights.keys())[0]
        chosen_weight = c_weights[list(c_weights.keys())[0]]
        for action in c_weights:
            if c_weights[action] > chosen_weight:
                chosen_action = action
                chosen_weight = c_weights[action]
        c_node = c_node.child_nodes[chosen_action]
        state = board.next_state(state, chosen_action)

    return c_node
    # Hint: return leaf_node

def UTB_calculation(node, identity):
    c_nodes, c_weights = node.child_nodes, {}
    
    for child in c_nodes:
        c = c_nodes[child]
        c_wins = c.visits - c.wins if identity == c.player else c.wins

        if c.visits == 0 or node.visits == 0:
            c_weights[child] = 1.0
        else:
            c_weights[child] = (c_wins/c.visits) + (explore_faction * sqrt(log(node.visits) / c.visits))

    return c_weights




def expand_leaf(node, board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node.

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:    The added child node.

    """
    if len(node.untried_actions) == 0:
        return None
    
    action = choice(node.untried_actions)
    state = board.next_state(state, action)
    act_list = board.legal_actions(state)
    new_node = MCTSNode(parent=node, parent_action = action, action_list = act_list, player = board.current_player(state))
    node.child_nodes[action] = new_node
    node.untried_actions.remove(action)
    
    return new_node

def rollout(board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board:  The game setup.
        state:  The state of the game.

    """
    me = 1 if board.current_player(state) == 2 else 2
    while not board.is_ended(state):
        actions = board.legal_actions(state)
        state = board.next_state(state, choice(actions))
    return True if board.points_values(state)[me] == 1 else False


def backpropagate(node, won, identity):
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
    identity_of_bot = board.current_player(state)

    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(state), player=identity_of_bot)

    for step in range(num_nodes):
        # Copy the game for sampling a playthrough
        sampled_game = state

        # Start at root
        node = root_node
        # Do MCTS - This is all you!
        node = traverse_nodes(node, board, sampled_game, identity_of_bot)
        sampled_game = update_state(node, board, state)
        node = expand_leaf(node, board, sampled_game)
        sampled_game = update_state(node, board, state)
        if node:
            won = rollout(board, sampled_game)
            backpropagate(node, won, identity_of_bot)
        else:
            break

    # With the completed tree, get the action with the best rate.

    best_action = None
    best_rate = float('-inf')
    highest_visits = 0
    for child in root_node.child_nodes:
        r = root_node.child_nodes[child]
        child_wins = r.visits - r.wins if r.player != identity_of_bot else r.wins
        child_rate = child_wins / root_node.child_nodes[child].visits
        child_visits = root_node.child_nodes[child].visits
        if child_rate > best_rate and child_visits >= highest_visits:
            best_action = child
            best_rate = child_rate
            #print("BEST: " + str(best_rate))
            highest_visits = child_visits
    print("MCTS Vanilla bot " + str(identity_of_bot) + " picking %s with expected win rate %f" % (str(best_action), best_rate))

    return best_action


def update_state(node, board, state):
    temp_node = node
    act_list = []
    while temp_node and temp_node.parent:
        act_list.insert(0,node.parent_action)
        temp_node = temp_node.parent
    for action in act_list:
        state = board.next_state(state, action)
    return state