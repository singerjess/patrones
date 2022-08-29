from typing import List

from application.domain.pattern import Pattern
from application.mapper.pattern_mapper import PatternMapper
from application.service.injective_node_mapper import InjectiveNodeMapper
from application.service.pattern_expander import PatternExpander
from application.service.pattern_unifying import PatternUnifying
from application.service.subpattern_calculator import SubpatternCalculator


def main():
    pattern_mapper = PatternMapper()
    base_patterns = pattern_mapper.map_json_to_pattern_list('resources/base_patterns.json')
    two_thinness_patterns = pattern_mapper.map_json_to_pattern_list('resources/two_thinness_patterns.json')
    injective_node_mapper = InjectiveNodeMapper()
    subpattern_calculator = SubpatternCalculator(injective_node_mapper)
    pattern_unifying = PatternUnifying(subpattern_calculator, injective_node_mapper)

    output_pattern_subtraction_optimized(base_patterns, pattern_mapper, pattern_unifying, two_thinness_patterns, subpattern_calculator)


def output_pattern_subtraction(base_patterns, pattern_mapper, pattern_unifying, two_thinness_patterns):
    index = 0
    for base_pattern in base_patterns:
        result_file_name = "resources/results/base_pattern_" + str(index) + ".json"
        index += 1
        with open(result_file_name, 'w') as f:
            f.write('[')
            pattern_number = 0
            for two_thinness_pattern in two_thinness_patterns:
                if pattern_number > 0:
                    f.write(",\n")
                pattern_number += 1
                result = pattern_unifying.get_undecided_completion_to_form_subpattern(base_pattern,
                    two_thinness_pattern)
                f.write(pattern_mapper.map_pattern_to_json(result))
            f.write(']')


def output_pattern_subtraction_optimized(base_patterns: List[Pattern], pattern_mapper: PatternMapper, pattern_unifying: PatternUnifying, two_thinness_patterns, subpattern_calculator: SubpatternCalculator):
    index = 0
    pattern_expander = PatternExpander()
    for base_pattern in base_patterns:
        result_file_name = "resources/results/base_pattern_" + str(index) + ".json"
        index += 1
        results = pattern_unifying.subtract_many_patterns(base_pattern, two_thinness_patterns)
        with open(result_file_name, 'w') as f: # todo: ojo, los ordenes no se si vale compararlos asi nomas.. sino tendiras cordal = comparabilidad
            f.write(pattern_mapper.map_patterns_to_json(results))


if __name__ == "__main__":
    main()
