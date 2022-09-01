from typing import List

from application.domain.graph import Graph


### TODO: validar, hoy por hoy, no estoy contando grafos con más ejes, es decir, si tengo un K3 y
#### un nodo suelto, no lo tomo como subgrafo de un K4. igualmente esto se me cancela antes
#### con los patrones.. Ademas, lo spatrones con menos nodos me cancelan un monton de patrones
#### grandes
class GraphUnifying:
    def remove_redundant_supergraphs(self, graphs: List[Graph]):
        graphs.sort(key=lambda p: len(p.edges()))
        for index, graph in enumerate(graphs):
            for another_index, another_graph in enumerate(graphs):
                if graph.edges() != another_graph.edges() or graph.nodes() != another_graph.nodes():
                    if graph.is_subgraph_of(another_graph):
                        graphs.remove(another_graph)
        return graphs
