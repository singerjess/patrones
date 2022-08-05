from itertools import combinations, permutations

from application.domain.pattern import Pattern


class InjectiveNodeMapper:

    def possible_assignments(self, big_pattern: Pattern, small_pattern: Pattern):
        return list(list(combination) for combination in
                    combinations(range(0, big_pattern.total_nodes), small_pattern.total_nodes))

    def possible_assignments_unordered(self, big_pattern: Pattern, small_pattern: Pattern):
        return list(permutations(range(0, big_pattern.total_nodes), small_pattern.total_nodes))
