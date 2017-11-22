from recommendation import RecommendIndex
from unittest import TestCase

import pprint


class TestRecommendIndex(TestCase):
    def setUp(self):
        self.ri = RecommendIndex()
        self.ri.index(
            '/Users/hyundai/workspace/pycharm/hts-bns/data/shop_to_shop.csv',
            '/Users/hyundai/workspace/pycharm/hts-bns/data/shop_to_topic.csv'
        )

    def test_recommend(self):
        print('Popular')
        edge_weights = {
            'shop_to_shop': 1.0,
            'shop_to_topic': 0.0,
            'neighbors': 0.0
        }

        result = self.ri.recommend(edge_weights)
        pprint.pprint(result)

        print('Behavior')
        edge_weights = {
            'shop_to_shop': 0.1,
            'shop_to_topic': 0.3,
            'neighbors': 0.6
        }
        personalization = {
            'CJ올리브네트웍스역삼점': 10,
            '아리따움강남역지하점': 10,
            '토니모리강남점': 10
        }
        result = self.ri.recommend(edge_weights, personalization)
        pprint.pprint(result)

        print('Behavior + Tendency')
        personalization = {
            '커피빈강남대로점': 10,
            '빈로이': 20,
            '직장인': 1,
            '점심': 1,
            '커피': 1
        }
        result = self.ri.recommend(edge_weights, personalization)
        pprint.pprint(result)

        print('Before steal competitor\'s sale')
        personalization = {
            '커피빈강남대로점': 20,
            '엔제리너스강남교보타워': 20
        }

        result = self.ri.recommend(edge_weights, personalization)
        pprint.pprint(result)

        print('After steal competitor\'s sale')
        neighbors = {
            '커피빈강남대로점': [ 'CJ올리브네트웍스역삼점', '빈로이', '봉피양' ]
        }
        result = self.ri.recommend(edge_weights, personalization, neighbors)
        pprint.pprint(result)

        self.assertEqual(result['shop'][0][0], '커피빈강남대로점')

    def test_recommend_processor(self):
        data = {
            'behaviors': {'커피빈강남대로점': 10, '빈로이': 20},
            'tendencies': ['커피', '점심', '직장인', '저가'],
            'neighbors': {'커피빈강남대로점': ['봉피양', '빈로이', 'CJ올리브네트웍스역삼점']},
            'weights': {'shop_to_shop': 0.1, 'shop_to_topic': 0.3, 'neighbors': 0.6}
        }

        result = self.ri.recommend_processor(data)
        pprint.pprint(result)

        self.assertEqual(result['shop'][0][0], '커피빈강남대로점')
