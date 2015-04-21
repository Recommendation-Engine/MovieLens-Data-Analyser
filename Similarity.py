from collections import defaultdict
from math import sqrt

class Similarity(object):

	def __init__(self, userDic):
		self.__userDic = userDic

	def adjustValue(self, userDic):
		adjustUserDic = {}

		for key in userDic:
			adjustlist = []
			for pair in userDic[key]:
				adjustlist.append((pair[0],pair[1]-3))
			adjustUserDic[key] = adjustlist

		return adjustUserDic
		
	def calculateSimilarity(self):
		adjustedUserDict = self.adjustValue(self.__userDic)

		userSize = len(adjustedUserDict)
		similarityDict = defaultdict(lambda: defaultdict(float))

		for i in range(1, userSize+1):
			for j in range(i+1, userSize+1):
				similarity = self.calculatePairSimilarity(adjustedUserDict[i],adjustedUserDict[j])
				similarityDict[i][j] = similarity
				similarityDict[j][i] = similarity

		return similarityDict

	def calculateNorm(self, user):
		norm = 0.0
		for pair in user:
			norm += pair[1] * pair[1]
		return sqrt(norm)

	def calculateDotProduct(self,userI,userJ):
		i, j, dotProduct = 0, 0, 0.0
		
		while i < len(userI) and j < len(userJ):
			if userI[i][0] < userJ[j][0]:
				i += 1
			elif userI[j][0] < userJ[i][0]:
				j += 1
			else:
				dotProduct += userI[i][1] * userJ[j][1]
				i += 1
				j += 1

		return dotProduct
	
	def calculatePairSimilarity(self, userI, userJ):

		normProduct = self.calculateNorm(userI) * self.calculateNorm(userJ)

		dotProduct = self.calculateDotProduct(userI,userJ)
	
		if dotProduct == 0:
			return 0
		else:
			similarity = dotProduct/normProduct
			return similarity