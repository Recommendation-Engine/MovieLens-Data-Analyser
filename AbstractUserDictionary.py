from collections import defaultdict

class AbstractUserDictionary(object):

	def __init__(self, inputfile):
		self.__userDic = defaultdict(lambda: defaultdict(int))
		self.__inputfile = inputfile

	def generateUserDic(self):
		with open(self.__inputfile, 'r') as source:
			for line in source:
				items = line.split("::")
				userId = int(items[0])
				movieId = int(items[1])
				rating = int(items[2])
				self.__userDic[userId][movieId] = rating

	def sortUserDictByMovieId(self):
		for key in self.__userDic:
			self.__userDic[key] = sorted(self.__userDic[key].items())

	def getUserDic(self):
		return self.__userDic