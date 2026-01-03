import sys
import optimal.solver as sv


if len(sys.argv) != 2:
    print("Usage: python solver_hard.py <cubestring>")
    sys.exit(1)
cubestring = sys.argv[1]
if len(cubestring) == 54:
    result = sv.solve(cubestring)
    print(result)
else:
    print('Wrong length of cubestring')

