from _pytest.fixtures import fixture

from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.subpattern_calculator import SubpatternCalculator


class TestSubpatternCalculator:
    @fixture
    def subpattern_calculator(self, injective_node_mapper):
        return SubpatternCalculator(injective_node_mapper)

    @fixture()
    def injective_node_mapper(self):
        return InjectiveNodeMapper()

    def test_a_pattern_is_found_in_itself(self, subpattern_calculator: SubpatternCalculator):
        pattern = Pattern(3, [(0, 2), (1, 2)], [(0, 1)])
        assert subpattern_calculator.is_subpattern(pattern, pattern, [[0, 1, 2]])

    def test_a_pattern_changing_one_edge_for_non_edge_is_not_found_in_the_original_pattern(self, subpattern_calculator):
        pattern = Pattern(3, [(0, 2), (1, 2)], [(0, 1)])
        pattern_changing_one_edge = Pattern(3, [(0, 2)], [(0, 1), (1, 2)])
        assert not subpattern_calculator.is_subpattern(pattern_changing_one_edge, pattern, [[0, 1, 2]])

    def test_a_mirror_pattern_is_not_found_in_the_pattern(self, subpattern_calculator):
        pattern = Pattern(3, [(0, 2), (1, 2)], [(0, 1)])
        mirror_pattern = Pattern(3, [(0, 2), (0, 1)], [(1, 2)])
        assert not subpattern_calculator.is_subpattern(mirror_pattern, pattern, [[0, 1, 2]])

    def test_a_pattern_minus_one_node_is_found_in_the_original_pattern(self, subpattern_calculator):
        pattern = Pattern(3, [(0, 2), (1, 2)], [(0, 1)])
        pattern_one_less_node = Pattern(2, [(0, 1)], [])
        assert subpattern_calculator.is_subpattern(pattern_one_less_node, pattern, [[0, 1], [0, 2], [1, 2]])
