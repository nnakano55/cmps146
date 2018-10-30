import sys
sys.path.insert(0, '../')
from planet_wars import issue_order
from math import sqrt, ceil

#not a good function
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

#not a good function
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

#these are all the neutral palnets that are not currently being sent to
def sort_neutrals(state):
    n_planets = [planet for planet in state.neutral_planets() if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    n_planets.sort(key=lambda planet: planet.num_ships * (1 + 1 / planet.growth_rate))

    return n_planets

#maybe try to account for distance to see the best planet to look at between two planet
#I had to make this because the given distance function is iffy
def planet_distance(src, dst):
    return int(ceil(sqrt((src.x - dst.x)**2 + (src.y-dst.y)**2)))


#not even needed, scrpapped this
def best_three_planets(state):
    topThree  = []
    choice = 0

    planet =  state.my_planets()
    planet.sort(key=lambda pl: pl.num_ships * (1 + 1 / pl.growth_rate))

    while len(topThree) != 3:
        topThree.append(planet[choice])

    return topThree


#finds the closes and weakest planet to spread to
#targets best growth rate first
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
        dst = planet_distance(strongest_planet, planets) + planets.num_ships / (1+ planets.growth_rate)

        if dst < close_and_weak_dst:
            close_and_weak_dst = dst
            close_and_weak = planets


    #now that you know the closest and weakest planet we need to see what to do with it
    if close_and_weak is not None and close_and_weak.num_ships + 10 < strongest_planet.num_ships:
        required_ships = close_and_weak.num_ships + \
                         state.distance(strongest_planet.ID, close_and_weak.ID) * close_and_weak.growth_rate + 2
        issue_order(state, strongest_planet.ID, close_and_weak.ID, required_ships)

    return False



#uselses, why defend?
def defend(state):
    pass


#based on the spread_bot attack function
def attack_them(state):
    my_planets = iter(sorted(state.my_planets(), key=lambda p: p.num_ships))

    enemy_planets = [planet for planet in state.enemy_planets()
                      if not any(fleet.destination_planet == planet.ID for fleet in state.my_fleets())]
    enemy_planets.sort(key=lambda p: p.num_ships)

    target_planets = iter(enemy_planets)

    try:
        my_planet = next(my_planets)
        target_planet = next(target_planets)
        while True:
            required_ships = target_planet.num_ships + \
                                 state.distance(my_planet.ID, target_planet.ID) * target_planet.growth_rate + 1

            if my_planet.num_ships > required_ships:
                issue_order(state, my_planet.ID, target_planet.ID, required_ships)
                my_planet = next(my_planets)
                target_planet = next(target_planets)
            else:
                my_planet = next(my_planets)
        return True

    except StopIteration:
        return True


#if passes the start of the game check, goes checks the distance to see if we are close to the enemy planet at the start
#if we are close, we attack the enemy planet because its a prime target
def attack_start(state):
    if len(state.my_planets()) >= 1:

        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False

    weakest_planet = min(state.enemy_planets(), key=lambda t: t.num_ships, default=None)

    if planet_distance(strongest_planet, weakest_planet) < 10:

        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships/2)

    return False