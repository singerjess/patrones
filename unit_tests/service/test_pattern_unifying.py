from application.domain.pattern import Pattern
from application.service.pattern_unifying import PatternUnifying


class TestPatternUnifying:

    def test_when_subtracting_the_same_pattern_then_that_pattern_is_returned(self):
        pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        original_pattern = pattern
        assert pattern == PatternUnifying().subtract(pattern, original_pattern)

    def test_when_the_base_pattern_is_less_restrictive_then_the_compare_pattern_is_returned(self):
        base_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        compare_pattern = Pattern(2, [], [(0, 1)])
        assert compare_pattern == PatternUnifying().subtract(base_pattern, compare_pattern)

    def test_when_the_base_pattern_is_a_subpattern_without_undecided_edges_then_the_result_is_the_empty_pattern(self):
        compare_pattern = Pattern(3, [(0, 2)], [(1, 2)])
        base_pattern = Pattern(2, [], [(0, 1)])
        assert Pattern(2, [], []) == PatternUnifying().subtract(base_pattern, compare_pattern)

    def test_when_the_base_pattern_is_a_subpattern_with_undecided_edges_then_the_result_has_the_edges_decided_opposite(
            self):
        base_pattern = Pattern(2, [(0, 1)], [])
        compare_pattern = Pattern(2, [], [])
        assert Pattern(2, [], [(0, 1)]) == PatternUnifying().subtract(base_pattern, compare_pattern)



