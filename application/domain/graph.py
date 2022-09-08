from typing import List

from application.domain.pattern import Edge
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.subgraph_calculator import SubgraphCalculator


class Graph:
    def __init__(self, nodes: int, edges: List[Edge]):
        self._nodes = nodes
        self._edges = edges

    def edges(self):
        return List.copy(self._edges)

    def nodes(self):
        return self._nodes

    def __hash__(self):
        return hash((self._nodes, *self._edges))

    def __le__(self, other):
        if isinstance(other, Graph):
            if self._nodes > other.nodes():
                return False
            for edge in self.edges():
                if edge not in other.edges() and (edge[1], edge[0]) not in other.edges():
                    return False
            return True
        return False

    def is_subgraph_of(self, graph):
        subgraph_calculator = SubgraphCalculator(InjectiveNodeMapper())
        return subgraph_calculator.is_induced_subgraph(self.nodes(), self.edges(), graph.nodes(),
                                                       graph.edges())

    def __repr__(self):
        return "total_nodes:" + str(self._nodes) + "\nedges: " + ''.join(
            map(str, self._edges)) + '\n'

    def __str__(self):
        return "total_nodes:" + str(self._nodes) + "\nedges: " + ''.join(
            map(str, self._edges)) + "\n"
