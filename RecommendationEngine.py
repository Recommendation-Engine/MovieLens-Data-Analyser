from collections import defaultdict
from math import sqrt
from operator import itemgetter
import time
import pprint
import numpy
from scipy.sparse import csr_matrix, dok_matrix

class RecommendationEngine(object):

	def __init__(self, inputfile, testingfile, userSize, movieSize):
		self.__userDic = defaultdict(lambda: defaultdict(int))
		self.__similarityMatrix = None
		self.__sortedIndexMatrix = None
		self.__inputfile = inputfile
		self.__testingfile = testingfile
		self.__userSize = userSize
		self.__movieSize = movieSize
		self.__userMovieMatrix = dok_matrix((userSize+1,movieSize+1))

	def _processLine(self,line):
		items = line.split("::")
		userId = int(items[0])
		movieId = int(items[1])
		rating = int(items[2])

		return userId, movieId, rating

	def generateUserDic(self):
		with open(self.__inputfile, 'r') as source:
			for line in source:
				userId, movieId, rating = self._processLine(line)

				self.__userDic[userId][movieId] = rating
				self.__userMovieMatrix[userId,movieId] = (rating - 3)
		
	def _generateNormMatrix(self, similarity_matrix):
		square_mag = numpy.diag(similarity_matrix)
		inv_square_mag = 1 / square_mag
		inv_square_mag[numpy.isinf(inv_square_mag)] = 0

		return numpy.diag(numpy.sqrt(inv_square_mag))

	def _calculateCosineMatrix(self,similarity_matrix,norm_matrix):
		cosine_matrix = similarity_matrix * norm_matrix
		cosine_matrix = cosine_matrix.T * norm_matrix

		return cosine_matrix

	def calculateSimilarity(self):
		similarity_matrix = self.__userMovieMatrix.dot(self.__userMovieMatrix.T).todense()
		norm_matrix = self._generateNormMatrix(similarity_matrix)

		self.__similarityMatrix = self._calculateCosineMatrix(similarity_matrix,norm_matrix)

	def sortNeighbours(self):
		self.__sortedIndexMatrix = self.__similarityMatrix.argsort()

	def getTopKNeighbours(self, user, k):
		topKNeighbours = self.__sortedIndexMatrix[user, self.__userSize-k:self.__userSize]

		return numpy.asarray(topKNeighbours).flatten()

	def _calculateVoteScore(self, topKUsers, movieId):
		voteScore = 0.0
		count = 0
		for user in topKUsers:
			if movieId in self.__userDic[user]:
				voteScore += self.__userDic[user][movieId]
				count += 1

		if count > 0:
			voteScore /= count

		return voteScore

	def evaluate(self, k):
		diff = 0.0
		ratingCount = 0

		with open(self.__testingfile, 'r') as testingfile:
			for line in testingfile:
				userId, movieId, rating = self._processLine(line)

				topKUsers = self.getTopKNeighbours(userId, k)
				
				voteScore = self._calculateVoteScore(topKUsers, movieId)
				diff += abs(voteScore - rating)
				ratingCount += 1

		diff /= ratingCount
		return diff

def main():
	engine = RecommendationEngine("data/training.txt", "data/testing.txt", 6040, 3952)
	start_time = time.time()
	engine.generateUserDic()
	generateEnd = time.time()

	print "generateUserDic cost: " + str(generateEnd - start_time) + " secs"

	engine.calculateSimilarity()
	calculateSimilarityEnd = time.time()

	print "calculateSimilarity cost: " + str(calculateSimilarityEnd - generateEnd) + " secs"

	engine.sortNeighbours()
	sortNeighboursEnd = time.time()

	print "sortNeighbours cost: " + str(sortNeighboursEnd - calculateSimilarityEnd) + " secs"

	with open("evaluateResult.txt", 'w') as output:
		for k in range(1,500):
			if k % 10 == 0:
				print "be more confident! K is :" + str(k) + " now!"
				output.write("for k = " + str(k) + " error is : " + str(engine.evaluate(k))) + "\n"
	evaluateEnd = time.time()

	print "evaluate cost: " + str(evaluateEnd - sortNeighboursEnd) + " secs"


if __name__ == '__main__':
	main()