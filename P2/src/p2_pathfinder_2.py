from heapq import heappop, heappushdef find_path (source_point, destination_point, mesh):    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    path = []    boxes = {}            indicateD = 0    indicateS = 0	# The dictionary that will be returned with the costs    distances = {}    distances_BACK = {}		# The dictonary that will store the boxes    backboxes = {}    backboxes_BACK = {}	    queue=[]	    # The dictionary that will store the backpointers    backpointers = {}    backpointers_BACK = {}		    for i in mesh["boxes"]:        if i[0]<=source_point[0] and source_point[0]<=i[1]:             if i[2]<=source_point[1] and source_point[1]<=i[3]:                 # The priority queue                 heappush(queue, (0, source_point, i))                 distances[i] = 0                 backboxes[i] = None                 backpointers[i] = (source_point)                 indicateS = 1                 				         if i[0]<=destination_point[0] and destination_point[0]<=i[1]:             if i[2]<=destination_point[1] and destination_point[1]<=i[3]:                 heappush(queue,(0, destination_point, i))                 distances_BACK[i] = 0                 backboxes_BACK[i] = None                 backpointers_BACK[i] = (destination_point)                 indicateD = 1		    #print(source_point, queue[0][2])    if indicateD == 0 or indicateS == 0:        print("EXCEPTION! Source or Destination ERROR!")        return path,boxes.keys()    print("Strat")    while queue:        current_dist_P, Direction_Point, current_boxes = heappop(queue)        #print(backboxes, "  ", backboxes_BACK)        # Check if current node is the destination_point        #print(current_node, "For\n", current_node_BACK, "Back\n")        if Direction_Point == source_point and backboxes_BACK[current_boxes]:            if backboxes_BACK[current_boxes] == current_boxes:            # List containing all cells from source_point to destination_point                tupMeet = (backpointers[current_boxes][1], backpointers_BACK[current_boxes][1])                #print(current_node, backpointers_BACK[current_boxes][1])                path.append(tupMeet)                boxes[current_boxes] = 0                            # Go backwards from destination_point until the source using backpointers            # and add all the nodes in the shortest path into a list                current_back_boxes = current_boxes                while current_back_boxes is not None:                    boxes[current_back_boxes] = 0                    path.append(backpointers[current_back_boxes])                    #print(backpointers[current_back_boxes], "S", "\n")                    current_back_boxes = backboxes[current_back_boxes]			                current_back_boxes_Back = current_boxes                while current_back_boxes_Back is not None:                    boxes[current_back_boxes_Back] = 0                    path.append(backpointers_BACK[current_back_boxes_Back])                    #print(backpointers_BACK[current_back_boxes_Back],"B", "\n")                    current_back_boxes_Back = backboxes_BACK[current_back_boxes_Back]	                #print(path) 	                return path, boxes.keys()        if Direction_Point == destination_point and backboxes[current_boxes]:            if backboxes[current_boxes] == current_boxes:            #print("current_boxes == current_boxes_BACK")            # List containing all cells from source_point to destination_point                tupMeet = (backpointers[current_boxes][1], backpointers_BACK[current_boxes][1])                #print(current_node, backpointers_BACK[current_boxes][1])                path.append(tupMeet)                boxes[current_boxes] = 0                            # Go backwards from destination_point until the source using backpointers            # and add all the nodes in the shortest path into a list                current_back_boxes = current_boxes                while current_back_boxes is not None:                    boxes[current_back_boxes] = 0                    path.append(backpointers[current_back_boxes])                    #print(backpointers[current_back_boxes], "S", "\n")                    current_back_boxes = backboxes[current_back_boxes]                            current_back_boxes_Back = current_boxes                while current_back_boxes_Back is not None:                    boxes[current_back_boxes_Back] = 0                    path.append(backpointers_BACK[current_back_boxes_Back])                    #print(backpointers_BACK[current_back_boxes_Back],"B", "\n")                    current_back_boxes_Back = backboxes_BACK[current_back_boxes_Back]                    #print(path)                    return path, boxes.keys()                        # Calculate cost from current note to all the adjacent ones        if Direction_Point == source_point: #print("Here")            for adj_node_boxes in mesh["adj"][current_boxes]:				                x1 = adj_node_boxes[2]                x2 = adj_node_boxes[3]                y1 = adj_node_boxes[0]                y2 = adj_node_boxes[1]			                if y1 == current_boxes[1]:                    if(x1 < current_boxes[2]):                        x1 = current_boxes[2]                    if(x2 > current_boxes[3]):                        x2 = current_boxes[3]                    adj_node_x = max(x1,min(x2,backpointers[current_boxes][1]))                    adj_node = (y1, adj_node_x)					                if y2 == current_boxes[0]:                    if(x1 < current_boxes[2]):                        x1 = current_boxes[2]                    if(x2 > current_boxes[3]):                        x2 = current_boxes[3]					                    adj_node_x = max(x1,min(x2,backpointers[current_boxes][1]))                    adj_node = (y2, adj_node_x)					                if x1 == current_boxes[3]:                    if (y1 < current_boxes[0]):                        y1 = current_boxes[0]                    if (y2 > current_boxes[1]):                        y2 = current_boxes[1]					                    adj_node_y = max(y1,min(y2,backpointers[current_boxes][0]))                    adj_node = (adj_node_y, x1)					                if x2 == current_boxes[2]:                    if (y1 < current_boxes[0]):                        y1 = current_boxes[0]                    if (y2 > current_boxes[1]):                        y2 = current_boxes[1]                    adj_node_y = max(y1,min(y2,backpointers[current_boxes][0]))                    adj_node = (adj_node_y, x2)									                estCost = abs(adj_node[0]-destination_point[0])+abs(adj_node[1]-destination_point[1])                pathcost = (pow((adj_node[0]-current_node[0]),2)+pow((adj_node[1]-current_node[1]),2))**0.5+current_dist_P            #print("estdit", estDit)                            if adj_node_boxes not in distances.keys() or pathcost< distances[adj_node_boxes]:                    distances[adj_node_boxes] = pathcost                    tup = (current_node, adj_node)                    backpointers[adj_node_boxes] = tup                    backboxes[adj_node_boxes] = current_boxes                    heappush(queue, (pathcost, Direction_Point, adj_node_boxes))            		       									        if Direction_Point == destination_point: #print("Here")            for adj_node_boxes in mesh["adj"][current_boxes]:                                x1 = adj_node_boxes[2]                x2 = adj_node_boxes[3]                y1 = adj_node_boxes[0]                y2 = adj_node_boxes[1]                            if y1 == current_boxes[1]:                    if(x1 < current_boxes[2]):                        x1 = current_boxes[2]                    if(x2 > current_boxes[3]):                        x2 = current_boxes[3]                    adj_node_x = max(x1,min(x2,backpointers_BACK[current_boxes][1]))                    adj_node = (y1, adj_node_x)                                    if y2 == current_boxes[0]:                    if(x1 < current_boxes[2]):                        x1 = current_boxes[2]                    if(x2 > current_boxes[3]):                        x2 = current_boxes[3]                                        adj_node_x = max(x1,min(x2,backpointers_BACK[current_boxes][1]))                    adj_node = (y2, adj_node_x)                                    if x1 == current_boxes[3]:                    if (y1 < current_boxes[0]):                        y1 = current_boxes[0]                    if (y2 > current_boxes[1]):                        y2 = current_boxes[1]                                        adj_node_y = max(y1,min(y2,backpointers_BACK[current_boxes][0]))                    adj_node = (adj_node_y, x1)                                    if x2 == current_boxes[2]:                    if (y1 < current_boxes[0]):                        y1 = current_boxes[0]                    if (y2 > current_boxes[1]):                        y2 = current_boxes[1]                    adj_node_y = max(y1,min(y2,backpointers_BACK[current_boxes][0]))                    adj_node = (adj_node_y, x2)                                                    estCost = abs(adj_node[0]-source_point[0])+abs(adj_node[1]-source_point[1])                pathcost = (pow((adj_node[0]-current_node[0]),2)+pow((adj_node[1]-current_node[1]),2))**0.5+current_dist_P            #print("estdit", estDit)                            if adj_node_boxes not in distances.keys() or pathcost< distances_BACK[adj_node_boxes]:                    distances_BACK[adj_node_boxes] = pathcost                    tup = (current_node, adj_node)                    backpointers_BACK[adj_node_boxes] = tup                    backboxes_BACK[adj_node_boxes] = current_boxes                    heappush(queue, (pathcost, Direction_Point, adj_node_boxes))                print("Exception! No Path Exist!")    return path, boxes.keys()				