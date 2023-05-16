import tsplib95
import numpy as np
from matplotlib import pyplot as plt
import networkx as nx
from datetime import timedelta


class TSPProblem:
    def __init__(self, path):
        self.object = tsplib95.load(path)
        self.name = self.object.name
        self.solutions = []

    def get_distance_matrix(self):
        distance_matrix_flattened = np.array(
            [self.object.get_weight(*edge) for edge in self.object.get_edges()]
        )
        distance_matrix = np.reshape(
            distance_matrix_flattened,
            (self.object.dimension, self.object.dimension),
        )
        np.fill_diagonal(distance_matrix, 0)

        return distance_matrix

    def show_solutions(self):
        assert len(self.solutions) > 0
        G = self.object.get_graph()
        G.remove_edges_from(nx.selfloop_edges(G))
        pos = self.object.node_coords

        fig, ax = plt.subplots(ncols=len(self.solutions), figsize=(16, 9))
        fig.suptitle(G.name, fontsize=18)

        for i, solution in enumerate(self.solutions):
            path = solution["path"]
            edges = list(zip(path, path[1:]))

            ax[i].set_title(
                f"{solution['solver']} - {solution['length']} | {timedelta(seconds=solution['time'])}"
            )

            nx.draw_networkx_nodes(G, pos, ax=ax[i])
            nx.draw_networkx_labels(G, pos, ax=ax[i], font_color="black")
            nx.draw_networkx_edges(G, pos, ax=ax[i], edge_color="lightgray")
            nx.draw_networkx_edges(
                G,
                pos,
                ax=ax[i],
                edgelist=edges,
                edge_color="r",
                arrows=True,
                arrowstyle="-|>",
                arrowsize=15,
            )
        plt.show()

    def dump(self):
        return {
            "name": self.name,
            "description": self.object.comment,
            "dimension": self.object.dimension,
            # "solutions": self.solutions,
        }
