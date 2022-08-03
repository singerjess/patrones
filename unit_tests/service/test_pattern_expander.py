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
        assert [expanded_pattern_with_decided_edge, expanded_pattern_with_decided_non_edge] == pattern_expander.expand(pattern_with_one_undecided_edge)
