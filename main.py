#!/usr/bin/env python3.9
from benchmark import *
import solvers


def main():
    problems_list = [
        benchmark.TSPProblem("./problemset/burma14.tsp"),
        # benchmark.TSPProblem("./problemset/a280.tsp"),
    ]

    solvers_list = [
        # benchmark.TSPSolver("branch and bound", solvers.exact.tsp_branch_bound),
        benchmark.TSPSolver("local search", solvers.heuristics.solve_tsp_local_search),
        benchmark.TSPSolver(
            "simulated annealing", solvers.heuristics.solve_tsp_simulated_annealing
        ),
    ]

    bench = benchmark.TSPBenchmark()

    bench.add_problems(*problems_list)
    bench.add_solvers(*solvers_list)
    bench.run_benchmark()

    problems_list[0].show_solutions()


if __name__ == "__main__":
    main()
