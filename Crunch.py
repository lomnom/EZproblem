"""
Main file to run EZproblem from.
EZproblem generates testcases for competitive programming
"""

"""
TODO:
- Create a new folder and run Crunch.py [folder name] to get steps to create a project!
"""

import argparse
import yaml
import os, sys
import importlib.util
import EZproblem as ez
from time import perf_counter
import subprocess
import tempfile

# Let libs be imported from the application directory
sys.path.insert(0, os.path.dirname(__file__)) 

def error(message: str):
	"""Print error message then quit program."""
	print(message)
	exit(1)

def parse_args() -> argparse.Namespace:
	"""Parse args with argparse.
	Will exit program if -h is invoked."""
	parser = argparse.ArgumentParser(
		prog='EZproblem',
		description="The easiest CP problem testcase generator.",
		epilog="Github page: [to add]"
	)
	parser.add_argument('project', help="The project folder", type=str)
	# TODO:
	# parser.add_argument('--reuse', help="Skip generating testcases that already exist in the folder.", type=str)
	# Generate one specific testcase

	return parser.parse_args()

def get_creator(proj_root: str) -> "module":
	"""Loads creator.py from the project directory.
	Takes in path to project."""
	creator_path = proj_root + "creator.py" # Python script with generator functions
	if not os.path.exists(creator_path):
		error(f"creator.py does not exist in the project folder!")

	spec = importlib.util.spec_from_file_location("creator", creator_path)
	creator = importlib.util.module_from_spec(spec)
	spec.loader.exec_module(creator)
	return creator

def display_info(problem: ez.Problem):
	print("[Problem info]")
	print(f"Name: {problem.name}")
	print()
	print(problem.breakdown_str())
	print()
	print(ez.cbr_layout_format(problem.get_layout()))

def run(exc_path: str, input_str: str) -> tuple:
	"""Runs exc_path and passes input_str to stdin.
	Returns stdout and time taken.
	Raises RuntimeError on non-zer0 exit code"""
	with tempfile.NamedTemporaryFile(mode="w+", delete=True) as tmp:
	    tmp.write(input_str)
	    tmp.flush()  # ensure data is written

	    start = perf_counter()
	    proc = subprocess.run(
	        [exc_path],
	        stdin=open(tmp.name, "rb"),
	        stdout=subprocess.PIPE,
	        stderr=subprocess.PIPE,
	    )
	    end = perf_counter()

	if proc.returncode != 0:
	    raise RuntimeError

	return (proc.stdout.decode(errors="replace"), end - start)

def generate_solution(solver_path: str, testcase: str) -> tuple:
	"""Runs testcase through solver to get output and returns it.
	Raises RuntimeError if solver crashes.
	Returns a tuple (output, time taken to compute in seconds)"""
	print("Running solver...")
	try:
		output, duration = run(solver_path, testcase)
	except RuntimeError:
		raise RuntimeError("Solver crashed!")
	print(f"Solved in {round(duration, 2)}s!")
	return (output, duration)

def save_result(out_folder: str, filename: str, data: str) -> str:
	"""Saves a result to a file in the testcase result folder.
	Returns the path it saved to."""
	os.makedirs(out_folder, exist_ok=True)
	with open(out_folder + filename, 'w') as outfile:
		outfile.write(data)
	print(f"Saved result {filename}")
	return out_folder + filename

def generate_testcases(problem: ez.Problem, solver_path: str, out_folder: str, err_file: str = "err_case.in") -> list:
	"""Generate and save all testcases in a project.
	Puts testcases in out_folder in format [n].in [n].out
	Errors and saves as err_case.in if the solver crashes while solving.
	Returns a list of times taken to solve subtasks in order."""
	times = []
	for number, testcase in problem.generate():
		print(f"Input {number} generated")
		try:
			output, duration = generate_solution(solver_path, testcase)
			times.append(duration)
		except RuntimeError:
			error(f"Solver crashed! Bad testcase saved to {save_result(out_folder, err_file, testcase)}")
		
		save_result(out_folder, f"{number}.in", testcase)
		save_result(out_folder, f"{number}.out", output)
	return times

def display_times_breakdown(times: list, problem: ez.Problem):
	"""Takes in a list of times taken to solve subtasks in order
	Displays stats split by subtask and testcase type.
	"""

def main() -> None:
	"""Main program function"""
	args = parse_args()

	# Project file paths
	proj_root = args.project + "/" # Project root directory.
	out_folder = proj_root + "/testcases/"

	if not os.path.exists(proj_root):
		error(f"Project folder {proj_root} does not exist!")

	creator = get_creator(proj_root)
	try:
		problem = creator.problem
	except AttributeError:
		error(
			"Error! There should be a variable named `problem` in the global scope of creator.py.\n"
			"It is the ez.Problem object which defines your problem."
		)

	display_info(problem)
	try:
		input("Press enter to generate testcases, ctrl-c to cancel > ")
	except KeyboardInterrupt:
		error("Cancelled.")

	try:
		solver_path = proj_root + creator.solver
	except AttributeError:
		error(
			"Error! There should be a variable named `solver` in the global scope of creator.py.\n"
			"It is the path to the solver binary for the problem."
		)

	times = generate_testcases(problem, solver_path, out_folder)

if __name__ == "__main__":
	main()