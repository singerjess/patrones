from itertools import combinations, permutations

from application.domain.pattern import Pattern


class InjectiveNodeMapper:

    def possible_assignments(self, total_nodes: int, substructure_nodes: int):
        return list(list(combination) for combination in
                    combinations(range(0, total_nodes), substructure_nodes))

    def possible_assignments_unordered(self, total_nodes: int, substructure_nodes: int):
        return list(permutations(range(0, total_nodes), substructure_nodes))
