from constraint import Problem

problem = Problem()
problem.addVariable('A', [1,2,3])
problem.addVariable('B',[1,2,3])
problem.addVariable('C',[1,2,3])
problem.addConstraint(lambda A, B: A != B, ['A', 'B'])

solutions = problem.getSolutions()

print(solutions)