from recommendation import GraphBasedRecommendation

import math
import json
import csv


class RecommendIndex:
    def __init__(self):
        self.gbr = GraphBasedRecommendation(pref_weight=0.25, teleport_weight=0.05)

    def index(self, sts_file, stt_file, log_transform=True):
        """
        Index shop_to_shop and shop_to_topic data
        :param sts_file: shop_to_shop file path
        :param stt_file: shop_to_topic file path
        :param log_transform: apply log transfor for shop_to_shop weight
        :return: None
        """
        # Load shop to shop data
        with open(sts_file, encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            rows = []
            for row in reader:
                rows.append(row)

            for row in rows:
                self.gbr.add_node(row['u'], 'shop')
                self.gbr.add_node(row['v'], 'shop')

            if log_transform:
                for row in rows:
                    self.gbr.add_edge(row['u'], row['v'], math.log2(int(row['w'])), 'shop_to_shop')
            else:
                for row in rows:
                    self.gbr.add_edge(row['u'], row['v'], int(row['w']), 'shop_to_shop')

        # Load shop to topic data
        with open(stt_file, encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            rows = []
            for row in reader:
                rows.append(row)

            for row in rows:
                self.gbr.add_node(row['v'], 'topic')
            for row in rows:
                self.gbr.add_bi_edge(row['u'], row['v'], float(row['w']), 'shop_to_topic')

    def recommend(self, edge_weights, personalization={}, neighbors={}):
        """
        Recommendation Implementation
        :param edge_weights: weights of each edge
        :param personalization: behavior and/or tendency data
        :param neighbors: define relation between nodes
        :return: Ranking result of recommendation
        """
        for u, vs in neighbors.items():
            for v in vs:
                self.gbr.add_bi_edge(v, u, 1, 'neighbors')

        pr = self.gbr.fit_predict(edge_weights, personalization)
        self.gbr.remove_edges('neighbors')
        return pr

    def recommend_processor(self, data):
        """
        Wrapping method to response for recommendation
        :param data: json request to parse
        ex)
        data = {
            'behaviors': {'커피빈강남대로점': 10, '빈로이': 20},
            'tendencies': ['커피', '점심', '직장인', '저가'],
            'neighbors': {'커피빈강남대로점': ['봉피양', '빈로이']},
            'weights': {'shop_to_shop': 0.1, 'shop_to_topic': 0.3, 'neighbor': 0.6}
        }

        :return: Ranking result of recommendation
        """
        if type(data) is str:
            data = json.loads(data)

        weights = data['weights']
        personalization = {}
        if 'behaviors' in data:
            for k, v in data['behaviors'].items():
                personalization[k] = v

        if 'tendencies' in data:
            for k in data['tendencies']:
                personalization[k] = 1

        relations = {}
        if 'neighbors' in data:
            relations = data['neighbors']

        return self.recommend(weights, personalization, relations)

