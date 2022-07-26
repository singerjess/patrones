from patrones.application.domain.pattern import Pattern


class SubpatternCalculator:
    def subpattern(self, base_pattern: Pattern, comp_pattern: Pattern, assignments: list):
        sub_patterns = [comp_pattern.generate_subpattern(assignment) for assignment in assignments]
        for i in range(0, len(sub_patterns)):
            if base_pattern <= sub_patterns[i]:
                return assignments[i]
