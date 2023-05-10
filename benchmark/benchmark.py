import os
from os.path import isfile, join, splitext
from .problem import TSPProblem
from .solver import TSPSolver


class TSPBenchmark:
    def __init__(self, *problems: TSPProblem):
        self.problems = [p for p in problems]
        self.solvers = []

    def _timer(func):
        from time import time
        from datetime import timedelta

        def _wrapper(self, *args, **kwargs):
            start = time()
            path, length = func(self, *args, **kwargs)
            return (path, length), timedelta(seconds=time() - start)

        return _wrapper

    def add_problem_dir(self, path: str):
        self.problems.extend(
            [
                TSPProblem(join(path, p))
                for p in os.listdir(path)
                if isfile(join(path, p)) and splitext(p)[1] == ".tsp"
            ]
        )

    def add_problems(self, *problems: TSPProblem):
        for problem in problems:
            self.problems.append(problem)

    def add_solvers(self, *solvers: TSPSolver):
        for solver in solvers:
            self.solvers.append(solver)

    @_timer
    def run_test(self, matrix, solver: TSPSolver):
        return solver.solve(matrix)

    def run_benchmark(self):
        for problem in self.problems:
            print(f"\nPROBLEM: {problem.name}")
            dm = problem.get_distance_matrix()
            for solver in self.solvers:
                result, time = self.run_test(dm, solver)
                problem.solutions.append(
                    {
                        "solver": solver.name,
                        "path": list(map(lambda x: x + 1, result[0])),
                        "path_length": result[1],
                        "time_elapsed": time,
                    }
                )
                # print(f"{solver.name}: \t{result[1]} | {time}")
