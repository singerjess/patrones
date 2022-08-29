from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper


class SubpatternCalculator:
    def __init__(self, injective_node_mapper: InjectiveNodeMapper):
        self._injective_node_mapper = injective_node_mapper

    def is_subpattern(self, base_pattern: Pattern, comp_pattern: Pattern, assignments: list):
        sub_patterns = [comp_pattern.generate_subpattern(assignment) for assignment in assignments]
        for i in range(0, len(sub_patterns)):
            if base_pattern <= sub_patterns[i]:
                return True # todo: devolver algo con mas sentido
        return False
