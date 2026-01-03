# Rubik's cube + computer vision

## INSTALL
+ for **easy** mode:
    + install requirements `pip install -r requirements_easy.txt`
+ for **hard** mode:
    + create a Pypy virual enviroment with: `pypy -m venv venv_pypy`
    + activate pypy `venv: venv_pypy\Scripts\activate`
    + install requirements  `pip install -r requirements_hard.txt`
    + without PyPy, the hard mode solver may take several _hours_ to complete.


## USAGE
+ Press `Space` to capture the color of a cube face.
+ Press `Q` to exit the program.
1. `python kubik_calibration.py` define colors of your cube. Make sure that you have camera. Place the color of face to record the color for better definitions. Show the colors in the correct order. The calibration is strict — if you show the wrong color, restart the process.
2. `python kubik_vision.py` to run cube view program. You must show all six faces with the correct orientation (e.g., _white_ on top, _green_ in front). The order in which you show the faces does not matter.. Find the front of the rubik's cube. Below is following structure of rubik's cube.
```
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
```
    Each face:

    U = Up 
    D = Down  
    L = Left 
    R = Right 
    F = Front 
    B = Back 

## `kubik_vision.py` supports two modes:

easy: faster, less accurate, no large files  
hard: slower, computes the shortest solution using advanced algorithms

+ to choose the mode:
    + easy:
        + `python kubik_vision.py`
        + `python kubik_vision.py easy`
    + hard:
        + `python kubik_vision.py hard`

+ Advantages of easy mode:
    + fast execution
    + no need for 1 GB of disk space for lookup tables
    + simple to use
+ Advantages of hard mode:
    + computes the shortest possible solution
+ Disadvantages:
    + very slow without PyPy
    + need to install PyPy for faster complete
    + makes files of tables with 1 GB size (delete with `python clear_hard.py`)

## Solution
Solution string consists of space-separated parts, each of them represents a single move:
* A single letter by itself means to turn that face clockwise 90 degrees.
* A letter followed by an apostrophe means to turn that face counterclockwise 90 degrees.
* A letter with the number 2 after it means to turn that face 180 degrees.
```
    Each face:

    U = Up 
    D = Down  
    L = Left 
    R = Right 
    F = Front 
    B = Back 
```
The following solution needs to do next:  
solution: F2 D2 B L2 U'  
* F2: Rotate __front__ face __two__ times clockwise
* D2: Rotate __down__ face __two__ times clockwise
* B: Rotate __back__ face __one__ time clockwise
* L2: Rotate __left__ face __two__ time clockwise
* U': Rotate __up__ face __one__ time counterclockwise

##  Credits and Licenses:
+ Kociemba [link](https://github.com/muodov/kociemba)
+ Rubik's cube two steps solver Optimal [link](https://github.com/hkociemba/RubiksCube-TwophaseSolver)
+ Thanks to these smart and good coders. Thats my first README.md file.
+ If there are some troubles text to my email: serghey117@gmail.com
+ If i dont answer repeat the letter.