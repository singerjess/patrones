from _pytest.fixtures import fixture

from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.pattern_unifying import PatternUnifying
from application.service.subpattern_calculator import SubpatternCalculator


class TestPatternUnifying:

    @fixture()
    def subpattern_calculator(self, injective_node_mapper):
        return SubpatternCalculator(injective_node_mapper)

    @fixture()
    def injective_node_mapper(self):
        return InjectiveNodeMapper()

    @fixture()
    def pattern_unifying(self, subpattern_calculator, injective_node_mapper):
        return PatternUnifying(subpattern_calculator, injective_node_mapper)

    def test_equal_patterns_have_only_trivial_mapping(self, subpattern_calculator, injective_node_mapper):
        base_pattern = Pattern(3, [(0, 1), (1, 2)], [(0, 2)])
        assignments = injective_node_mapper.possible_assignments(base_pattern,
                                                                 base_pattern)
        assert [0, 1, 2] == subpattern_calculator.is_subpattern_with_same_ordering(base_pattern, base_pattern,
                                                                                   assignments)

    def test_the_same_pattern_with_different_order_is_not_a_subpattern(self, pattern_unifying):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        assert comp_pattern == pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern)

    def test_the_k2_pattern_is_subpattern_of_a_k3(self, pattern_unifying):
        base_pattern = Pattern(2, [(0, 1)], [])
        comp_pattern = Pattern(3, [(1, 2), (0, 2), (0, 1)], [])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(0,
                                                                                                                   [],
                                                                                                                   [])

    def test_the_mirror_cordal_pattern_is_found_one_time_in_the_third_thinness_pattern(self, pattern_unifying):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 3), (2, 4)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(0,
                                                                                                                   [],
                                                                                                                   [])

    def test_when_only_one_non_edge_is_missing_then_it_is_returned_as_an_edge(self, pattern_unifying):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(3, [(0, 1), (0, 2)], [])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(3, [
            (1, 2), (0, 1), (0, 2)], [])

    def test_an_empty_pattern_cannot_form_a_pattern_with_three_decided_edges_or_non_edges(self, pattern_unifying):
        base_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        comp_pattern = Pattern(4, [], [])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern, comp_pattern) == Pattern(4,
                                                                                                                   [],
                                                                                                                   [])

    def test_adding_edges_and_non_edges_for_mirror_cordal_vs_ninth_thinness_pattern(self, pattern_unifying):
        mirror_cordal_pattern = Pattern(3, [(0, 1), (0, 2)], [(1, 2)])
        ninth_thinness_pattern = Pattern(6, [(0, 2), (0, 5), (1, 4)], [(1, 2), (3, 4), (3, 5)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(mirror_cordal_pattern,
                                                                            ninth_thinness_pattern) == \
               Pattern(6, [(2, 5), (0, 2), (0, 5), (1, 4)], [(0, 1), (0, 3), (1, 3), (2, 3), (1, 2), (3, 4), (3, 5)])

    def test_fifth_thinness_pattern_needs_one_non_edge_to_form_chordal_pattern(self, pattern_unifying):
        chordal_pattern = Pattern(3, [(1, 2), (0, 2)], [(0, 1)])
        first_thinness_pattern = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(chordal_pattern,
                                                                            first_thinness_pattern) == \
               Pattern(4, [(0, 1), (0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])

    def test_the_cocomparability_pattern_is_contained_once_in_the_first_thinness_pattern(self, pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        first_thinness_pattern = Pattern(4, [(0, 2), (0, 3), (1, 3)], [(1, 2), (2, 3)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                            first_thinness_pattern) == Pattern(0, [],
                                                                                                               [])

    def test_the_fifth_thinness_pattern_can_be_restricted_with_three_more_edges_if_base_graph_is_co_comparability(self,
                                                                                                                  pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        fifth_thinness_pattern = Pattern(5, [(0, 4), (0, 3), (1, 4)], [(1, 3), (2, 4)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                            fifth_thinness_pattern) == \
               Pattern(5, [(0, 1), (1, 2), (0, 2), (3, 4), (0, 4), (0, 3), (1, 4)], [(1, 3), (2, 4)])

    def test_the_second_thinness_pattern_can_be_restricted_with_three_more_edges_if_base_graph_is_co_comparability(
        self, pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        fifth_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                            fifth_thinness_pattern) == \
               Pattern(5, [(0, 1), (0, 3), (1, 3), (2, 3), (2, 4), (0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])

    def test_the_third_thinness_pattern_contains_a_co_comparability_subpattern(self, pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        third_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 4), (2, 3)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(cocomparability_pattern,
                                                                            third_thinness_pattern) == Pattern(0, [],
                                                                                                               [])

    def test_k3_pattern_cannot_be_formed_with_the_third_thinness_pattern(self, pattern_unifying):
        k3_pattern = Pattern(3, [(1, 2), (0, 2), (0, 1)], [])
        third_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 3), (2, 4)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(k3_pattern,
                                                                            third_thinness_pattern) == third_thinness_pattern

    def test_interval_pattern_is_not_subpattern_of_thirteenth_pattern(self, pattern_unifying):
        interval_pattern = Pattern(3, [(0, 2)], [(0, 1)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        assert pattern_unifying.get_undecided_completion_to_form_subpattern(interval_pattern,
                                                                            thirteenth_thinness_pattern) == Pattern(6, [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3)],
                                                                                                                    [(1,
                                                                                                                    4),
                                                                                                                        (
                                                                                                                        1,
                                                                                                                        5),
                                                                                                                        (
                                                                                                                        2,
                                                                                                                        3),
                                                                                                                        (
                                                                                                                        2,
                                                                                                                        4),
                                                                                                                        (
                                                                                                                        2,
                                                                                                                        5)])

    def test_when_subtracting_two_equal_comp_patterns_then_they_should_be_joined_in_one(self, pattern_unifying):
        interval_pattern = Pattern(3, [(0, 2)], [(0, 1)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        assert pattern_unifying.subtract_many_patterns(interval_pattern,
                                                       [thirteenth_thinness_pattern, thirteenth_thinness_pattern]) == [
                   Pattern(6, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3)],
                           [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])]

    def test_when_subtracting_one_comp_pattern_and_one_subpattern_then_the_subpattern_should_be_the_only_result(self,
                                                                                                                pattern_unifying):
        interval_pattern = Pattern(3, [(0, 2)], [(0, 1)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        subpattern_of_thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4)], [(1, 4), (2, 5), (2, 3)])
        assert pattern_unifying.subtract_many_patterns(interval_pattern,
                                                       [thirteenth_thinness_pattern,
                                                           subpattern_of_thirteenth_thinness_pattern]) == [
                   Pattern(6, [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)],
                           [(1, 4), (1, 5), (2, 3), (2, 4), (2, 5)])]

    def test_given_a_subtraction_if_one_has_the_base_pattern_then_the_other_one_should_be_returned_extended(self,
                                                                                                            pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        third_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 3)], [(1, 2), (2, 4), (2, 3)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        assert pattern_unifying.subtract_many_patterns(cocomparability_pattern,
                                                       [thirteenth_thinness_pattern, third_thinness_pattern]) == [
                   Pattern(6, [(0, 5), (0, 4), (1, 3), (1, 2), (0, 2), (0, 1)], [(1, 4), (2, 5), (2, 3)])]

    def test_when_subtracting_two_non_related_patterns_then_they_both_should_be_returned_extended(self,
                                                                                                  pattern_unifying):
        cocomparability_pattern = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        fifth_thinness_pattern = Pattern(5, [(0, 2), (0, 4), (1, 4)], [(1, 2), (3, 4)])
        thirteenth_thinness_pattern = Pattern(6, [(0, 5), (0, 4), (1, 3)], [(1, 4), (2, 5), (2, 3)])
        assert pattern_unifying.subtract_many_patterns(cocomparability_pattern,
                                                       [thirteenth_thinness_pattern, fifth_thinness_pattern]) == [
                   Pattern(6, [(0, 5), (0, 4), (1, 3), (1, 2), (0, 2), (0, 1)], [(1, 4), (2, 5), (2, 3)]),
                   Pattern(5, [(0, 1), (0, 2), (0, 3), (0, 4), (1, 3), (1, 4), (2, 3), (2, 4)], [(1, 2), (3, 4)])]
