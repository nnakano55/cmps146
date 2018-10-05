"""

Programmers:
    Noriaki Nakano
    Jay Parikh
    
P1:
    This program takes in a maze that is stored into a txt file and 
    tries to solve the maze and draws a path that solves the maze.
    It also saves a map saved with the cost to get from the initial position to
    all other vertices 

Outside Reference: 
    Priority Queue Dijkstra:
        https://www.geeksforgeeks.org/dijkstras-shortest-path-algorithm-using-priority_queue-stl/
    Python Syntax/Features:
        https://www.w3schools.com/python/

"""


from p1_support import load_level, show_level, save_level_costs
from math import inf, sqrt
from heapq import heappop, heappush

SPACES = "spaces"

def dijkstras_shortest_path(initial_position, destination, graph, adj):
    """ Searches for a minimal cost path through a graph using Dijkstra's algorithm.

    Args:
        initial_position: The initial cell from which the path extends.
        destination: The end location for the path.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        If a path exits, return a list containing all cells from initial_position to destination.
        Otherwise, return None.

    """
    # contains weight information of the maze
    vert = {}

    # init dictionary with inf 
    for k in graph[SPACES].keys():
        vert[k] = inf
    
    # priority queue 
    pq = list()
    heappush(pq, (initial_position, 0))
    
    #init vert with first coord 
    vert[initial_position] = 0

    # stores in path in which the algorithm searches and its weight
    # Format: { (x0, y0, w0): [(x1, y1, w1),(x2,y2,w2)...]
    # (x3,y3,w3): [(x4,y4,w4), ...]  
    # ... }
    path_dict = {}

    switch, ret_dest = 1, 0

    # loop until nothing in pq
    while pq:
        u = heappop(pq)[0]
        if not path_dict.get(u):
            path_dict[u] = list()

        nav_edge = adj(level, u)
        print(str(len(pq)) + " : " + str(u[0]) + ", " + str(u[1]))
        #loop through each edge 
        for edge in nav_edge:
            v, weight = edge[0], edge[1]

            # stop if desination is found 
            if switch:
                
                if vert[v] > vert[u] + weight:
                    #print(v)
                    vert[v] = vert[u] + weight
                    path_dict[u].append((v[0], v[1], vert[v]))

                    heappush(pq, (v, vert[v]))

                if v == destination:
                    print("destination reached")
                    pq = []
                    switch 
                    reach_dest = 1

        switch = 1

    # the list to be returned 
    ret_list = list()
   
    # if the destination was found, backtrack the dictionary to find the path
    if reach_dest:

        # init the list with the destination 
        ret_list.append(destination)     
        # set current coordinate to destination in order to backtrack the shortest path
        current_coord = destination

        # iterate until the intial position is reached 
        while current_coord != initial_position:
            
            lowweight, maxcoord, at_least_one = inf, (), 0
            print(str(current_coord[0]) + ", " + str(current_coord[1]) + " : " + str(initial_position[0]) + ", " + str(initial_position[1]))
            # iterate through each item inside the path_dict dictionary 
            for key, value in path_dict.items():
                for v in value:
                    if (v[0], v[1]) == current_coord:
                        if v[2] <= lowweight:
                            lowweight = v[2]
                            maxcoord = key
                            at_least_one = 1
            # makes sure that it will backtrack to the shortest path and not just any path 
            if at_least_one:
                ret_list.insert(0, maxcoord)
                current_coord = maxcoord

    return ret_list


