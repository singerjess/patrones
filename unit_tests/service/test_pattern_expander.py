from _pytest.fixtures import fixture

from application.domain.pattern import Pattern
from application.service.pattern_expander import PatternExpander


class TestPatternExpander:
    @fixture
    def pattern_expander(self):
        return PatternExpander()

    def test_a_pattern_with_one_undecided_edge_has_two_expanded_patterns_with_both_possibilities(self,
                                                                                                 pattern_expander):
        pattern_with_one_undecided_edge = Pattern(2, [], [])
        expanded_pattern_with_decided_edge = Pattern(2, [(0, 1)], [])
        expanded_pattern_with_decided_non_edge = Pattern(2, [], [(0, 1)])
        assert [expanded_pattern_with_decided_edge, expanded_pattern_with_decided_non_edge] == pattern_expander.expand(
            pattern_with_one_undecided_edge)

    def test_the_cocomparability_pattern_expanded_is_the_cocomparability_pattern(self,
                                                                                 pattern_expander):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        assert [cocomparability_pattern] == pattern_expander.expand(cocomparability_pattern)

    def test_the_first_thinness_pattern_is_expanded_to_two_patterns_with_0_1_edge(self,
                                                                                  pattern_expander):
        first_thinness_pattern = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        first_thinness_pattern_decided_edge = Pattern(4, [(0, 1), (0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        first_thinness_pattern_decided_non_edge = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(0, 1), (1, 2), (2, 3)])

        expanded_patterns = pattern_expander.expand(first_thinness_pattern)

        assert len(expanded_patterns) == 2
        assert first_thinness_pattern_decided_non_edge in expanded_patterns
        assert first_thinness_pattern_decided_edge in expanded_patterns

    def test_a_pattern_with_two_undecided_edges_expands_into_four_patterns_with_edges_decided(self,
                                                                                              pattern_expander):
        pattern_with_two_undecided_edges = Pattern(4, [(0, 3), (1, 3)], [(1, 2), (2, 3)])
        expected_pattern_1 = Pattern(4, [(0, 3), (1, 3), (0, 2), (0, 1)], [(1, 2), (2, 3)])
        expected_pattern_2 = Pattern(4, [(0, 3), (1, 3), (0, 2)], [(1, 2), (2, 3), (0, 1)])
        expected_pattern_3 = Pattern(4, [(0, 3), (1, 3)], [(1, 2), (2, 3), (0, 1), (0, 2)])
        expected_pattern_4 = Pattern(4, [(0, 3), (1, 3), (0, 1)], [(1, 2), (2, 3), (0, 2)])

        expanded_patterns = pattern_expander.expand(pattern_with_two_undecided_edges)

        assert expected_pattern_4 in expanded_patterns
        assert expected_pattern_3 in expanded_patterns
        assert expected_pattern_2 in expanded_patterns
        assert expected_pattern_1 in expanded_patterns
        assert len(expanded_patterns) == 4
