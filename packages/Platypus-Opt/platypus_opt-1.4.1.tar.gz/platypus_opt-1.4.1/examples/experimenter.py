from platypus import (DTLZ2, NSGAII, NSGAIII, Hypervolume, calculate, display,
                      experiment)

if __name__ == "__main__":
    algorithms = [NSGAII, (NSGAIII, {"divisions_outer": 12})]
    problems = [DTLZ2(3)]

    # run the experiment
    results = experiment(algorithms, problems, nfe=10000, seeds=10, display_stats=True)

    # calculate the hypervolume indicator
    hyp = Hypervolume(minimum=[0, 0, 0], maximum=[1, 1, 1])
    hyp_result = calculate(results, hyp)
    display(hyp_result, ndigits=3)