def dijkstras_shortest_path_to_all(initial_position, graph, adj):
    """ Calculates the minimum cost to every reachable cell in a graph from the initial_position.

    Args:
        initial_position: The initial cell from which the path extends.
        graph: A loaded level, containing walls, spaces, and waypoints.
        adj: An adjacency function returning cells adjacent to a given cell as well as their respective edge costs.

    Returns:
        A dictionary, mapping destination cells to the cost of a path from the initial_position.
    """

    # dictionary to be returned 
    vert = {}

    # init dictionary with inf 
    for k in graph[SPACES].keys():
        vert[k] = inf
    
    # priority queue 
    pq = list()
    heappush(pq, (initial_position, 0))
    
    #init vert with first coord 
    vert[initial_position] = 0

    # loop until nothing in pq
    while pq:
        u = heappop(pq)[0]
        nav_edge = adj(level, u)
        for edge in nav_edge:
            v = edge[0]
            weight = edge[1]
            if vert[v] > vert[u] + weight:
                vert[v] = vert[u] + weight
                heappush(pq, (v, vert[v]))

    return vert


def navigation_edges(level, cell):
    """ Provides a list of adjacent cells and their respective costs from the given cell.

    Args:
        level: A loaded level, containing walls, spaces, and waypoints.
        cell: A target location.

    Returns:
        A list of tuples containing an adjacent cell's coordinates and the cost of the edge joining it and the
        originating cell.

        E.g. from (0,0):
            [((0,1), 1),
             ((1,0), 1),
             ((1,1), 1.4142135623730951),
             ... ]
    """

    # original values of the input cell 
    x = cell[0]
    y = cell[1]
    cell_value = level[SPACES][cell]

    # integers to shift the coordinates
    dx = -1
    dy = -1
    
    # the list that is to be returned by the function 
    ret_list = list()
    
    # iterate through each point surrounding the cell
    while dy <= 1:
        while dx <= 1:
            coord = (x + dx, y + dy)
            if(get_cell_type(level, coord) == SPACES and (dx != 0 or dy != 0)):
                # if dx * dy does not equal 0, it means the line is diagonal 
                diagonal = 1 if dx * dy == 0 else sqrt(2)
                dest_value = (0.5 * cell_value + 0.5 * level[SPACES][coord]) * diagonal
                ret_list.append((coord, dest_value))
            dx += 1
        dx = -1 
        dy += 1 

    return ret_list


def test_route(filename, src_waypoint, dst_waypoint):
    """ Loads a level, searches for a path between the given waypoints, and displays the result.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        dst_waypoint: The character associated with the destination waypoint.

    """
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source and destination coordinates from the level.
    src = level['waypoints'][src_waypoint]
    dst = level['waypoints'][dst_waypoint]

    # Search for and display the path from src to dst.
    #path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    path = dijkstras_shortest_path(src, dst, level, navigation_edges)
    if path:
        show_level(level, path)
    else:
        print("No path possible!")


def cost_to_all_cells(filename, src_waypoint, output_filename):
    """ Loads a level, calculates the cost to all reachable cells from 
    src_waypoint, then saves the result in a csv file with name output_filename.

    Args:
        filename: The name of the text file containing the level.
        src_waypoint: The character associated with the initial waypoint.
        output_filename: The filename for the output csv file.

    """
    
    # Load and display the level.
    level = load_level(filename)
    show_level(level)

    # Retrieve the source coordinates from the level.
    src = level['waypoints'][src_waypoint]
    
    # Calculate the cost to all reachable cells from src and save to a csv file.
    costs_to_all_cells = dijkstras_shortest_path_to_all(src, level, navigation_edges)
    save_level_costs(level, costs_to_all_cells, output_filename)

def get_cell_type(level, coord):
    # finds the cell type of the particular coordinate 
    if coord in level["walls"]: 
        return "walls"

    elif coord in level[SPACES]: 
        return SPACES

    return "invalid coord or level"


if __name__ == '__main__':

    filename, src_waypoint, dst_waypoint = 'test_maze.txt', 'a','d'
    
    #file_directory = "../input/"
    level = load_level(filename)

    # Use this function call to find the route between two waypoints.
    test_route(filename, src_waypoint, dst_waypoint)

    # Use this function to calculate the cost to all reachable cells from an origin point.
    cost_to_all_cells(filename, src_waypoint, 'my_maze_costs.csv')
    
