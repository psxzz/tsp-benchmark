import os
import time
import functools
from .problem import TSPProblem
from .solver import TSPSolver
from typing import List
from matplotlib import pyplot as plt


def _timer(func):
    @functools.wraps(func)
    def _wrapper(*args, **kwargs):
        start = time.perf_counter()
        path, length = func(*args, **kwargs)
        return (path, length), (time.perf_counter() - start)

    return _wrapper


class TSPBenchmark:
    def __init__(self, results_dir: str = "./results/", verbose=False):
        self.results_dir = results_dir
        self.verbose = verbose
        self.problems: List[TSPProblem] = []
        self.solvers: List[TSPSolver] = []

    def add_problems(self, *problems: TSPProblem):
        self.problems.extend(*problems)

    def add_solvers(self, *solvers: TSPSolver):
        self.solvers.extend(*solvers)

    @_timer
    def run_test(self, matrix, solver: TSPSolver):
        return solver.solve(matrix)

    def run_benchmark(self):
        from datetime import timedelta

        for problem in self.problems:
            if self.verbose:
                results = ""
                print(f"Current problem: {problem.name}")

            dm = problem.get_distance_matrix()
            for solver in self.solvers:
                result, time = self.run_test(dm, solver)

                if self.verbose:
                    results += (
                        f"{solver.name}:\t{result} in {timedelta(seconds=time)}\n"
                    )

                problem.solutions[solver.name] = {
                    "path": list(map(lambda x: x + 1, result[0])),
                    "length": int(result[1]),
                    "time": float(time),
                }

            if self.verbose:
                print(results)

    def dump_results(self, name="benchmark_results.json"):
        import json

        path = self.results_dir + name
        with open(path, "w+") as f:
            json.dump([s.dump() for s in self.problems], f, indent=2)

        print(f"Results dumped at {path}")

    def timechart(self, name="timechart.png", scale="linear"):
        path = self.results_dir + name

        plt.figure(figsize=(16, 9))
        # plt.title("Benchmark results: Timechart")
        plt.xlabel("Размерность задачи")
        plt.ylabel("Время выполнения, сек.")

        x = [p.dimension for p in self.problems]
        ys = dict([(p.name, []) for p in self.solvers])
        _ = [
            [ys[k].append(v["time"]) for k, v in p.solutions.items()]
            for p in self.problems
        ]

        for key, times in ys.items():
            plt.plot(x, times, label=key)

        plt.yscale(scale)
        plt.legend()
        plt.grid()
        # plt.show()
        plt.savefig(path)
