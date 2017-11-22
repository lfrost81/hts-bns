from recommendation import GraphBasedRecommendation

import pprint
import csv
import math


class RecommendIndex:
    def __init__(self):
        edge_weights = {
            'shop_to_shop': 0.1,
            'shop_to_topic': 0.3,
            'neighbors': 0.6
        }
        self.gbr = GraphBasedRecommendation(edge_weights, pref_weight=0.25, teleport_weight=0.05)

    def index(self, sts_file, stt_file, log_transform=True):
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
                self.gbr.add_bi_edge(row['u'], row['v'], 1, 'shop_to_topic')

    def recommend(self, personalization={}, relations={}):
        for u, vs in relations.items():
            for v in vs:
                self.gbr.add_bi_edge(v, u, 1, 'neighbors')

        pr = self.gbr.fit_predict(personalization)
        self.gbr.remove_edges('neighbors')
        return pr


if __name__ == '__main__':
    ri = RecommendIndex()
    ri.index(
        '/Users/hyundai/workspace/pycharm/hts-bns/data/shop_to_shop.csv',
        '/Users/hyundai/workspace/pycharm/hts-bns/data/shop_to_topic.csv'
    )

    ###personalization = {
    ###    '커피빈강남대로점': 7,
    ###    '직장인': 1,
    ###    '점심': 1,
    ###}
    relations = {}

    personalization = {
        '엔제리너스강남교보타워': 20,
        '커피빈강남대로점': 20,
    }
    relations = {
        '커피빈강남대로점': [
            'CJ올리브네트웍스역삼점',
            '빈로이',
            '봉피양'
        ]
    }

    result = ri.recommend(personalization, relations)
    pprint.pprint(result['shop'][0:10])
    pprint.pprint(result['topic'][0:5])

