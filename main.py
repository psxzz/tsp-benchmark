#!/usr/bin/env python3.9
from benchmark import *
import solvers


def main():
    problems_list = [
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-5.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-7.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-10.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-12.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-13.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-14.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-15.tsp"),
        benchmark.TSPProblem("./problemset/time-benchmarking/tsp-16.tsp"),
        # benchmark.TSPProblem("./problemset/burma14.tsp"),
        # benchmark.TSPProblem("./problemset/gr21.tsp"),
        # benchmark.TSPProblem("./problemset/berlin52.tsp"),
        # benchmark.TSPProblem("./problemset/a280.tsp"),
    ]

    solvers_list = [
        # benchmark.TSPSolver("branch and bound", solvers.exact.tsp_branch_bound),
        benchmark.TSPSolver(
            "dynamic programming", solvers.exact.solve_tsp_dynamic_programming
        ),
        benchmark.TSPSolver("local search", solvers.heuristics.solve_tsp_local_search),
        benchmark.TSPSolver(
            "simulated annealing", solvers.heuristics.solve_tsp_simulated_annealing
        ),
    ]

    bench = benchmark.TSPBenchmark()
    bench.add_problems(problems_list)
    bench.add_solvers(solvers_list)

    bench.run_benchmark()
    bench.dump_results()
    bench.timechart()

    # for p in problems_list:
    #     p.show_solutions()


if __name__ == "__main__":
    main()
