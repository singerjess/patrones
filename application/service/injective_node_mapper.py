from itertools import combinations, permutations


class InjectiveNodeMapper:

    def possible_assignments(self, remaining_nodes: list, total_nodes):
        return list(list(combination) for combination in combinations(remaining_nodes, total_nodes))

    def possible_assignments_unordered(self, remaining_nodes: list, total_nodes):
        return list(permutations(remaining_nodes, total_nodes))
