from collections import defaultdict
from math import sqrt
from operator import itemgetter
import time
import pprint

class RecommendationEngine(object):

	def __init__(self, inputfile, testingfile, k):
		self.__userDic = defaultdict(lambda: defaultdict(int))
		self.__userDicSorted = defaultdict(list)
		self.__similarityDict = defaultdict(lambda: defaultdict(float))
		self.__inputfile = inputfile
		self.__testingfile = testingfile
		self.__k = k

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
			self.__userDicSorted[key] = sorted(self.__userDic[key].items())
		
	def calculateSimilarity(self):
		adjustedUserDict = self._adjustValue(self.__userDicSorted)

		userSize = len(adjustedUserDict)

		for i in range(1, userSize+1):
			for j in range(i+1, userSize+1):
				similarity = self._calculatePairSimilarity(adjustedUserDict[i],adjustedUserDict[j])
				self.__similarityDict[i][j] = similarity
				self.__similarityDict[j][i] = similarity

	def findTopKNeighbours(self):
		for key in self.__similarityDict:
			self.__similarityDict[key] = self._findTopKNeighboursForUser(self.__similarityDict[key])

	def evaluate(self):
		diff = 0.0
		ratingCount = 0
		zeroCount = 0
		with open(self.__testingfile, 'r') as testingfile:
			for line in testingfile:
				items = line.split('::')
				userId = int(items[0])
				movieId = int(items[1])
				rating = int(items[2])
				topKUsers = self.__similarityDict[userId]
				voteScore = 0.0
				count = 0
				for userSimPair in topKUsers:
					if movieId in self.__userDic[userSimPair[0]]:
						voteScore += self.__userDic[userSimPair[0]][movieId]
						count += 1
				if count > 0:
					voteScore /= count
				else:
					zeroCount += 1
				diff += abs(voteScore - rating)
				ratingCount += 1
		diff /= ratingCount
		print 'Average Error:', diff
		print 'zeroCount:', zeroCount

	def _adjustValue(self, userDic):
		adjustUserDic = {}

		for key in userDic:
			adjustlist = []
			for pair in userDic[key]:
				adjustlist.append((pair[0],pair[1]-3))
			adjustUserDic[key] = adjustlist

		return adjustUserDic

	def _calculatePairSimilarity(self, userI, userJ):

		normProduct = self._calculateNorm(userI) * self._calculateNorm(userJ)

		dotProduct = self._calculateDotProduct(userI,userJ)
	
		if dotProduct == 0:
			return 0
		else:
			similarity = dotProduct/normProduct
			return similarity

	def _calculateNorm(self, user):
		norm = 0.0
		for pair in user:
			norm += pair[1] * pair[1]
		return sqrt(norm)

	def _calculateDotProduct(self,userI,userJ):
		i, j, dotProduct = 0, 0, 0.0
		
		while i < len(userI) and j < len(userJ):
			if userI[i][0] < userJ[j][0]:
				i += 1
			elif userJ[j][0] < userI[i][0]:
				j += 1
			else:
				dotProduct += userI[i][1] * userJ[j][1]
				i += 1
				j += 1

		return dotProduct

	def _findTopKNeighboursForUser(self, userDict):
		sortedList = sorted(userDict.items(), key=itemgetter(1), reverse=True)

		return sortedList[:self.__k]

	def getSimilarityDict(self):
		return self.__similarityDict

def main():
	engine = RecommendationEngine("data/training_1.txt", "data/testing_1.txt",300)
	start_time = time.time()
	engine.generateUserDic()
	generateEnd = time.time()
	
	engine.sortUserDictByMovieId()
	sortEnd = time.time()

	engine.calculateSimilarity()
	calculateSimilarityEnd = time.time()

	engine.findTopKNeighbours()
	findTopKNeighboursEnd = time.time()

	engine.evaluate()
	evaluateEnd = time.time()

	print "generateUserDic cost: " + str(generateEnd - start_time) + " secs"
	print "sortUserDictByMovieId cost: " + str(sortEnd - generateEnd) + " secs"
	print "calculateSimilarity cost: " + str(calculateSimilarityEnd - sortEnd) + " secs"
	print "findTopKNeighbours cost: " + str(findTopKNeighboursEnd - calculateSimilarityEnd) + " secs"
	print "evaluate cost" + str(evaluateEnd - findTopKNeighboursEnd) + " secs"
	with open("similarityResult.txt",'w') as output:
		output.write(pprint.pformat(engine.getSimilarityDict(),indent=4))


if __name__ == '__main__':
	main()