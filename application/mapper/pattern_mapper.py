import json

from patrones.application.domain.pattern import Pattern


class PatternMapper:
    def map_json_to_pattern_list(self, patterns_file_name):
        # Opening JSON file
        patterns_file = open(patterns_file_name)
        patterns = []
        patterns_dict_list = json.load(patterns_file)
        for pattern in patterns_dict_list:
            patterns.append(Pattern(pattern['total_nodes'], [tuple(edges) for edges in pattern["edges"]],
                                    [tuple(non_edges) for non_edges in pattern["non_edges"]]))
        return patterns

    def map_pattern_to_json(self, pattern: Pattern):
        edges_string = str([list(elem) for elem in pattern.edges])
        non_edges_string = str([list(elem) for elem in pattern.non_edges])
        return '{"total_nodes":' + str(
            pattern.total_nodes) + ',"edges":' + edges_string + ', "non_edges":' + non_edges_string + '}'

    def map_patterns_to_json(self, results):
        return str([json.loads(self.map_pattern_to_json(result)) for result in results])
