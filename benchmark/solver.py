class TSPSolver:
    def __init__(self, name, solve_func):
        self.name = name
        self.func = solve_func

    def solve(self, args):
        return self.func(args)
