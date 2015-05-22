#!/usr/bin/python

class SourceGraph:
    def __init__(self):
        self.node_scores = {}
        self.node_in_edges = {}
        self.total_score = 0.0

    def add_node(self, path):
        assert(path not in self.node_scores)
        self.node_scores[path] = 1.0
        self.node_in_edges[path] = []
        self.total_score += 1.0

    def add_edge(self, src, dst):
        assert(src in self.node_scores)
        assert(dst in self.node_scores)
        self.node_in_edges[dst].append(src)

    def update_scores(self):
        new_scores = {}
        new_total = 0.0
        for path, in_edges in self.node_in_edges.iteritems():
            new_scores[path] = sum(map(lambda x: self.node_scores[x], in_edges)) / float(self.total_score)
            new_total += new_scores[path]

        self.node_scores = new_scores
        self.total_score = new_total

    def get_ranked_paths(self, query, limit=10):
        if query == None or len(query) == 0:
            paths = self.node_scores.keys()
        else:
            paths = filter(lambda x: x.startswith(query), self.node_scores.keys())

        print self.node_scores

        results = sorted(paths, key=lambda x: self.node_scores[x], reverse=True)
        return results[:min(len(results), limit)]

