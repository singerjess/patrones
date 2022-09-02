from typing import Tuple, List

Edge = Tuple[int, int]


class Pattern:
    def __init__(self, total_nodes: int, edges: List[Edge], non_edges: List[Edge]):
        self._assert_edges_and_non_edges_do_not_intersect(total_nodes, edges, non_edges)
        self._total_nodes = total_nodes
        self._edges = sorted(set(edges), key=lambda edge: (edge[0], edge[1]))
        self._non_edges = sorted(set(non_edges), key=lambda non_edge: (non_edge[0], non_edge[1]))

    def neighbors(self, node_index):
        response = []
        for edge in self._edges:
            if edge[0] == node_index:
                response.append(edge[1])
        return response

    def edges(self):
        return List.copy(self._edges)

    def total_nodes(self):
        return self._total_nodes

    def non_edges(self):
        return List.copy(self._non_edges)

    def non_neighbors(self, node_index):
        response = []
        for edge in self._non_edges:
            if edge[0] == node_index:
                response.append(edge[1])
        return response

    def undecided_edges(self):
        response = []
        for node_index in range(0, self._total_nodes):
            for x in range(node_index + 1, self._total_nodes):
                undecided = True
                for edge in self.neighbors(node_index):
                    if edge == x:
                        undecided = False
                for non_edge in self.non_neighbors(node_index):
                    if non_edge == x:
                        undecided = False
                if undecided:
                    response.append((node_index, x))
        return response

    def __eq__(self, other):
        if isinstance(other, Pattern):
            return self._edges == other._edges and self._non_edges == other._non_edges \
                   and self._total_nodes == other._total_nodes
        return False

    def __le__(self, other):
        if isinstance(other, Pattern):
            return set(self._edges).issubset(set(other._edges)) and set(self._non_edges).issubset(set(other._non_edges)) \
                   and self._total_nodes <= other.total_nodes()
        return False

    def __lt__(self, other):
        if isinstance(other, Pattern):
            return set(self._edges).issubset(set(other._edges)) and set(self._non_edges).issubset(set(other._non_edges)) \
                   and self._total_nodes <= other.total_nodes() and (
                           len(self._edges) < len(other._edges) or len(self._non_edges) < len(
                       other.non_edges()) or self.total_nodes() < other.total_nodes())
        return False

    def __add__(self, other):
        if isinstance(other, Pattern) and other.total_nodes() == self._total_nodes:
            return Pattern(self.total_nodes(), self._edges + [*other.edges()], self._non_edges + [*other.non_edges()])
        raise RuntimeError("Patterns with different number of nodes cannot be added")

    def has_edge(self, node1, node2):
        return node2 in self.neighbors(node1)

    def has_non_edge(self, node1, node2):
        return node2 in self.non_neighbors(node1)

    def generate_subpattern(self, assignment: list):
        total_nodes = len(assignment)
        edges = []
        for i in range(0, len(assignment)):
            for edge in self._edges:
                if edge[0] == assignment[i] and edge[1] in assignment:  ### TODO: refctor
                    index = assignment.index(edge[1])
                    edges.append((i, index))
        non_edges = []
        for i in range(0, len(assignment)):
            for non_edge in self._non_edges:
                if non_edge[0] == assignment[i] and non_edge[1] in assignment:  ### TODO: refctor
                    index = assignment.index(non_edge[1])
                    non_edges.append((i, index))
        return Pattern(total_nodes, edges, non_edges)


    def _assert_edges_and_non_edges_do_not_intersect(self, total_nodes, edges, non_edges):
        for edge in edges:
            if edge in non_edges or edge[0] >= total_nodes or edge[1] >= total_nodes:
                raise RuntimeError("Trying to create illegal pattern with edge: " + str(edge))
        for non_edge in non_edges:
            if non_edge in edges or non_edge[0] >= total_nodes or non_edge[1] >= total_nodes:
                raise RuntimeError("Trying to create illegal pattern with edge: " + str(non_edge))
