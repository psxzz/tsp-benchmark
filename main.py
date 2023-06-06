#!/usr/bin/env python3.9
from benchmark import *
import solvers
import argparse
import signal
import sys
from os import listdir
from os.path import join, isfile

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="Verbose mode")


def main():
    args = parser.parse_args()

    problem_path = "./problemset/accuracy-benchmarking"

    problems_list = [
        benchmark.TSPProblem(join(problem_path, p)) for p in listdir(problem_path)
    ]

    solvers_list = [
        # benchmark.TSPSolver("Полный перебор", solvers.exact.solve_tsp_brute_force),
        # benchmark.TSPSolver(
        #     "Динамическое программирование", solvers.exact.solve_tsp_dynamic_programming
        # ),
        # benchmark.TSPSolver("Метод ветвей и границ", solvers.exact.tsp_branch_bound),
        benchmark.TSPSolver(
            "Метод ближайшего соседа", solvers.heuristics.solve_tsp_local_search
        ),
        benchmark.TSPSolver(
            "Метод имитации отжига", solvers.heuristics.solve_tsp_simulated_annealing
        ),
        # benchmark.TSPSolver(
        #     "Алгоритм Кристофидеса", solvers.heuristics.solve_christofides
        # ),
    ]

    bench = benchmark.TSPBenchmark(verbose=args.verbose)
    bench.add_problems(sorted(problems_list))
    bench.add_solvers(solvers_list)

    def sigint_handle(signal, frame):
        bench.dump_results("interrupted_benchmark_results.json")
        bench.timechart("interrupted_timechart.png")
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handle)

    bench.run_benchmark()
    bench.dump_results()
    bench.timechart()

    # for problem in problems_list:
    #     problem.show_solutions()


if __name__ == "__main__":
    main()
