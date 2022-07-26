from _pytest.fixtures import fixture

from application.domain.graph import Graph
from application.domain.pattern import Pattern
from application.mapper.expanded_pattern_graph_mapper import ExpandedPatternGraphMapper
from application.service.graph_unifying import GraphUnifying
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.pattern_expander import PatternExpander
from application.service.pattern_unifying import PatternUnifying
from application.service.subpattern_calculator import SubpatternCalculator


class TestIntegrationGraphComparison:

    @fixture
    def pattern_expander(self):
        return PatternExpander()

    @fixture()
    def pattern_unifying(self):
        injective_node_mapper = InjectiveNodeMapper()
        return PatternUnifying(SubpatternCalculator(injective_node_mapper), injective_node_mapper)

    @fixture()
    def expanded_pattern_graph_mapper(self):
        return ExpandedPatternGraphMapper()

    def test_two_equal_expanded_patterns_are_equal_as_graphs(self, expanded_pattern_graph_mapper):
        pattern_1 = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        pattern_2 = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        graph_1 = expanded_pattern_graph_mapper.map(pattern_1)
        graph_2 = expanded_pattern_graph_mapper.map(pattern_2)

        assert graph_1 == graph_2
        assert graph_1.is_subgraph_of(graph_2)
        assert graph_2.is_subgraph_of(graph_1)

    def test_two_mirror_expanded_patterns_are_equal_as_graphs(self, expanded_pattern_graph_mapper):
        pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        mirror_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        graph_1 = expanded_pattern_graph_mapper.map(pattern)
        graph_2 = expanded_pattern_graph_mapper.map(mirror_pattern)

        assert set(graph_1.edges()) == {(0, 2), (0, 1)}
        assert set(graph_2.edges()) == {(1, 2), (0, 2)}
        assert graph_1.nodes() == 3
        assert graph_2.nodes() == 3
        assert graph_1 == graph_2
        assert graph_1.is_subgraph_of(graph_2)
        assert graph_2.is_subgraph_of(graph_1)

    def test_K3_and_3K1_are_not_equal_graphs(self, expanded_pattern_graph_mapper):
        graph_3k1 = Graph(3, [])
        graph_k3 = Graph(3, [(0, 1), (1, 2), (0, 2)])

        assert graph_3k1 != graph_k3
        assert not graph_3k1.is_subgraph_of(graph_k3)
        assert not graph_k3.is_subgraph_of(graph_3k1)

    def test_chordal_and_comparability_patterns_are_equal_as_graphs(self,
                                                                    expanded_pattern_graph_mapper):
        chordal_pattern = Pattern(3, [(0, 2), (1, 2)], [(0, 1)])
        comparability_pattern = Pattern(3, [(0, 1), (1, 2)], [(0, 2)])
        chordal_graph = expanded_pattern_graph_mapper.map(chordal_pattern)
        comparability_graph = expanded_pattern_graph_mapper.map(comparability_pattern)

        assert set(chordal_graph.edges()) == {(0, 2), (1, 2)}
        assert set(comparability_graph.edges()) == {(0, 1), (1, 2)}
        assert comparability_graph.nodes() == 3
        assert chordal_graph.nodes() == 3
        assert comparability_graph == chordal_graph
        assert comparability_graph.is_subgraph_of(chordal_graph)
        assert chordal_graph.is_subgraph_of(comparability_graph)

    def test_K2_is_subgraph_of_K3(self):
        graph_k2 = Graph(2, [(0, 1)])
        graph_k3 = Graph(3, [(0, 1), (0, 2), (1, 2)])

        assert graph_k2 != graph_k3
        assert graph_k2.is_subgraph_of(graph_k3)

    def test_when_expanding_and_mapping_a_pattern_with_one_undecided_edge_then_two_graphs_are_generated(
        self, expanded_pattern_graph_mapper, pattern_expander):
        pattern_1 = Pattern(3, [(0, 1)], [(1, 2)])
        patterns_expanded = pattern_expander.expand(pattern_1)
        graphs = expanded_pattern_graph_mapper.map_all(patterns_expanded)

        expected_graph_1 = Graph(3, [(0, 1), (0, 2)])
        expected_graph_2 = Graph(3, [(0, 1)])
        assert len(graphs) == 2
        assert expected_graph_1 in graphs
        assert expected_graph_2 in graphs

    def test_expanding_and_comparing_is_the_same_as_comparing_expanding_and_comparing(self,
                                                                                      expanded_pattern_graph_mapper,
                                                                                      pattern_expander,
                                                                                      pattern_unifying):
        forest_pattern = Pattern(3, [(0, 2), (1, 2)], [])
        pattern_1 = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        pattern_2 = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        comp_patterns = [pattern_1, pattern_2]
        all_patterns_expanded = pattern_expander.expand(pattern_1) + pattern_expander.expand(
            pattern_2)
        patterns_expanded_subtracted = pattern_unifying.subtract_many_patterns(forest_pattern,
                                                                               all_patterns_expanded)

        patterns_subtracted = pattern_unifying.subtract_many_patterns(forest_pattern, comp_patterns)
        subtracted_expanded_patterns = []
        for pattern_subtracted in patterns_subtracted:
            subtracted_expanded_patterns = subtracted_expanded_patterns + pattern_expander.expand(
                pattern_subtracted)

        subtracted_expanded_patterns = pattern_unifying.subtract_many_patterns(forest_pattern,
                                                                               subtracted_expanded_patterns)
        assert set(subtracted_expanded_patterns) == set(patterns_expanded_subtracted)

    def test_when_pattern_appears_on_comp_patterns_then_there_is_no_resulting_graph(self,
                                                                                    expanded_pattern_graph_mapper,
                                                                                    pattern_expander,
                                                                                    pattern_unifying):
        forest_pattern = Pattern(3, [(0, 2), (1, 2)], [])
        pattern_1 = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        pattern_2 = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        comp_patterns = [pattern_1, pattern_2]
        all_patterns_expanded = pattern_expander.expand(pattern_1) + pattern_expander.expand(
            pattern_2)
        all_patterns_expanded_subtracted = pattern_unifying.subtract_many_patterns(forest_pattern,
                                                                                   all_patterns_expanded)

        assert len(all_patterns_expanded_subtracted) == 0

        graphs = expanded_pattern_graph_mapper.map_all(all_patterns_expanded_subtracted)
        assert len(graphs) == 0

    def test_pepe(self, expanded_pattern_graph_mapper, pattern_expander, pattern_unifying):
        co_forest_pattern = Pattern(3, [], [(0, 2), (1, 2)])
        pattern_1 = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        pattern_2 = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        comp_patterns = [pattern_1, pattern_2]

        all_patterns_subtracted = pattern_unifying.subtract_many_patterns(co_forest_pattern,
                                                                          comp_patterns)

        first_pattern_expanded = pattern_expander.expand(all_patterns_subtracted[0])
        second_pattern_expanded = pattern_expander.expand(all_patterns_subtracted[1])
        all_patterns_expanded = second_pattern_expanded + first_pattern_expanded

        all_patterns_expanded_subtracted = pattern_unifying.subtract_many_patterns(
            co_forest_pattern, all_patterns_expanded)
        graphs = expanded_pattern_graph_mapper.map_all(all_patterns_expanded_subtracted)
        graph_unifying = GraphUnifying()
        graphs = graph_unifying.remove_redundant_supergraphs(graphs)

        expected_graphs = [Graph(4, [(0, 2), (0, 3), (1, 3)]),
                           Graph(4, [(0, 1), (0, 2), (0, 3), (1, 3)]),
                           Graph(5, [(0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4)]),
                           Graph(5,
                                 [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4)])]
        assert len(graphs) == 4
        assert len(all_patterns_subtracted) == 2
        assert all_patterns_subtracted[0].edges() == [(0, 2), (0, 3), (1, 3)]
        assert all_patterns_subtracted[1].edges() == [(0, 2), (0, 4), (1, 4), (2, 4)]
        assert all_patterns_subtracted[0].non_edges() == [(1, 2), (2, 3)]
        assert all_patterns_subtracted[1].non_edges() == [(1, 2), (3, 4)]
        assert len(first_pattern_expanded) == 2
        assert len(second_pattern_expanded) == 16
        assert len(graphs) == 4
        for expected_graph in expected_graphs:
            assert expected_graph in graphs
