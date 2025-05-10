# EZproblem, a CP testcase generator
Hate how tedious and finnicky it is to create CP testcases from scratch? Dont have enough RAM left in your brain for all that headache?

EZproblem was made to solve this. It is a tool which handles everything in creating testcases for a CP question, leaving just the testcase generator for you to implement. 

All you have to do is write a function which returns your testcase in string form, and EZproblem handles the rest for you. 

EZproblem does:
- Support having multiple testcase types for a subtask
- Automatic allocation of testcase numbers, you just have to tell it how many of a type of testcase you want.
- Automatically generates all .in and .out files
- Generation of solver time statistics by subtask and testcase type, so you can tell if your testcases are too hard/easy

## Tutorial
### Step 1 - Folder structure
A problem to be processed with EZproblem must live in its own folder. Thus, we create a project folder with the following two items:
```
Project folder (Name it whatever you want)
|- creator.py  (The python script which implements testcase generation)
|- solver binary (It can have any name but remember it. It must be a compiled executable.)
```

### Step 2 - Implementing generation
Below is the template for a `creator.py` file
```py
import EZproblem as ez
from random import randint, choice

problem = ez.Problem("INSERT PROBLEM NAME HERE")
solver = "INSERT SOLVER FILENAME HERE"

# problem.new_subtask(ez.cbr_naming(SUBTASK NUMBER, HOW MANY POINTS))
subtask_1 = problem.new_subtask(ez.cbr_naming(1, HOW MANY POINTS))

# Define a function that generates testcases for subtask 1, and how many testcases to generate
# @subtask_1.testcases(How many testcases to generate with this function, name for the subtasks made with this)
@subtask_1.testcases(HOW MANY, INSERT NAME) 
def factory(i): 
	... # Logic to generate
	return testcase_string

# Add 5 more testcases to subtask 1, called "Trolling"
@subtask_1.testcases(5, "Trolling") 
def factory(i): 
	... # Logic to generate
	return testcase_string

subtask_2 = problem.new_subtask(ez.cbr_naming(2, HOW MANY POINTS))

@subtask_2.testcases(HOW MANY, INSERT NAME) 
def factory(i): 
	... # Logic to generate
	return testcase_string

...
```
An example `creator.py` file is in `bracketex/creator.py`. It is commented to serve as a tutorial.

### Step 3 - Generate testcases
Run `python3 Crunch.py [path to project folder]`. The testcases generated will be put in `project folder/testcases/`, in the form `[number].in` and `[number].out`.

Allocation information and time information can be found in the output. The allocation will be the first thing displayed to allow you to double-check you are generating correctly. All statistics will be printed again after generation. 

Sample output at the end of generation (from `bracketex` example):
```
Finished generating for problem bracketex

Solver time breakdown:
For subtask Subtask 1 (10 pts):
- Valid: avg=0.01s min=0.0s max=0.01s
- Random: avg=0.01s min=0.0s max=0.01s
- Trolling: avg=0.01s min=0.0s max=0.01s
> Overall: avg=0.01s min=0.0s max=0.01s
[OMITTED IN README.MD FOR BREVITY]
For subtask Subtask 4 (40 pts):
- Valid: avg=0.03s min=0.03s max=0.03s
- Random: avg=0.02s min=0.02s max=0.03s
- Odd length: avg=0.02s min=0.02s max=0.02s
> Overall: avg=0.02s min=0.02s max=0.03s
For subtask Subtask 5 (0 pts):
- Sample testcases: avg=0.01s min=0.0s max=0.01s
> Overall: avg=0.01s min=0.0s max=0.01s

(recap)
Problem name: bracketex

Testcase breakdown
Subtask 1 (10 pts) (18 non-subset testcases):
- Valid: subtask testcase #1-5, testcase files #1-5
- Random: subtask testcase #6-15, testcase files #6-15
- Trolling: subtask testcase #16-18, testcase files #16-18
[OMITTED IN README.MD FOR BREVITY]
Subtask 4 (40 pts) (23 non-subset testcases):
- Valid: subtask testcase #1-5, testcase files #65-69
- Random: subtask testcase #6-20, testcase files #70-84
- Odd length: subtask testcase #21-23, testcase files #85-87
Subtask 5 (0 pts) (3 non-subset testcases):
- Sample testcases: subtask testcase #1-3, testcase files #88-90

Testcase file numbers:
- Subtask 1 (10 pts): 1-18
- Subtask 2 (30 pts): 19-41
- Subtask 3 (20 pts): 42-64
- Subtask 4 (40 pts): 65-87
- Subtask 5 (0 pts): 88-90

All testcases generated! They are in bracketex/testcases/
```

To run the `bracketex` example, you have to first compile its `solver.cpp` to a binary named `solver` in the folder.

## TODO
1. Implement subtasks inheriting testcases of another subtask (subset)
2. Implement lazy generation where testcases already generated are skipped. 