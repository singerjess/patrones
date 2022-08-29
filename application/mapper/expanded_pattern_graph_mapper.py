from typing import List

from application.domain.graph import Graph
from application.domain.pattern import Pattern


class ExpandedPatternGraphMapper:
    def map(self, pattern: Pattern) -> Graph:
        assert pattern.undecided_edges() == []
        edges = pattern.edges()
        total_nodes = pattern.total_nodes()
        return Graph(total_nodes, edges)

    def map_all(self, patterns: List[Pattern]):
        return [self.map(pattern) for pattern in patterns]
