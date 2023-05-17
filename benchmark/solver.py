class TSPSolver:
    def __init__(self, name, solve_func, **kwargs):
        self.name = name
        self.func = solve_func
        self.kwargs = kwargs

    def solve(self, *args):
        return self.func(*args, **self.kwargs)
