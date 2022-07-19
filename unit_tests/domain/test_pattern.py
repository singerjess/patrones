import pytest

from application.domain.pattern import Pattern


class TestPattern:
    def test_when_creating_a_pattern_then_the_edges_are_added_ordered(self):
        pattern = Pattern(4, [(3, 4), (1, 2), (3, 1)], [])
        assert pattern.edges == [(1, 2), (3, 1), (3, 4)]

    def test_when_creating_a_pattern_then_the_non_edges_are_added_ordered(self):
        pattern = Pattern(4, [], [(3, 4), (1, 2), (3, 1)])
        assert pattern.non_edges == [(1, 2), (3, 1), (3, 4)]
