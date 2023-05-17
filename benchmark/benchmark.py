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
    def __init__(self):
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
        for problem in self.problems:
            dm = problem.get_distance_matrix()
            for solver in self.solvers:
                result, time = self.run_test(dm, solver)
                problem.solutions[solver.name] = {
                    "path": list(map(lambda x: x + 1, result[0])),
                    "length": int(result[1]),
                    "time": float(time),
                }

    def dump_results(self):
        import json

        with open("benchmark_results.json", "w+") as f:
            json.dump([s.dump() for s in self.problems], f, indent=2)

        print(f"Results dumped at {os.getcwd()}/benchmark_results.json")

    def timechart(self):
        plt.figure(figsize=(16, 9))
        plt.title("Benchmark results: Timechart")
        plt.xlabel("Dimension")
        plt.ylabel("Time, sec.")

        x = [p.dimension for p in self.problems]
        ys = dict([(p.name, []) for p in self.solvers])
        _ = [
            [ys[k].append(v["time"]) for k, v in p.solutions.items()]
            for p in self.problems
        ]

        for key, times in ys.items():
            plt.plot(x, times, label=key)

        plt.legend()
        plt.show()
