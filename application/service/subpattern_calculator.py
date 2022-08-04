from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper


class SubpatternCalculator:
    def __init__(self, injective_node_mapper: InjectiveNodeMapper):
        self._injective_node_mapper = injective_node_mapper

    def is_subpattern_with_same_ordering(self, base_pattern: Pattern, comp_pattern: Pattern, assignments: list):
        sub_patterns = [comp_pattern.generate_subpattern(assignment) for assignment in assignments]
        for i in range(0, len(sub_patterns)):
            if base_pattern <= sub_patterns[i]:
                return assignments[i]

    def is_subpattern(self, subpattern: Pattern, pattern: Pattern):  ## TODO: aclarar que es sin orden
        if subpattern.total_nodes > pattern.total_nodes:
            return False
        ordered_assignments = self._injective_node_mapper.possible_assignments_unordered(
            [i for i in range(0, pattern.total_nodes)], subpattern.total_nodes)

        sub_patterns = [pattern.generate_subpattern(assignment) for assignment in ordered_assignments]
        for i in range(0, len(sub_patterns)):
            if subpattern.less_or_equal_without_ordering(sub_patterns[i]):
                return True
        return False
