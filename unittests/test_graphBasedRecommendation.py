from recommendation import GraphBasedRecommendation
from unittest import TestCase

import numpy as np
import pprint
import time


class TestGraphBasedRecommendation(TestCase):
    def setUp(self):
        n_node = 300

        edge_weights = {
            'shop_to_shop': 0.33,
            'shop_to_topic': 0.33,
            'neighbors': 0.33
        }
        self.gbr = GraphBasedRecommendation(edge_weights)

        for i in range(n_node):
            self.gbr.add_node(str(i), node_type='가맹점')

        for i in range(n_node):
            for j in range(n_node):
                if i == j:
                    continue
                self.gbr.add_edge(str(i), str(j), np.random.randint(1, 10, 1)[0], 'shop_to_shop')

        for i in range(10):
            self.gbr.add_node(str(i) + '성향', node_type='성향')

        for i in range(10):
            for j in range(n_node):
                self.gbr.add_bi_edge(str(i) + '성향', str(j), 1, 'shop_to_topic')

        for i in range(10):
            for j in range(10):
                if i == j:
                    continue
                self.gbr.add_edge(str(i), str(j), 1, 'neighbors')

    def test_fit_predict(self):
        beg = time.time()
        pr = self.gbr.fit_predict()

        print('elapsed:', time.time() - beg)

        pprint.pprint(pr)
