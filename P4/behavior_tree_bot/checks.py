#useless
def if_neutral_planet_available(state):
    return any(state.neutral_planets())


#get a reverse check of no neutral palnets available
def no_neutral_planet_available(state):
    return len(state.neutral_planets()) == 0

#useless
def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())


#too lazy to change the name, optimized this to check if I have seven planets before attacking else spread
def have_five_planets(state):
    return len(state.my_planets()) >= 7


#this is to check if there is only one planet on each side so start of game
def starting_position_close(state):
    if len(state.enemy_planets()) == 1 and len(state.my_planets()) == 1:
        return True

    return False