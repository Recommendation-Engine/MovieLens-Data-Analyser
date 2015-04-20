class Measure(object):

	def __init__(self, userDic):
		self.__userDic = userDic

	def distance(self, i, j):
		userI = self.__userDic[i]
		userJ = self.__userDic[j]

		