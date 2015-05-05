import json

class CalculateCategoriesInCommon(object):
	"""docstring for CalculateCategoriesInCommon"""
	def __init__(self, moviefile, outfile, movieNo):
		self.__moviefile = moviefile
		self.__outfile = outfile
		self.__movieNo = movieNo
		self.__movie2cat = {}

	def _processMovieLine(self, line):
		items = line.split("::")
		movieId = int(items[0])
		movieCat = set(items[-1].strip().split('|'))
		return movieId, movieCat

	def loadMovieFile(self):
		with open(self.__moviefile, 'r') as f:
			for line in f:
				movieId, movieCat = self._processMovieLine(line)
				self.__movie2cat[movieId] = movieCat

	def _genJsonRes(self, i, j, commonCat):
		res = []
		oneRecord = {}
		oneRecord['mid'] = i
		oneRecord['mid2'] = j
		oneRecord['cat'] = list(commonCat)
		res.append(json.dumps(oneRecord))
		oneRecord['mid'] = j
		oneRecord['mid2'] = i
		res.append(json.dumps(oneRecord))
		return res

	def catInCommon(self):
		with open(self.__outfile, 'w') as f:
			for i in range(1, self.__movieNo+1):
				for j in range(i+1, self.__movieNo+1):
					if j % 100 == 0:
						print i, j
					if i in self.__movie2cat and j in self.__movie2cat:
						commonCat = self.__movie2cat[i].intersection(self.__movie2cat[j])
						resLines = self._genJsonRes(i, j, commonCat)
						for line in resLines:
							f.write(line+'\n')

def main():
	calCatInCommon = CalculateCategoriesInCommon("../data/movies.txt", 
		"../data/catInCommon.txt", 3952)
	print "loadMovieFile..."
	calCatInCommon.loadMovieFile()
	print "catInCommon..."
	calCatInCommon.catInCommon()

if __name__ == '__main__':
	main()			


		