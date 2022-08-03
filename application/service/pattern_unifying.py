from application.domain.pattern import Pattern
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.subpattern_calculator import SubpatternCalculator


class PatternUnifying:
    def __init__(self, subpattern_calculator: SubpatternCalculator, injective_node_mapper: InjectiveNodeMapper):
        self.subpattern_calculator = subpattern_calculator
        self.injective_node_mapper = injective_node_mapper

    def get_undecided_completion_to_form_subpattern(self, base_pattern: Pattern, comp_pattern: Pattern) -> Pattern:
        assignments = self.injective_node_mapper.possible_assignments([i for i in range(0, comp_pattern.total_nodes)],
                                                                      base_pattern.total_nodes)
        subpattern = self.subpattern_calculator.subpattern(base_pattern, comp_pattern, assignments)
        if subpattern is not None:
            return Pattern(0, [], [])  # the null pattern

        response_pattern = Pattern(comp_pattern.total_nodes, [*comp_pattern.edges], [*comp_pattern.non_edges])
        last_calculated_pattern = Pattern(comp_pattern.total_nodes, [*comp_pattern.edges], [*comp_pattern.non_edges])
        is_first_run = True
        while is_first_run or response_pattern != last_calculated_pattern:
            is_first_run = False
            response_pattern = last_calculated_pattern
            for i in range(0, len(assignments)):
                induced_sub_pattern = comp_pattern.generate_subpattern(assignments[i])
                undecided_edges = induced_sub_pattern.get_undecided_edges()
                for undecided_edge in undecided_edges:
                    original_undecided_edge = (assignments[i][undecided_edge[0]], assignments[i][undecided_edge[1]])

                    last_calculated_pattern = self._evaluate_undecided_edge(base_pattern, comp_pattern,
                                                                            induced_sub_pattern,
                                                                            last_calculated_pattern,
                                                                            original_undecided_edge, undecided_edge)
                    comp_pattern = Pattern(comp_pattern.total_nodes, comp_pattern.edges,
                                           comp_pattern.non_edges) + last_calculated_pattern
        return response_pattern

    def _evaluate_undecided_edge(self, base_pattern, comp_pattern, induced_sub_pattern, last_pattern,
                                 original_undecided_edge, undecided_edge):
        if undecided_edge in base_pattern.edges:
            induced_sub_pattern_plus_edge = Pattern(induced_sub_pattern.total_nodes,
                                                    induced_sub_pattern.get_all_edges() + [undecided_edge],
                                                    induced_sub_pattern.get_all_non_edges())
            if base_pattern <= induced_sub_pattern_plus_edge:
                last_pattern = last_pattern + Pattern(comp_pattern.total_nodes, [],
                                                      [original_undecided_edge])
        else:
            if undecided_edge in base_pattern.non_edges:
                induced_sub_pattern_plus_non_edge = Pattern(induced_sub_pattern.total_nodes,
                                                            induced_sub_pattern.get_all_edges(),
                                                            induced_sub_pattern.get_all_non_edges() + [
                                                                undecided_edge])
                if base_pattern <= induced_sub_pattern_plus_non_edge:
                    last_pattern = last_pattern + Pattern(comp_pattern.total_nodes,
                                                          [original_undecided_edge], [])
        return last_pattern

    def subtract_many_patterns(self, base_pattern, patterns):
        pattern_merges = []
        results = []
        for two_thinness_pattern in patterns:
            pattern_merge = self.get_undecided_completion_to_form_subpattern(base_pattern,
                                                                             two_thinness_pattern)
            if pattern_merge.total_nodes != 0:
                pattern_merges.append(pattern_merge)
        pattern_merges.sort(key=lambda p: len(p.edges))
        for pattern in pattern_merges:
            for other_pattern in pattern_merges:
                if pattern is not other_pattern:
                    result = self.get_undecided_completion_to_form_subpattern(pattern,
                                                                              other_pattern)
                    if result.total_nodes == 0:
                        pattern_merges.remove(other_pattern)
            results.append(pattern)
        return results
