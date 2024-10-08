import functools
import importlib
import inspect
import itertools
import os
import pickle
import re
import shlex
import subprocess
import sys
import threading
import time
import traceback
from collections.abc import Iterable, Iterator, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from os import path
from subprocess import CompletedProcess
from typing import Any, Callable, Optional, Self

f = inspect.currentframe()

if [f for f in inspect.getouterframes(f) if (co := f.frame.f_code).co_code[i := f.frame.f_lasti] in [0x6b, 0x6c]]:
	if "__main__" in co.co_names[co.co_code[i + 1]]:
		line = max(l[2] for l in f.f_code.co_lines() if l[2])
		trace0 = sys.gettrace()

		def trace(frame, event, a):
			if event == "line":
				import warnings

				sys.settrace(trace0)

				with warnings.catch_warnings():
					warnings.filterwarnings("ignore", message = r"assigning None to \d+ unbound locals")
					frame.f_lineno = line

		f.f_trace = trace
		f.f_trace_lines = True
		sys.settrace(trace)

__version__ = 1
assert __name__ == "bt", f'bt\'s module name is "{__name__}" instead of "bt"'
bt = sys.modules["bt"]

Runnable = Callable[[], Any]

class State(Enum):
	NORMAL = 0
	RUNNING = 1
	DONE = 2
	SKIPPED = 3

class FlatList(list):
	@staticmethod
	def isIterable(x): return isinstance(x, Iterable) and not isinstance(x, str)

	def transform(this, x):
		return x

	def copy(this):
		copy = type(this)()
		copy += this
		return copy

	def append(this, x):
		if x := this.transform(x):
			if this.isIterable(x): this.extend(x)
			elif x: super().append(x)

	def insert(this, i, x):
		if x := this.transform(x):
			if this.isIterable(x): this[i:i] = x
			elif x: super().insert(i, x)

	def extend(this, x):
		if x := this.transform(x):
			assert this.isIterable(x), f"{x!r} is a string or not iterable."
			super().extend(x)
		return this

	def __setitem__(this, i, x):
		if x := this.transform(x):
			if isinstance(x, Iterable):
				if not isinstance(i, slice): i = slice(i, i + 1)
				if isinstance(x, str): x = [x]

			super().__setitem__(i, x)

	def __iadd__(this, x):
		return this.extend(x)

	def __add__(this, x):
		return this.copy().extend(x)

class Arguments(FlatList):
	def __init__(this, *arguments):
		for arg in arguments: this.append(arg)

	def set(this, *arguments): this[:] = Arguments(arguments)

	def transform(this, args):
		if isinstance(args, str): return args.strip()
		if isinstance(args, Arguments): return args
		if isinstance(args, Iterable): return Arguments(*args)
		if args: raise TypeError(f"{args!r} is not iterable or a string")

	def split(this): return shlex.split(str(this))

	def __str__(this): return " ".join(this)

@dataclass
class Files:
	def __init__(this, *files):
		this.files = {}

		def flatten(f):
			if isinstance(f, str): this.files[f] = None
			elif isinstance(f, Mapping): flatten(f.values())
			elif isinstance(f, Iterable):
				for e in f: flatten(e)
			elif callable(f): flatten(f())
			else: raise AssertionError(f"{output!r} cannot be converted to a file (is not a string, a list, or callable).")

		flatten(files)

	def __iter__(this): return iter(this.files)

	def __repr__(this): return f"Files({", ".join(this.files)})"

class Task:
	def __init__(this, task: Runnable, dependencies: list[Self], options: dict[str, object]):
		vars(this).update(options)
		this.name0 = this.name
		this.setFunction(task)
		this.dependencies = dependencies
		this.state = State.NORMAL
		this.force = False
		this.args = []
		this.inputFiles = []
		this.outputFiles = []

	def setFunction(this, fn):
		this.fn = fn
		this.spec = inspect.getfullargspec(fn)
		if this.name0 is None: this.name = getattr(fn, "__name__", f"<{len(tasks)}>")
		
	def __call__(this, *args, **kw):
		if started: return this.fn(*args, *this.args[len(args):], **kw)

		del tasks[this.name]
		this.dependencies.insert(0, this.fn)
		this.setFunction(args[0])
		tasks[this.name] = this

		return this

	for state in State:
		vars()[state.name.lower()] = property(functools.partial(lambda this, state: this.state == state, state = state))

Output = str | Files
Output |= Iterable[Output]

def first[A](iterator: Iterator[A]) -> Optional[A]:
	return next(iterator, None)

