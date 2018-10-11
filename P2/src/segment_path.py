
def segment_path(path):
	# contains tuples that have each line as input 
	ret = []
	count, final = 0, len(path) - 1
	while(count < final):
		ret.append((path[count], path[count+1]))
		count += 1
	return ret
