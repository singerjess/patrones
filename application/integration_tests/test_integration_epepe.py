from _pytest.fixtures import fixture

from application.domain.graph import Graph
from application.domain.pattern import Pattern, Edge
from application.mapper.expanded_pattern_graph_mapper import ExpandedPatternGraphMapper
from application.service.pattern_expander import PatternExpander


class TestIntegrationPepe:

    @fixture
    def pattern_expander(self):
        return PatternExpander()

    @fixture()
    def expanded_pattern_graph_mapper(self):
        return ExpandedPatternGraphMapper()

    def test_two_equal_expanded_patterns_are_equal_as_graphs(self, expanded_pattern_graph_mapper):
        pattern_1 = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        pattern_2 = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        graph_1 = expanded_pattern_graph_mapper.map(pattern_1)
        graph_2 = expanded_pattern_graph_mapper.map(pattern_2)

        assert graph_1 == graph_2
        assert graph_1.is_subgraph(graph_2)
        assert graph_2.is_subgraph(graph_1)

    def test_two_mirror_expanded_patterns_are_equal_as_graphs(self, expanded_pattern_graph_mapper):
        pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        mirror_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        graph_1 = expanded_pattern_graph_mapper.map(pattern)
        graph_2 = expanded_pattern_graph_mapper.map(mirror_pattern)

        assert graph_1 == graph_2
        assert graph_1.is_subgraph(graph_2)
        assert graph_2.is_subgraph(graph_1)

    def test_when_expanding_and_mapping_a_pattern_with_one_undecided_edge_then_two_graphs_are_generated(self,
                                                                                                        expanded_pattern_graph_mapper,
                                                                                                        pattern_expander):
        pattern_1 = Pattern(3, [(0, 1)], [(1, 2)])
        patterns_expanded = pattern_expander.expand(pattern_1)
        graphs = expanded_pattern_graph_mapper.map_all(patterns_expanded)

        expected_graph_1 = Graph(3, [(0, 1), (0, 2)])
        expected_graph_2 = Graph(3, [(0, 1)])
        assert len(graphs) == 2
        assert expected_graph_1 in graphs
        assert expected_graph_2 in graphs
