from typing import List

from application.domain.pattern import Edge
from application.service.injective_node_mapper import InjectiveNodeMapper


class SubgraphCalculator:
    def __init__(self, injective_node_mapper: InjectiveNodeMapper):
        self._injective_node_mapper = injective_node_mapper

    def is_subgraph(self, nodes_subgraph: int, edges_subgraph: List[Edge], nodes_supergraph: int, edges_supergraph: List[Edge]):
        if nodes_supergraph < nodes_subgraph:
            return False
        possible_assignments = self._injective_node_mapper.possible_assignments_unordered(nodes_supergraph, nodes_subgraph)
        for assignment in possible_assignments:
            induced_supergraph_edges = self._generate_induced_edge_mapping(assignment, edges_supergraph)
            is_subgraph = True
            for edge in edges_subgraph:
                if edge not in induced_supergraph_edges and (edge[1], edge[0]) not in induced_supergraph_edges:
                    is_subgraph = False
            if is_subgraph:
                return True
        return False

    def _generate_induced_edge_mapping(self, assignment: List[int], edges_supergraph: List[Edge]) -> List[Edge]:
        new_edges = []
        for edge in edges_supergraph:
            if edge[0] in assignment and edge[1] in assignment:
                new_edges.append((assignment.index(edge[0]), assignment.index(edge[1])))
        return new_edges
