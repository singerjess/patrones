from application.mapper.pattern_mapper import PatternMapper
from application.service.pattern_unifying import PatternUnifying


def main():
    pattern_mapper = PatternMapper()
    base_patterns = pattern_mapper.map_json_to_pattern_list('resources/base_patterns.json')
    two_thinness_patterns = pattern_mapper.map_json_to_pattern_list('resources/two_thinness_patterns.json')
    pattern_unifying = PatternUnifying()

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


if __name__ == "__main__":
    main()
