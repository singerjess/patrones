from typing import Tuple

import graphviz

Edge = Tuple[int, int]


class Pattern:
    def __init__(self, total_nodes, edges, non_edges):
        self._assert_edges_and_non_edges_do_not_intersect(edges, non_edges)
        self.total_nodes = total_nodes
        self.edges = sorted(set(edges), key=lambda edge: (edge[0], edge[1]))
        self.non_edges = sorted(set(non_edges), key=lambda non_edge: (non_edge[0], non_edge[1]))

    def get_edges(self, node_index):
        response = []
        for edge in self.edges:
            if edge[0] == node_index:
                response.append(edge[1])
        return response

    def get_all_edges(self):
        return self.edges

    def get_all_non_edges(self):
        return self.non_edges

    def get_non_edges(self, node_index):
        response = []
        for edge in self.non_edges:
            if edge[0] == node_index:
                response.append(edge[1])
        return response

    def get_undecided_edges(self):
        response = []
        for node_index in range(0, self.total_nodes):
            for x in range(node_index + 1, self.total_nodes):
                undecided = True
                for edge in self.get_edges(node_index):
                    if edge == x:
                        undecided = False
                for non_edge in self.get_non_edges(node_index):
                    if non_edge == x:
                        undecided = False
                if undecided:
                    response.append((node_index, x))
        return response

    def __eq__(self, other):
        if isinstance(other, Pattern):
            return self.edges == other.edges and self.non_edges == other.non_edges \
                   and self.total_nodes == other.total_nodes
        return False

    def __le__(self, other):
        if isinstance(other, Pattern):
            return set(self.edges).issubset(set(other.edges)) and set(self.non_edges).issubset(set(other.non_edges)) \
                   and self.total_nodes <= other.total_nodes
        return False

    def __lt__(self, other):
        if isinstance(other, Pattern):
            return set(self.edges).issubset(set(other.edges)) and set(self.non_edges).issubset(set(other.non_edges)) \
                   and self.total_nodes <= other.total_nodes and (
                           len(self.edges) < len(other.edges) or len(self.non_edges) < len(
                       other.non_edges) or self.total_nodes < other.total_nodes)
        return False

    def __add__(self, other):
        if isinstance(other, Pattern) and other.total_nodes == self.total_nodes:
            return Pattern(self.total_nodes, self.edges + [*other.edges], self.non_edges + [*other.non_edges])
        return False

    def has_edge(self, node1, node2):
        return node2 in self.get_edges(node1)

    def has_non_edge(self, node1, node2):
        return node2 in self.get_non_edges(node1)

    def generate_subpattern(self, assignment: list):
        total_nodes = len(assignment)
        edges = []
        for i in range(0, len(assignment)):
            for edge in self.edges:
                if edge[0] == assignment[i] and edge[1] in assignment:  ### TODO: refctor
                    index = assignment.index(edge[1])
                    edges.append((i, index))
        non_edges = []
        for i in range(0, len(assignment)):
            for non_edge in self.non_edges:
                if non_edge[0] == assignment[i] and non_edge[1] in assignment:  ### TODO: refctor
                    index = assignment.index(non_edge[1])
                    non_edges.append((i, index))
        return Pattern(total_nodes, edges, non_edges)

    def to_dot_format(self):
        dot = graphviz.Digraph(comment='Patrón')
        for i in range(0, self.total_nodes):
            dot.node(str(i), 'node_' + str(i))
        # pendiente

    def __repr__(self):
        return "total_nodes:" + str(self.total_nodes) + "\nedges: " + ''.join(
            map(str, self.edges)) + "\nnon_edges: " + ''.join(map(str, self.non_edges)) + '\n'

    def __str__(self):
        return "total_nodes:" + str(self.total_nodes) + "\nedges: " + ''.join(
            map(str, self.edges)) + "\nnon_edges: " + ''.join(map(str, self.non_edges)) + "\n"

    def _assert_edges_and_non_edges_do_not_intersect(self, edges, non_edges):
        for edge in edges:
            if edge in non_edges:
                raise RuntimeError("Trying to create illegal pattern with edge: " + str(edge))
        for non_edge in non_edges:
            if non_edge in edges:
                raise RuntimeError("Trying to create illegal pattern with edge: " + str(non_edge))
