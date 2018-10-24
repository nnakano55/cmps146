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
    weakest_planet = min(state.neutral_planets(), key=lambda p: p.num_ships, default=None)

    if not strongest_planet or not weakest_planet:
        # No legal source or destination
        return False
    else:
        # (4) Send half the ships from my strongest planet to the weakest enemy planet.
        return issue_order(state, strongest_planet.ID, weakest_planet.ID, strongest_planet.num_ships / 2)


#maybe try to account for distance to see the best planet to look at between two planet
def planet_distance(src, dst):
    return int(ceil(sqrt((src.x - dst.x)**2 + (src.y-dst.y)**2)))


def spread_to_weakest_and_closest_planet(state):

    
    close_and_weak = None
    close_and_weak_dst = float("inf")

    #check how many planets you own first to ensure survival
    if len(state.my_planets()) >= 1:
        strongest_planet = max(state.my_planets(), key=lambda p: p.num_ships, default=None)
    else:
        return False


    #now check planets that are not mine
    for planets in state.not_my_planets():
        # Noriaki comment:
        # needs to actually spread, use fleet and check if fleet have already been sent
        
        """
        psedocode(something like this?):
        for some_sort_of_loop_to_keep_looping_weakest & closest in order:
            count = 0
            for fleet in state.my_fleets():
                if strongest_planet.ID == fleet.source_planet.ID and close_and_weak.ID == fleet.destination_planet.ID:
                    count++
            if counter == 0:
                return issue_order(state, strongest_planet.ID, close_and_weak.ID, close_and_weak.num_ships * 2)
        
        """

        #get a combined value that will determine if this planet is weak and has a small fleet
        dst = planet_distance(strongest_planet, planets) + planets.num_ships

        if dst < close_and_weak_dst:
            close_and_weak_dst = dst
            close_and_weak = planets

        #now that you know the closest and weakest planet we need to see what to do with it
        if close_and_weak.num_ships * 2< strongest_planet.num_ships:
            return issue_order(state, strongest_planet.ID, close_and_weak.ID, close_and_weak.num_ships * 2)














