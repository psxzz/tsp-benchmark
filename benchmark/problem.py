import tsplib95
import numpy as np
from matplotlib import pyplot as plt
from networkx import nx_pylab as nx


class TSPProblem:
    def __init__(self, path) -> None:
        # self.filepath = path
        self.object = tsplib95.load(path)
        self.name = self.object.name
        self.solutions = []

    def visualize(self, path=None):
        plt.figure(figsize=(10, 8))
        G = self.object.get_graph()
        plt.title(G.name)
        pos = self.object.node_coords

        if path is not None:
            edges = []
            for i in range(0, len(path) - 1):
                edges.append((path[i], path[i + 1]))
            edges.append((path[-1], path[0]))

            nx.draw_networkx_nodes(G, pos)
            nx.draw_networkx_labels(G, pos)
            nx.draw_networkx_edges(G, pos, edge_color="lightgray")
            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=edges,
                edge_color="r",
                arrows=True,
                arrowstyle="-|>",
                arrowsize=15,
            )
        else:
            nx.draw(G, pos, with_labels=True, width=1)

        plt.show()

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
        pos = self.object.node_coords

        fig, ax = plt.subplots(ncols=len(self.solutions), figsize=(16, 9))
        print(self.solutions)
        for i, solution in enumerate(self.solutions):
            edges = []
            path = solution["path"]
            for j in range(0, len(path) - 1):
                edges.append((path[j], path[j + 1]))
            edges.append((path[-1], path[0]))

            ax[i].set_title(
                f"{solution['solver']} - {solution['path_length']} | {solution['time_elapsed']}"
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