def group[A, B](iterable: Iterable[A], key: Callable[[A], B]) -> dict[list[B]]:
	return {it[0]: list(it[1]) for it in itertools.groupby(sorted(iterable, key = key), key)}

def findTask(task: str | Runnable | Task, error = True, command = False) -> Optional[Task]:
	if callable(task): return task

	if (match := tasks.get(task, None)) and (match.export or not command):
		return match

	if task[-1:] == "!" and (match := tasks.get(task[:-1], None)) and (match.export or not command):
		match.force = True
		return match

	if error: exit(print(f'No task matched {task!r}.'))

def registerTask(fn: Runnable, dependencies: Iterable, options):
	task = Task(fn, [findTask(d) for d in dependencies], options)
	tasks[task.name] = task
	return task

def require(version: int):
	if __version__ < version: exit(print(f"bt is version {__version__} but version {version} or newer is required."))

def task(*dependencies: str | Task | Runnable, name: str = None, default = False, export = True, pure = False, input: Optional[Any] = None, output: Output = []):
	"""Declare a task named `name` to be run at most once from the command line or as a dependency.
	Ensure that each dependency runs before the task.

	If `default`, then run it when no tasks are specified in the command line.
	If `export`, then make it available in the command line.
	If `pure`, then allow dependent tasks to be skipped even if this task runs.
	If `input` is not `None` or `output` is not empty, then enable caching.
	`input` may be any object and `output` must be a path string or an `Iterable` of path strings.
	If `input` is or contains—directly or indirectly—a routine (as determined by `inspect.isroutine`),
	then replace it by its result just before running the task.

	Skip the task if
	- caching is enabled
	- no task dependency runs
	- `input` and the mtimes of the `Files` in it are the same values from the task's previous run
	- and all outputs exist."""

	options = locals().copy()
	del options["dependencies"]

	if dependencies and callable(dependencies[0]) and not isinstance(dependencies[0], Task):
		return registerTask(dependencies[0], dependencies[1:], options)

	return lambda fn: registerTask(fn, dependencies, options)

def parameter(name: str, default = None, require = False):
	"""Return the value of the parameter `name` if it's set or else `default`.
	If it's unset and not `require`, then print an error message and exit."""

	assert isinstance(name, str), f"Parameter name ({name!r}) must be a string."
	value = parameters.get(name, default)
	if not value and require: exit(print(f'Parameter "{name}" must be set.'))
	return value

def sh(*commandLine: Optional[str | Arguments | Iterable], shell = True, text = True, **kwargs) -> CompletedProcess[str]:
	"""Wrap `subprocess.run` with the defaults `shell = True` and `text = True`.
	Convert `commandLine` into an `Arguments` and then a string."""
	return subprocess.run(str(Arguments(commandLine)), shell = shell, text = text, **kwargs)

def shout(*args, capture_output = True, **kwargs) -> str:
	"Wrap `sh` with `capture_output = True` and return the command's `stdout`."
	return sh(*args, capture_output = capture_output, **kwargs).stdout

