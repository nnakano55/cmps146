import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import sqrt, ceil


def attack_weakest_enemy_planet(state):
    # (1) If we currently have a fleet in flight, abort plan.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda t: t.num_ships, default=None)

    # (3) Find the weakest enemy planet.
    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_weakest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)

    # (3) Find the weakest neutral planet.
    weakest_planet = max(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)

def spread_to_fastest_neutral_planet(state):
    # (1) If we currently have a fleet in flight, just do nothing.
    if len(state.my_fleets()) >= 1:
        return False

    # (2) Find my strongest planet.
    strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    # (3) Find the weakest neutral planet.
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.growth_rate, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


#these are all the neutral palnets that are not currently being sent to
def sort_neutrals(state):
    n_planets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    n_planets.sort(key=lambda planet: planet.num_ships * (1 + 1 / planet.growth_rate))

    return n_planets

#maybe try to account for distance to see the best planet to look at between two planet
def planet_distance(src, dst):
    return int(ceil(sqrt((src.x - dst.x)**2 + (src.y-dst.y)**2)))



def best_three_planets(state):
    topThree  = []
    choice = 0

    planet =  state.my_planets()
    planet.sort(key=lambda pl: pl.num_ships * (1 + 1 / pl.growth_rate))

    while len(topThree) != 3:
        topThree.append(planet[choice])

    return topThree


def spread_to_weakest_and_closest_planet(state):


    close_and_weak = None
    close_and_weak_dst = float("inf")

    #check how many planets you own first to ensure survival
    if len(state.my_planets()) >= 1:
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False

        # now check planets that are not mine
    for planets in state.not_my_planets():
        # get a combined value that will determine if this planet is weak and has a small fleet
        dst = planet_distance(strongest_planet, planets) + planets.num_ships

        if dst < close_and_weak_dst:
            close_and_weak_dst = dst
            close_and_weak = planets

    #now that you know the closest and weakest planet we need to see what to do with it
    if close_and_weak is not None and close_and_weak.num_ships + 10 < strongest_planet.num_ships and close_and_weak.num_ships < 30:
        issue_order(state, strongest_planet.ID, close_and_weak.ID, strongest_planet.num_ships/2)

    #I want to use my next sequence also so returning False
    return False

#we need to look at growth rate
def defend_planet(state):
    current = None
    current_growth = 0

    #check how many planets you own first to ensure survival
    if len(state.my_planets()) >= 2:
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False

    # now check planets that are not mine
    for planets in state.my_planets():
        # get a combined value that will determine if this planet is weak and has a small fleet

        if planets.growth_rate >= 4 and strongest_planet.growth_rate < planets.growth_rate:
            issue_order(state, strongest_planet.ID, planets.ID, strongest_planet.num_ships / 1.25)

    return True







