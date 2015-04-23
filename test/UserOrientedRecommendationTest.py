import sys
sys.path.insert(0, '../')


from nose.tools import assert_equals, assert_true
from UserOrientedRecommendation import UserOrientedRecommendation

class TestUserOrientedRecommendation:

	def test_find_top_k_neighbours_for_user(self):

		similarityDict = {1 : { 2 : 0.1, 3 : 0.2, 4 : 0.3, 5 : 0.4},
						  2 : { 1: 0.1 }}

		userRecom = UserOrientedRecommendation(3, similarityDict)

		assert_equals(userRecom.findTopKNeighboursForUser(similarityDict[1]),[(5, 0.4), (4, 0.3), (3, 0.2)])

	def test_find_top_k_neighbours(self):
		similarityDict = {1 : { 2 : 0.1, 3 : 0.2, 4 : 0.5},
						  2 : { 1 : 0.1, 2 : 0.6, 3 : 0.3},
						  3 : { 1 : 0.2, 2 : 0.3, 4 : 0.1},
						  4 : { 1 : 0.5, 2 : 0.6, 3 : 0.1}}
		userRecom = UserOrientedRecommendation(2, similarityDict)
		
		userRecom.findTopKNeighbours()

		assert_equals(userRecom.getSimilarityDict(), {1: [(4, 0.5), (3, 0.2)], 2: [(2, 0.6), (3, 0.3)], 3: [(2, 0.3), (1, 0.2)], 4: [(2, 0.6), (1, 0.5)]})