def main():
	global started
	started = True
	erred = False

	def error(task: Optional[Task], message: str = None):
		nonlocal erred
		erred = not print(f"Task {task.name}: {message}." if message else task)

	for task in tasks.values():
		if not isinstance(task.default, bool): error(task, f"default ({task.default!r}) is not a bool")
		if not isinstance(task.export, bool): error(task, f"export ({task.export!r}) is not a bool")
		if len(task.spec.kwonlyargs or []) != len(task.spec.kwonlydefaults or []): error(task, f"can't run with a non-default keyword-only parameter")

	initialTasks = [findTask(task, command = True) or task for task in cmdTasks] or [task for task in tasks.values() if task.default]
	if initialTasks: initialTasks[-1].args = args

	for task in initialTasks:
		arity = len(task.spec.args)
		min = arity - len(task.spec.defaults or [])
		count = len(task.args)

		if count < min or count > arity and not task.spec.varargs:
			error(task, f"received {count} argument{["s", ""][count == 1]} instead of {arity if min == arity else f"{min}-{arity}"}")

	if [not error(f'"{task}" does not match an exported task') for task in initialTasks if isinstance(task, str)]:
		print("Exported tasks are listed below.", *(name for name, task in tasks.items() if isinstance(name, str)), sep = "\n")

	if erred: return

	cache = {}

	if path.exists(CACHE):
		with open(CACHE, "br") as file:
			try:
				c = pickle.load(file)
				assert isinstance(c, Mapping)
				cache = c
			except Exception as e:
				print(CACHE + " is corrupt.")
				print(e)

	linesWritten = 0

	def run(task: Task, parent: Task = None, initial = False):
		if task.running: error(f'Circular dependency detected between tasks "{parent.name}" and "{task.name}".')
		if not task.normal: return

		task.state = State.RUNNING
		skip = True

		for dependency in task.dependencies:
			if isinstance(dependency, Task):
				if dependency.done and not dependency.pure: skip = False
				run(dependency, task)
			else: dependency()

		global current
		current = task

		if task.input:
			def flatten(inputs):
				if inspect.isroutine(inputs): inputs = inputs()

				if isinstance(inputs, Files): task.inputFiles.extend(inputs.files)
				elif isinstance(inputs, Mapping): inputs = list(inputs.values())
				elif isinstance(inputs, Iterable) and not isinstance(inputs, Sequence): inputs = list(inputs)

				if isinstance(inputs, Sequence) and not isinstance(inputs, str):
					for i, input in enumerate(inputs):
						inputs[i] = flatten(input)

				return inputs

			task.input = [flatten(task.input or 0), [os.path.getmtime(input) for input in task.inputFiles]]

		if task.output:
			def flatten(output):
				if isinstance(output, str): task.outputFiles.append(output)
				elif isinstance(output, Mapping): flatten(output.values())
				elif isinstance(output, Iterable):
					for o in output: flatten(o)
				elif callable(output): flatten(output())
				else: error(task, f"{output!r} is not a file (a string, iterable, or callable)")

			flatten(task.output)

		if [not error(task, f'input file "{input}" does not exist') for input in task.inputFiles if not path.exists(input)]:
			exit()

		if (skip and not (task.force or force == 1 and initial or force >= 2) and task.input == cache.get(task.name, None)
		and (task.input != None or task.outputFiles) and all(path.exists(output) for output in task.outputFiles)):
			task.state = State.SKIPPED
			return

		for directory in {path.dirname(path.abspath(output)) for output in task.outputFiles}:
			os.makedirs(directory, exist_ok = True)

		nonlocal linesWritten

		if debug:
			if linesWritten > 1: print()
			print(">", task.name)

		linesWritten = 0

		def redirect(stream):
			write0 = stream.write

			def write(s):
				nonlocal linesWritten
				linesWritten += s.count("\n")
				write0(s)

			stream.write = write
			return write0

		write10, write20 = redirect(sys.stdout), redirect(sys.stderr)
		try: task()
		finally: sys.stdout.write, sys.stderr.write = write10, write20

		task.state = State.DONE

	for task in initialTasks: run(task, initial = True)

	cache.update((task.name, task.input) for task in tasks.values() if task.done)

	with open(CACHE, "bw") as file:
		pickle.dump(cache, file)

exports = bt, Arguments, Files, Task, parameter, require, sh, shout, task
__all__ = [o.__name__ for o in exports]
exports = {export.__name__: export for export in exports}

CACHE = ".bt"

debug = False
tasks: dict[str, Task] = {}
current: Task = None

started = False

args0 = sys.argv[1:]

if "--" in args0 and ~(split := args0.index("--")):
	args0, args = args0[:split], args0[split + 1:]
else: args = []

args1 = group((arg for arg in args0 if arg != "!"), lambda a: "=" in a)
cmdTasks = args1.get(False, [])
parameters = args1.get(True, []) 
parameters: dict[str, str] = dict(arg.split("=", 2) for arg in parameters)
force = len(args0) - len(args1)

mainPath = path.realpath(sys.argv[0])
mainDirectory = path.dirname(mainPath)

if "MAIN" in globals():
	if entry := first(entry for entry in ["bs", "bs.py"] if path.exists(entry)):
		entry = path.abspath(entry)
		with open(entry) as source: script = compile(source.read(), entry, "exec")

		try: exec(script, exports)
		except Exception as e:
			tb = e.__traceback__
			while tb and tb.tb_frame.f_code.co_filename != entry: tb = tb.tb_next
			if tb: e.__traceback__ = tb
			exit(traceback.print_exc())
	else: exit(print("No build script (bs or bs.py) was found."))

	main()
else:
	os.chdir(mainDirectory)
	caller = threading.current_thread()
	thread = threading.Thread(target = lambda: (caller.join(), main()), daemon = False)
	thread.start()
	hook, threading.excepthook = threading.excepthook, lambda args: thread._stop() if args.thread == caller else hook(args)

pass