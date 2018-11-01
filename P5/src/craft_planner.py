import json

from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time

#additional imports 
import heapq

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        if rule.get('Requires'):
            for k, v in rule['Requires'].items():
                #can be if because should be only one anyway 
                if state[k] < (1 if v is True else 0):
                    return False

        if rule.get('Consumes'):
            for k, v in rule['Consumes'].items():
                #print(state[k], ', ', v)
                if state[k] < v:  
                    return False

        return True
    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()
        
        for k, v in rule['Produces'].items():
            next_state[k] += v

        if rule.get('Consumes'):
            for k, v in rule['Consumes'].items():
                next_state[k] -= v

        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for k, v in goal.items():
            if state[k] < v:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.

    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


Tools = [
    "bench",
    "iron_axe",
    "iron_pickaxe",
    "stone_axe",
    "stone_pickaxe",
    "wooden_axe",
    "wooden_pickaxe",
    "furnace"
]

Goals = {}

#"""

def heuristic(state):
    cost = 0
    for k, v in state.items():
        
        if k in Tools and v > 1:
            cost += 100
        elif v > 8 and not Goals.get(k):
            cost += v
        elif Goals.get(k):
            if Goals.get(k) + 16 <= v:
                cost += (v - Goals.get(k))
            elif Goals.get(k) > v:
                cost += (Goals.get(k) - v)

    return cost
"""

def heuristic(state):
    # Implement your heuristic here!
    cost = 0
    for k, v in state.items():
        if v > 9 and not Goals.get(k):
            cost += 5
        if k in Tools and v > 1:
            cost += 10
        if Goals.get(k) and Goals.get(k) >= v:
            cost -= 5
    return cost

#"""

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    total_path_cost = 0
    while time() - start_time < limit:
        if is_goal(state):
            return state
        possible = graph(state)
        queue = []
        heapq.heapify(queue)
        for pos in possible:
            f_value = heuristic(pos[1]) + pos[2]
            heapq.heappush(queue, (f_value, pos[1]))
        pop = heapq.heappop(queue)
        state = pop[1]
        print(pop[0])
        
    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])
    Goals = Crafting['Goal']

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    print('Initial: ', Crafting['Initial'])
    print('Goal: ', Crafting['Goal']) 
    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 5, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan.items():
            print(state, ": ", action)