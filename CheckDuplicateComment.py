
def main():
	original_file = "data/ratings.txt"

	pair_set = set()

	with open(original_file,'r') as inputfile:
		for line in inputfile:
			current_line = line.split("::")
			pair_set.add((current_line[0],current_line[1]))
		
	print len(pair_set)

if __name__ == '__main__':
	main()