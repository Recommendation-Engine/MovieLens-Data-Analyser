from nose.tools import assert_equals, assert_true
from Similarity import Similarity

class TestSimilarity:

	def setup(self):
		self.userDic = {1:[(1,1),(2,1),(3,4)],
					2:[(1,5),(2,5),(3,2),(4,3)]}
		self.similarity = Similarity(self.userDic)

	def test_adjust_value(self):
		
		adjustedUserDic = self.similarity.adjustValue(self.userDic)

		assert_equals(adjustedUserDic, {1:[(1,-2),(2,-2),(3,1)],2:[(1,2),(2,2),(3,-1),(4,0)]})

	def test_calculate_similarity(self):

		similarityDict = self.similarity.calculateSimilarity()

		assert_equals(similarityDict[1][2],-1.0)
		assert_equals(similarityDict[2][1],-1.0)

class TestCalculatePairSimilarity:

	def setup(self):
		self.userDic = {1:[(1,1),(2,2),(3,3)],
					2:[(4,4),(5,5)]}
		self.similarity = Similarity(self.userDic)

	def test_with_normal_data(self):
		userI = [(1,-2),(2,-1),(3,0)]
		userJ = [(1,2),(2,1),(4,0)]

		similarity = self.similarity.calculatePairSimilarity(userI,userJ)

		assert_true(abs(similarity+1.0)<0.001)

	def test_with_no_common_data(self):
		userI = [(1,-2),(2,-1),(3,0)]
		userJ = [(4,2),(5,1),(6,2)]

		similarity = self.similarity.calculatePairSimilarity(userI,userJ)

		assert_equals(similarity,0.0)

	def test_with_all_zero_value(self):
		userI = [(1,-2),(2,-1),(3,0)]
		userJ = [(1,0),(2,0),(3,0)]

		similarity = self.similarity.calculatePairSimilarity(userI,userJ)

		assert_equals(similarity,0.0)


