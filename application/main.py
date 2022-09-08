from typing import List

from application.domain.pattern import Pattern
from application.mapper.expanded_pattern_graph_mapper import ExpandedPatternGraphMapper
from application.mapper.graph_mapper import GraphMapper
from application.mapper.pattern_mapper import PatternMapper
from application.service.graph_unifying import GraphUnifying
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.pattern_expander import PatternExpander
from application.service.pattern_unifying import PatternUnifying
from application.service.subpattern_calculator import SubpatternCalculator


def main():
    pattern_mapper = PatternMapper()
    base_patterns = pattern_mapper.map_json_to_pattern_list('resources/base_patterns.json')
    two_thinness_patterns = pattern_mapper.map_json_to_pattern_list(
        'resources/4_two_thinness_patterns/two_thinness_patterns.json')
    injective_node_mapper = InjectiveNodeMapper()
    subpattern_calculator = SubpatternCalculator(injective_node_mapper)
    pattern_unifying = PatternUnifying(subpattern_calculator, injective_node_mapper)

    output_pattern_subtraction_optimized(base_patterns, pattern_mapper, GraphMapper(),
                                         pattern_unifying, two_thinness_patterns,
                                         subpattern_calculator)


def merge_resulting_graphs(pattern_unifying: PatternUnifying, patterns: List[Pattern],
                           base_pattern: Pattern):
    pattern_expander = PatternExpander()
    expanded_pattern_graph_mapper = ExpandedPatternGraphMapper()
    decided_patterns = []
    for pattern in patterns:
        expanded_patterns = pattern_expander.expand(pattern)
        decided_patterns = decided_patterns + expanded_patterns

    decided_patterns = pattern_unifying.subtract_many_patterns(base_pattern, decided_patterns)
    pattern_induced_graphs = [expanded_pattern_graph_mapper.map(pattern) for pattern in
                              decided_patterns]
    graph_unifying = GraphUnifying()
    pattern_induced_graphs = graph_unifying.remove_redundant_supergraphs(pattern_induced_graphs)
    return pattern_induced_graphs


def output_pattern_subtraction_optimized(base_patterns: List[Pattern],
                                         pattern_mapper: PatternMapper, graph_mapper: GraphMapper,
                                         pattern_unifying: PatternUnifying, two_thinness_patterns,
                                         subpattern_calculator: SubpatternCalculator):
    index = 0
    for base_pattern in base_patterns:
        patterns_result_file_name = \
            "resources/4_two_thinness_patterns/results/patterns/base_pattern_" + str(
            index) + ".json"
        graphs_result_file_name = "resources/4_two_thinness_patterns/results/graphs/base_pattern_" \
                                  "" + str(
            index) + ".json"
        index += 1
        results = pattern_unifying.subtract_many_patterns(base_pattern, two_thinness_patterns)
        with open(patterns_result_file_name, 'w') as f:
            f.write(pattern_mapper.map_patterns_to_json(results))
        with open(graphs_result_file_name, 'w') as f:
            graphs = merge_resulting_graphs(pattern_unifying, results, base_pattern)
            f.write(graph_mapper.map_graphs_to_json(graphs))


if __name__ == "__main__":
    main()
