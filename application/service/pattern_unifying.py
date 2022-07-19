from application.domain.pattern import Pattern


class PatternUnifying:
    def possible_assignments(self, remaining_nodes: list, total_nodes):
        if len(remaining_nodes) < total_nodes:
            return []
        if total_nodes == 1:
            return [[remaining_nodes[i]] for i in range(0, len(remaining_nodes))]
        all_possible_assignments = []
        next_ones = self.possible_assignments(remaining_nodes[1:], total_nodes - 1)
        for next_list in next_ones:
            if len(next_list) == total_nodes - 1:
                all_possible_assignments.append([remaining_nodes[0], *next_list])

        next_ones_without_first = self.possible_assignments(remaining_nodes[1:], total_nodes)

        for next_list in next_ones_without_first:
            if len(next_list) == total_nodes:
                all_possible_assignments.append(next_list)
        return all_possible_assignments

    # def compare_two(self, base_pattern: Pattern, comparison_pattern: Pattern, index_base: int, index_comp: int):
    #     result = True
    #     for i in range(0, base_pattern.total_nodes):
    #         for j in range(0, comparison_pattern.total_nodes):
    #             if can_work_as_node_i(base_pattern, comparison_pattern, i, j):
    #
    #
    # def subtract(self, base_pattern: Pattern, comparison_pattern: Pattern):
    #     start_point = 0
    #     pattern_index = 0
    #     for start_point in range(0, comparison_pattern.total_nodes):
    #         if can_work_as_that_pattern_index()
    #
    #     return comparison_pattern
    def this_pattern_works(self, comp_pattern: Pattern, base_pattern: Pattern, assignments):
        i = len(assignments)

        # Make sure that every edge between assigned vertices in the subgraph is also an
        # edge in the graph.
        for edge in base_pattern.edges:
            if edge[0] < i and edge[1] < i:
                if not comp_pattern.has_edge(assignments[edge[0]], assignments[edge[1]]):
                    return False
        for non_edge in base_pattern.non_edges:
            if non_edge[0] < i and non_edge[1] < i:
                if not comp_pattern.has_non_edge(assignments[non_edge[0]], assignments[non_edge[1]]):
                    return False

        # If all the vertices in the subgraph are assigned, then we are done.
        if i == base_pattern.total_nodes:
            return True

        # Otherwise, go through all the possible assignments for the next vertex of
        # the subgraph and try it.
        for j in range(0, comp_pattern.total_nodes):
            if j not in assignments:
                assignments.append(j)
                if self.this_pattern_works(comp_pattern, base_pattern, assignments):
                    # This worked, so we've found an isomorphism.
                    return True
                assignments.pop()

    def subpatterns_of_pattern(self, base_pattern: Pattern, comp_pattern: Pattern):
        assignments = self.possible_assignments([i for i in range(0, comp_pattern.total_nodes)],
                                                base_pattern.total_nodes)
        sub_patterns = [comp_pattern.generate_subpattern(assignment) for assignment in assignments]
        response = []
        for i in range(0, len(sub_patterns)):
            if base_pattern <= sub_patterns[i]:
                response.append(assignments[i])
        return response

    def get_undecided_completion_to_form_subpattern(self, base_pattern: Pattern, comp_pattern: Pattern):
        assignments = self.possible_assignments([i for i in range(0, comp_pattern.total_nodes)],
                                                base_pattern.total_nodes)
        response_pattern = Pattern(comp_pattern.total_nodes, [], [])
        last_calculated_pattern = Pattern(comp_pattern.total_nodes, [], [])
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
