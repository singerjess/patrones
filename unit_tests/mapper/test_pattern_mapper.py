import json

from application.domain.pattern import Pattern
from application.mapper.pattern_mapper import PatternMapper


class TestPatternMapper():
    def test_a_pattern_is_mapped_to_json_with_the_correct_fields(self):
        total_nodes = 5
        edges = [(0, 1), (2, 3)]
        non_edges = [(1, 2), (1, 3)]
        pattern_mapper = PatternMapper()
        pattern = Pattern(total_nodes, edges, non_edges)

        pattern_json_string = pattern_mapper.map_pattern_to_json(pattern)
        pattern_json = json.loads(pattern_json_string)
        assert pattern_json["total_nodes"] == total_nodes
        assert pattern_json["edges"] == [list(edge) for edge in edges]
        assert pattern_json["non_edges"] == [list(non_edge) for non_edge in non_edges]
