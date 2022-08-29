from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper


class SubpatternCalculator:
    def __init__(self, injective_node_mapper: InjectiveNodeMapper):
        self._injective_node_mapper = injective_node_mapper

    def is_subpattern(self, base_pattern: Pattern, comp_pattern: Pattern, assignments: list):
        for assignment in assignments:
            sub_pattern = comp_pattern.generate_subpattern(assignment)
            if base_pattern <= sub_pattern:
                return True
        return False
