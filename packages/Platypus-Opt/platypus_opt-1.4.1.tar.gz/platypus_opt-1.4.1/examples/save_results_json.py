from platypus import DTLZ2, NSGAII, save_json

# Select the problem
problem = DTLZ2()

# Create the optimization algorithm.
algorithm = NSGAII(problem)

# Optimize the problem using 10,000 function evaluations.
algorithm.run(10000)

# Save the result to JSON
save_json("NSGAII_DTLZ2_Results.json", algorithm, indent=4)
