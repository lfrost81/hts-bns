import networkx as nx
import copy


class GraphBasedRecommendation:
    def __init__(self, pref_weight=0.05, teleport_weight=0.05):
        self.g = nx.DiGraph()

        self.pref_weight = pref_weight
        self.teleport_weight = teleport_weight
        self.staging_edges = dict()

    def add_node(self, name, node_type=''):
        if name in self.g:
            return

        self.g.add_node(name, t=node_type)

    def add_edge(self, u, v, w=1, edge_type=''):
        if edge_type not in self.staging_edges:
            self.staging_edges[edge_type] = {u: {v: w}}
        elif u not in self.staging_edges[edge_type]:
            self.staging_edges[edge_type][u] = {v: w}
        else:
            self.staging_edges[edge_type][u][v] = w

    def remove_edges(self, edge_type=''):
        if edge_type in self.staging_edges:
            self.staging_edges.pop(edge_type)

    def add_bi_edge(self, u, v, w=1, edge_type=''):
        self.add_edge(u, v, w=w, edge_type=edge_type)
        self.add_edge(v, u, w=w, edge_type=edge_type)

    def __normalize_personalization(self, personalization={}):
        personalization = copy.deepcopy(personalization)

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

    def fit_predict(self, edge_weights, personalization={}):
        # Normalize personalization vector
        personalization = self.__normalize_personalization(personalization)

        if edge_weights is None:
            edge_weights = {'': 1}

        # Scaling for weights
        merged_edges = {}
        for k1, v1 in self.staging_edges.items():
            weight = edge_weights[k1]
            if weight == 0:
                continue
            for k2, v2 in v1.items():
                base = sum(v2.values())
                for k3, v3 in v2.items():
                    v2[k3] = v3 / base * weight
                    if k2 not in merged_edges:
                        merged_edges[k2] = {}
                    if k3 not in merged_edges[k2]:
                        merged_edges[k2][k3] = 0
                    merged_edges[k2][k3] += v2[k3]

        for u, vs in merged_edges.items():
            for v, w in vs.items():
                self.g.add_edge(u, v, w=w)

        # Calculate pagerank
        pr = nx.pagerank(self.g, alpha=1 - (self.pref_weight + self.teleport_weight),
                         weight='w', personalization=personalization, max_iter=100000)

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

