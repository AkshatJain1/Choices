class Graph:
    def __init__(self, graph_dict=None):
        if graph_dict is None:
            graph_dict = []
        self.graph_dict = graph_dict

    def get_vertices(self):
        return list(self.gdict.keys())

    def get_adjacent_vertices(self, node):
        return self.gdict[node]
