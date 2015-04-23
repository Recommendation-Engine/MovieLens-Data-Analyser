from operator import itemgetter

class UserOrientedRecommendation(object):

	def __init__(self,k,similarityDict):
		self.__k = k
		self.__similarityDict =similarityDict

	def getSimilarityDict(self):
		return self.__similarityDict

	def findTopKNeighbours(self):
		for key in self.__similarityDict:
			self.__similarityDict[key] = self.findTopKNeighboursForUser(self.__similarityDict[key])

	def findTopKNeighboursForUser(self, userDict):
		sortedList = sorted(userDict.items(), key=itemgetter(1), reverse=True)

		return sortedList[:self.__k]

