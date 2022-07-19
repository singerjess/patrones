from application.domain.pattern import Pattern
from application.service.pattern_unifying import PatternUnifying


class TestPatternUnifying:
    def test_equal_patterns_have_only_trivial_mapping(self):
        base_pattern = Pattern(3, [(0, 1), (1, 2)], [(0, 2)])
        pattern_unifier = PatternUnifying()
        assignments = pattern_unifier.possible_assignments([i for i in range(0, base_pattern.total_nodes)],
                                                           base_pattern.total_nodes)
        assert [0, 1, 2] == pattern_unifier.subpattern(base_pattern, base_pattern, assignments)

    def test_the_same_pattern_with_different_order_is_not_a_subpattern(self):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        assert comp_pattern == PatternUnifying().get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern)

    def test_the_k2_pattern_is_subpattern_of_a_k3(self):
        base_pattern = Pattern(2, [(0, 1)], [])
        comp_pattern = Pattern(3, [(1, 2), (0, 2), (0, 1)], [])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(0,
                                                                                                                    [],
                                                                                                                    [])

    def test_the_mirror_cordal_pattern_is_found_one_time_in_the_third_thinness_pattern(self):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 3), (2, 4)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(0,
                                                                                                                    [],
                                                                                                                    [])

    def test_when_only_one_non_edge_is_missing_then_it_is_returned_as_an_edge(self):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(3, [(0, 1), (0, 2)], [])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(3, [
            (1, 2), (0, 1), (0, 2)], [])

    def test_an_empty_pattern_cannot_form_a_pattern_with_three_decided_edges_or_non_edges(self):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(4, [], [])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(4,
                                                                                                                    [],
                                                                                                                    [])

    def test_adding_edges_and_non_edges_for_mirror_cordal_vs_ninth_thinness_pattern(self):
        mirror_cordal_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        ninth_thinness_pattern = Pattern(6, [(0, 2), (0, 5), (1, 4)], [(1, 2), (3, 4), (3, 5)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(mirror_cordal_pattern,
                                                                             ninth_thinness_pattern) == \
               Pattern(6, [(2, 5), (0, 2), (0, 5), (1, 4)], [(0, 1), (0, 3), (1, 3), (2, 3), (1, 2), (3, 4), (3, 5)])

    def test_fifth_thinness_pattern_needs_one_non_edge_to_form_chordal_pattern(self):
        chordal_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        first_thinness_pattern = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(chordal_pattern,
                                                                             first_thinness_pattern) == \
               Pattern(4, [(0, 1), (0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])

    def test_the_cocomparability_pattern_is_contained_once_in_the_first_thinness_pattern(self):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        first_thinness_pattern = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                             first_thinness_pattern) == Pattern(0, [],
                                                                                                                [])

    def test_the_fifth_thinness_pattern_can_be_restricted_with_three_more_edges_if_base_graph_is_co_comparability(self):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        fifth_thinness_pattern = Pattern(5, [(0, 4), (0, 3), (1, 4)], [(1, 3), (2, 4)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                             fifth_thinness_pattern) == \
               Pattern(5, [(0, 1), (1, 2), (0, 2), (3, 4), (0, 4), (0, 3), (1, 4)], [(1, 3), (2, 4)])

    def test_the_second_thinness_pattern_can_be_restricted_with_three_more_edges_if_base_graph_is_co_comparability(
            self):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        fifth_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                             fifth_thinness_pattern) == \
               Pattern(5, [(0, 1), (0, 3), (1, 3), (2, 3), (2, 4), (0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])

    def test_the_third_thinness_pattern_contains_a_co_comparability_subpattern(self):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        third_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 4), (2, 3)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                             third_thinness_pattern) == Pattern(0, [],
                                                                                                                [])

    def test_k3_pattern_cannot_be_formed_with_the_third_thinness_pattern(self):
        k3_pattern = Pattern(3, [(1, 2), (0, 2), (0, 1)], [])
        third_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 3), (2, 4)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(k3_pattern,
                                                                             third_thinness_pattern) == third_thinness_pattern

    def test_interval_pattern_should_is_not_formed_in_the_thirteenth_pattern(self):
        interval_pattern = Pattern(3, [(0, 2)], [(0, 1)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        assert PatternUnifying().get_undecided_completion_to_form_subpattern(interval_pattern,
                                                                             thirteenth_thinness_pattern) == Pattern(6,
                                                                                                                     [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3)],
                                                                                                                     [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])
