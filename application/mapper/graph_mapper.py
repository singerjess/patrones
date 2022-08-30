import json

from application.domain.graph import Graph


class GraphMapper:

    def map_graph_to_json(self, graph: Graph):
        edges_string = str([list(elem) for elem in graph.edges()])
        return '{"total_nodes":' + str(
            graph.nodes()) + ',"edges":' + edges_string + '}'

    def map_graphs_to_json(self, results: list):
        return "{\"total\":" + str(len(results)) + ", \"items\": " + str(
            [json.loads(self.map_graph_to_json(result)) for result in results]).replace("\'", "\"") + "}"
