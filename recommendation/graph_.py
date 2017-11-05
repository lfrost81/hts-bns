import networkx as nx
import pprint


class GraphBasedRecommendation:
    def __init__(self, edge_weights=None, pref_weight=0.05, teleport_weight=0.05):
        self.g = nx.DiGraph()
        if edge_weights is None:
            self.edge_weights = {'': 1}
        else:
            self.edge_weights = edge_weights

        self.pref_weight = pref_weight
        self.teleport_weight = teleport_weight
        self.staging_edges = dict()

    def add_node(self, name, node_type=''):
        self.g.add_node(name, t=node_type)

    def add_edge(self, u, v, w=1, edge_type=''):
        if edge_type not in self.staging_edges:
            self.staging_edges[edge_type] = {u: {v: w}}
        elif u not in self.staging_edges[edge_type]:
            self.staging_edges[edge_type][u] = {v: w}
        else:
            self.staging_edges[edge_type][u][v] = w

    def add_bi_edge(self, u, v, w=1, edge_type=''):
        self.add_edge(u, v, w=w, edge_type=edge_type)
        self.add_edge(v, u, w=w, edge_type=edge_type)

    def __normalize_personalization(self, personalization={}):
        # Normalize preference and teleport probabilities
        sum_of_personalization = sum([v for v in personalization.values()])
        sum_of_weights = self.pref_weight + self.teleport_weight
        node_count = self.g.number_of_nodes()
        pref_weight_ratio = self.pref_weight / sum_of_weights
        teleport_weight_ratio = self.teleport_weight / sum_of_weights
        uniform_teleport_prob = 1 / node_count

        for n in self.g.nodes_iter():
            if n in personalization:
                personalization[n] /= sum_of_personalization
                personalization[n] *= pref_weight_ratio
                personalization[n] += uniform_teleport_prob * teleport_weight_ratio
            else:
                personalization[n] = uniform_teleport_prob * teleport_weight_ratio

        return personalization

    def fit_predict(self, personalization={}):
        # Normalize personalization vector
        personalization = self.__normalize_personalization(personalization)

        # Scaling for weights
        for k1, v1 in self.staging_edges.items():
            weight = self.edge_weights[k1]
            for k2, v2 in v1.items():
                base = sum(v2.values())
                for k3, v3 in v2.items():
                    v2[k3] = v3 / base * weight
                    self.g.add_edge(k2, k3, w=v2[k3])

        # Calculate pagerank
        pr = nx.pagerank(self.g, 1 - (self.pref_weight + self.teleport_weight),
                         weight='w', personalization=personalization, max_iter=1000)

        # Formatting result
        result = dict()
        sums = dict()
        for k, v in pr.items():
            node_type = self.g.node[k]['t']
            if node_type not in result:
                result[node_type] = []
                sums[node_type] = 0
            result[node_type].append((k, v))
            sums[node_type] += v

        # Sort and scale
        for k in result.keys():
            result[k] = [(x[0], x[1] / sums[k]) for x in result[k]]
            result[k] = sorted(result[k], key=lambda tup: -tup[1])

        self.g.remove_edges_from(self.g.edges())

        return result


def main():
    edge_weights = {
        'shop_to_shop': 0.30,
        'shop_to_topic': 0.20,
        'neighbors': 0.50
    }
    gbr = GraphBasedRecommendation(edge_weights, pref_weight=0.45, teleport_weight=0.05)

    # Add shop_to_shop relations
    gbr.add_node('신선설농탕', '가맹점')
    gbr.add_node('놀부부대찌개', '가맹점')
    gbr.add_node('스타벅스', '가맹점')
    gbr.add_bi_edge('신선설농탕', '스타벅스', 6, 'shop_to_shop')
    gbr.add_bi_edge('스타벅스', '놀부부대찌개', 5, 'shop_to_shop')
    gbr.add_bi_edge('신선설농탕', '놀부부대찌개', 3, 'shop_to_shop')

    # Add neighbor relations
    gbr.add_bi_edge('스타벅스', '놀부부대찌개', 1, 'neighbors')

    # Add shop_to_topic relations
    gbr.add_node('고급스러운', '토픽')
    gbr.add_node('합리적인', '토픽')
    gbr.add_bi_edge('놀부부대찌개', '합리적인', 1, 'shop_to_topic')
    gbr.add_bi_edge('신선설농탕', '합리적인', 1, 'shop_to_topic')
    gbr.add_bi_edge('스타벅스', '고급스러운', 1, 'shop_to_topic')

    personalization = {
        '스타벅스': 1,
        '신선설농탕': 1,
    }
    pr = gbr.fit_predict(personalization)

    pprint.pprint(pr)

    pprint.pprint(gbr.staging_edges)

if __name__ == '__main__':
    main()
