class InjectiveNodeMapper:

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
