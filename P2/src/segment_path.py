
def segment_path(path):
	# contains tuples that have each line as input 
	ret = []
	count, final = 0, len(path) - 1
	while(count < final):
		ret.append((path[count], path[count+1]))
		count += 1
	return ret
	
def segment_path_rect(dict):
	ret = []
	for keys in dict:
		x1,x2,y1,y2 = [v for v in keys]
		ret.append(((x1+x2)/2, (y1+y2)/2))

	return segment_path(ret)

