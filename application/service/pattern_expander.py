from typing import List, Tuple

from application.domain.pattern import Edge, Pattern


class PatternExpander():
    def expand(self, pattern: Pattern) -> List[Pattern]:
        response_patterns = []
        undecided_edges = pattern.get_undecided_edges()
        all_expanded_edges_possibilities = self._expand_recursively(undecided_edges, [])
        for expanded_edges_possibility in all_expanded_edges_possibilities:
            response_patterns.append(Pattern(pattern.total_nodes, pattern.edges + expanded_edges_possibility[0],
                                             pattern.non_edges + expanded_edges_possibility[1]))
        return response_patterns

    def _expand_recursively(self, undecided_edges: list,
                            all_expanded_edges: list) -> List[Tuple[List[Edge], List[Edge]]]:

        if len(undecided_edges) == 0:
            return all_expanded_edges
        undecided_edge = undecided_edges.pop()
        if len(all_expanded_edges) == 0:
            return self._expand_recursively(undecided_edges, [([undecided_edge], []), ([], [undecided_edge])])

        new_all_expanded_edges = []
        for expanded_edges_list_tuple in all_expanded_edges:
            expanded_edges_list_tuple_copy = expanded_edges_list_tuple.copy()
            expanded_edges_list_tuple_copy[0].append(undecided_edge)
            expanded_edges_list_tuple[1].append([(-undecided_edge[0], -undecided_edge[1])])
            new_all_expanded_edges.append(expanded_edges_list_tuple)
            new_all_expanded_edges.append(expanded_edges_list_tuple_copy)
        return self._expand_recursively(undecided_edges, new_all_expanded_edges)
