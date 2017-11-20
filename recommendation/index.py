from recommendation import GraphBasedRecommendation

import pprint
import csv


class RecommendIndex:
    def __init__(self):
        edge_weights = {
            'shop_to_shop': 0.30,
            'shop_to_topic': 0.30,
            'neighbors': 0.40
        }
        self.gbr = GraphBasedRecommendation(edge_weights, pref_weight=0.15, teleport_weight=0.05)

    def index(self, sts_file, stt_file):
        with open(sts_file, encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            rows = []
            for row in reader:
                rows.append(row)

            for row in rows:
                self.gbr.add_node(row['u'], 'shop')
                self.gbr.add_node(row['v'], 'shop')
            for row in rows:
                self.gbr.add_edge(row['u'], row['v'], int(row['w']), 'shop_to_shop')

        with open(stt_file, encoding='utf-8') as fp:
            reader = csv.DictReader(fp)
            rows = []
            for row in reader:
                rows.append(row)

            for row in rows:
                self.gbr.add_node(row['v'], 'topic')
            for row in rows:
                self.gbr.add_edge(row['u'], row['v'], int(row['w']), 'shop_to_topic')

        pprint.pprint(self.gbr.fit_predict()['shop'][0:7])
        self.gbr.add_edge('빈로이', '파리크라상강남역', 1, 'neighbors')
        pprint.pprint(self.gbr.fit_predict()['shop'][0:7])
        self.gbr.remove_edges('neighbors')
        pprint.pprint(self.gbr.fit_predict()['shop'][0:7])


if __name__ == '__main__':
    RecommendIndex().index(
        'd:/workspace/python/hts-bns/data/shop_to_shop.csv',
        'd:/workspace/python/hts-bns/data/shop_to_topic.csv'
    )