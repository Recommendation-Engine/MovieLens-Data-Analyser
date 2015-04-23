from collections import defaultdict
import operator

def main():
	input_file = "../data/ratings.txt"
	output_file = "../data/movie_order_by_comment_no.txt"
	stat = defaultdict(set)
	stat_list = []
	# Collect user by movie
	with open(input_file, 'r') as f:
		for line in f:
			items = line.split("::")
			stat[items[1]].add(items[0])
	# Count comments and sort
	for key in stat:
		stat_list.append((key, len(stat[key])))
	stat_list = sorted(stat_list, key=operator.itemgetter(1), reverse=True)
	# Write result to file
	with open(output_file, 'w') as f:
		for item in stat_list:
			f.write("{0}\t{1}\n".format(item[0], item[1]))

if __name__ == '__main__':
	main()