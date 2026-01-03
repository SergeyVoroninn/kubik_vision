
import kociemba
import sys

"""
             |************|
             |*U1**U2**U3*|
             |************|
             |*U4**U5**U6*|
             |************|
             |*U7**U8**U9*|
             |************|
 ************|************|************|************
 *L1**L2**L3*|*F1**F2**F3*|*R1**R2**R3*|*B1**B2**B3*
 ************|************|************|************
 *L4**L5**L6*|*F4**F5**F6*|*R4**R5**R6*|*B4**B5**B6*
 ************|************|************|************
 *L7**L8**L9*|*F7**F8**F9*|*R7**R8**R9*|*B7**B8**B9*
 ************|************|************|************
             |************|
             |*D1**D2**D3*|
             |************|
             |*D4**D5**D6*|
             |************|
             |*D7**D8**D9*|
             |************|

Each face:

U = Up
D = Down
L = Left
R = Right
F = Front
B = Back

Colors: Use single letters:
Порядок строго определён: U → R → F → D → L → B
"""

"""
# Input your cube state as a string of 54 characters
# Order: UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
#        (Ux9)(Lx9)(Fx9)(Rx9)(Dx9)(Bx9)
"""

if len(sys.argv) == 2:
    cube_string = str(sys.argv[1])

elif len(sys.argv)>2:
    # Example scrambled:
    print('example of cubestring:')
    cube_string = "DRLUUBFBRBLURRLRUBLRDDFDLFUFUFFDBRDUBRUFLLFDDBFLUBLRBD"
    print(cube_string)


else:
    print('Usage: python kubik_solution <cube_string>')
    sys.exit(1)

try:
    solution = kociemba.solve(cube_string)
    len_solution = len(solution.split(sep=" "))
    print(f"Solution: {solution} ({len_solution})")
    # Output: "D R' D2 R F2 D' L2 U B2 U2 R2 B2 L2 D' R2 D' F2 D2"
except Exception as e:
    print("Error:", str(e))