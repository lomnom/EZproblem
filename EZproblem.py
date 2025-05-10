from typing import Any

"""
File imported by EZproblem project factory.py
Contains the Problem class used to specify testcase info.
This file only handles input creation. Outputs are handled by the main program.
"""

LOGGING = True # Set to true to enable logging.
def log(message: str) -> None:
	"""Log info about the process."""
	if LOGGING:
		print(message)

def number_range(text: str) -> list:
	"""Generates number from a string where numbers are seperated by commas 
	and dashes allow inclusive ranges.
	number_range("1,2-3,0") -> [1,2,3,0]
	"""
	numbers = []
	for part in text.split(","):
		if '-' in part:
			left, right = part.split('-') 
			left = int(left)
			right = int(right)
			for n in range(left, right+1):
				numbers.append(n)
		else:
			numbers.append(int(part))
	return numbers

def cbr_naming(subtask_no: int, points: int):
	"""Subtask name in codebreaker format"""
	return f"Subtask {subtask_no} ({points} pts)"

class Subtask:
	"""Class representing subtask in a CP problem.
	Every subtask has general and specific testcase generating functions.
	Every subtask has specific testcase numbers.

	Attributes:
	- name: str - name of subtask
	- factories: [(number of testcases, factory function, case_type)] - testcase factories
	- subsets: list[Subtask] - A list of subtasks where their testcases 
	    should also be included under this one

	Testcase factory functions generate a testcase of that type.
	It takes index, where first testcase generated of that type has index=1 and second index=2 etc.

	Testcase generation is in order of the factories list."""

	def __init__(self, name: str, subsets: list = None, factories: list = None):
		"""Constructs a subtask. Refer to attributes documentation for arguments.
		subsets and factories are empty by default."""
		self.name = name
		if factories is None:
			factories = []
		self.factories = factories
		if subsets is None:
			subsets = []
		self.subsets = subsets

	def generate_entry(self, entry: list) -> str:
		"""Takes in (number of testcases, factory function, case_type) and yields
		all its testcases."""
		number, factory, case_type = entry
		log(f"Generating {number} {case_type} inputs for subtask {self.name}")

		result = []
		for i in range(number):
			yield factory(i)

		log(f"^ done")

	def get_testcase_count(self) -> int:
		"""Returns number of testcases in this subtask."""
		total = 0
		for number, factory, case_type in self.factories:
			total += number
		return total

	def get_layout(self) -> list:
		"""Returns the layout of testcases in this subtask.
		Returns [(case_type, start idx, end idx), ...]"""
		result = []
		offset = 0
		for number, factory, case_type in self.factories:
			result.append((case_type, offset + 1, offset + number))
			offset += number
		return result

	def generate(self) -> tuple:
		"""An iterator which yields (index (from 1), testcase) for the subtask"""
		counter = 1
		for entry in self.factories:
			for testcase in self.generate_entry(entry):
				yield (counter, testcase)
				counter += 1

	def testcases(self, number: int, case_type: str) -> 'function':
		"""Use this decorator to add testcases to the subtask.
		Takes in number of testcases to add and name of testcase type.
		eg. 
		@subtask.testcases(10, 'general')
		def factory(index): 
			return str(random.randint(1, 1000))
		"""
		def add_testcase(function: 'function') -> None:
			"""Returned by testcases decorator"""
			self.factories.append((number, function, case_type))
		return add_testcase

def cbr_layout_format(layout: list) -> str:
	"""Formats Problem.get_layout() output in codebreaker format."""
	# TODO: handle 1-size windows
	result = "Testcase file numbers:\n"
	for name, windows in layout:
		result += f"- {name}: "
		testcases = []
		for window in windows:
			testcases.append(f"{window[0]}-{window[1]}")
		result += ", ".join(testcases) + '\n'
	return result.strip()

class Problem:
	"""Class representing a CP problem.
	Contains info on testcases to generate and relevant helper methods.

	Attributes:
	- name: str - name of problem
	- subtasks: list - list of subtasks in problem

	Testcase generation is in order of the subtasks list.
	"""

	def __init__(self, name: str, subtasks: list = None):
		"""Constructs a subtask. Refer to attributes documentation for arguments.
		subtasks is empty by default."""
		self.name = name
		if subtasks is None:
			subtasks = []
		self.subtasks = subtasks

	def new_subtask(self, *args, **kwargs) -> Subtask:
		"""Constructs a new subtask with provided args and kwargs
		Then appends it to own subtask list and returns."""
		subtask = Subtask(*args, **kwargs)
		self.subtasks.append(subtask)
		return subtask

	def get_testcase_count(self) -> int:
		"""Returns number of testcases in this problem."""
		total = 0
		for subtask in self.subtasks:
			total += subtask.get_testcase_count()
		return total

	# TODO: Start generating from some position
	def generate(self) -> tuple:
		"""An iterator which yields (testcase number, [testcases]) for all 
		testcases.
		"""
		offset = 0
		log(f"Generating inputs for problem {self.name}")
		for subtask in self.subtasks:
			log(f"Working on inputs for subtask {subtask.name}")
			for sub_index, testcase in subtask.generate():
				yield (offset + sub_index, testcase)
			offset += subtask.get_testcase_count()
			log(f"^ subtask {subtask.name} done!")
		log(f"Finished generating for problem {self.name}")

	def get_layout(self) -> list:
		"""Returns the testcase layout of the problem.
		In form [ [subtask name, [(start idx, end idx), ...]], ... ]"""

		result = []
		offset = 0
		for subtask in self.subtasks:
			size = subtask.get_testcase_count()
			ranges = [(offset + 1, offset + size)]

			# TODO: Implement subset layout
			if subtask.subsets != []:
				raise NotImplementedError

			result.append((subtask.name, ranges))
			offset += size

		return result

	def testcase_details(self) -> list:
		"""Returns info about all testcases.
		In form [
		  (Subtask,
		    [(case_type, subtask index (idx_low, idx_high), testcase numbers (idx_low, idx)), ...]
		  ), ...
		]"""
		result = []
		offset = 0
		for subtask in self.subtasks:
			layout = subtask.get_layout()
			subtask_result = []
			for case_type, sub_start, sub_end in layout:
				subtask_result.append((case_type, (sub_start, sub_end), (offset + sub_start, offset + sub_end)))
			result.append((subtask, subtask_result))
			offset += subtask.get_testcase_count()
		return result

	def breakdown_str(self) -> str:
		"""Formats .testcase_details() into a string and returns it"""
		details = self.testcase_details()
		result = f"Testcase breakdown\n"
		for subtask, allocations in details:
			result += f"{subtask.name} ({subtask.get_testcase_count()} non-subset testcases):\n"
			# TODO: Implement subset
			for case_type, sub_idx, testcase_idx in allocations:
				result += f"- {case_type}: subtask testcase #{sub_idx[0]}-{sub_idx[1]}"
				result += f", testcase files #{testcase_idx[0]}-{testcase_idx[1]}\n"
		return result.strip()