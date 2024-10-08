bt is a flexible, powerful, fast and simple **b**uild **t**ool inspired by Make and spurred by other build tools' inabilities.
Instead of relying on a weird limited DSL, bt exploits the power and familiarity of Python 3.12.

Introducing bt into a project is easy; see the [setup section](#setup).

### Overview
The execution of bt is always accompanied by a **b**uild **s**cript.
bt lets the build script run and define [tasks](#tasks) and do any other setup.
When the build script exits, bt takes over.
It looks at the command line arguments that were passed and sets [parameters](#parameter) and determines which tasks to run.
Before running a task, bt runs all of its [dependencies](#dependencies) which may include tasks and callables.
Since tasks can take long, bt provides facilities for [caching](#cache) them so that they don't have to run every time.

```py
bt.debug = True

options = ["-std=c2x", "-Ofast", parameter("options")]
main = "main"
mainc = main + ".c"

@task(export = False, output = mainc)
def generateSource():
	import textwrap
	with open(mainc, "w") as source: source.write(textwrap.dedent("""
		#include <stdio.h>
		int main() {puts("foo bar");}
	""").strip())

@task(generateSource, default = True, input = options, output = main)
def compile():
	sh(Arguments("gcc -o", main, options, generateSource.outputFiles))

@task(compile)
def run():
	sh("./" + main)
```
```sh
$ bt run
> generateSource
> compile
> run
foo bar

$ bt run
> run
foo bar

$ bt run options="-Oz -flto"
> compile
> run
foo bar

$ bt run options="-Oz -flto"
> run
foo bar
```

### Setup
bt can be [executed directly](#executable) or [imported as a library](#library) by the build script from a subdirectory (a Git submodule for example).
Both methods can be used simultaneously.

#### Executable
The executable is [`__main__.py`](__main__.py); a symbolic link in `PATH` or a shell alias can be used.
The build script has to be in the current directory and named `bs` or `bs.py`.

1. Clone bt: `git clone https://github.com/nnym/bt`.
2. Set up a symbolic link in PATH: `ln -s "$(realpath bt/__main__.py)" ~/.local/bin/bt # or in any other directory in PATH`.
3. With bt set up, make a build script (`bs` or `bs.py`) in a new or existing project directory:
```py
@task
def alfa(): print("bar")
```
4. Run it: `bt alfa # bar`.

For language server support, also [import](#library) bt.

#### Library
The build script—which may be named anything—is the main module and imports bt as a package in the same directory or in `sys.path`.
bt starts when the build script ends.

This option allows bt to be used without environmental setup.

1. Enter a new or existing project directory.
2. a. In a Git repository, add bt as a submodule: `git submodule add https://github.com/nnym/bt`.<br>
   b. Clone bt: `git clone https://github.com/nnym/bt`.
3. Make a build script (here `build.py`):
```py
#!/bin/env python
from bt import *

@task
def quebec(): print("bar")
```
4. Make it executable: `chmod +x build.py`.
5. Run it: `./build.py quebec # bar`.

If the build script is named `bs` or `bs.py` instead, then it additionally can be run by the [executable](#executable).

### Usage
bt takes as arguments names of tasks to run and `name=value` pairs which set [parameters](#parameter) for the build.

### Tasks
Tasks are functions that can be run on demand from the command line or as [dependencies](#dependencies) of other tasks.<br>
A function can be declared a task by using the decorator `@task`. The task's name is the function's name.

[`bt.debug = True`](#debug) is implicit in all of the examples below.

```py
@task
def bravo():
	print("bar")
```
This declares a task `bravo` that prints `"bar"`.
```sh
$ bt bravo
> bravo
bar
```

#### Task arguments
A sequence of command line arguments can be passed to a task by prefixing it by `--`.
The last task in the command line or the [default](#defaults) task that is declared last receives them.
A task can accept or require them as parameters. The arguments must match the task's arity.
Tasks may not have non-default keyword-only parameters.

This task accepts any number of arguments.
```py
@task
def oscar(*args):
	print(args)
```
```sh
$ bt oscar -- foo -- bar
> oscar
('foo', '--', 'bar')
```

This task requires exactly 2 arguments.
```py
@task
def papa(a, b):
	print(a, "|", b)
```
```sh
$ bt papa
Task papa: received 0 arguments instead of 2.
$ bt papa --
Task papa: received 0 arguments instead of 2.
$ bt papa -- foo
Task papa: received 1 argument instead of 2.
$ bt papa -- foo bar baz
Task papa: received 3 arguments instead of 2.

$ bt papa -- foo bar
> papa
foo | bar
```

#### Dependencies
Any non-keyword argument to `task` is considered as a dependency which may be another task or its name or a callable.
Before a task runs, its dependencies run first.

```py
@task
def charlie(): pass

@task(charlie)
def delta(): pass
```
Here `charlie` will always run before `delta`.
```sh
$ bt delta
> charlie
> delta

$ bt delta charlie
> charlie
> delta
```

#### Defaults
`task`'s parameter `default` controls whether the task runs when the command line has not specified any tasks.
```py
@task(default = True)
def echo():
	print("baz")
```
bt automatically runs `echo` when the user has not selected any tasks.
```sh
$ bt
> echo
baz
```

#### Exports
Any task can be run from the command line by default. This can be changed by the option `export`.
```py
@task(default = True, export = False)
def foxtrot():
	print("foo")
```
This will make `foxtrot` run by default but not runnable explicitly.
```sh
$ bt foxtrot
No task matched 'foxtrot'.
```

#### Cache
Inputs and outputs are objects that determine whether a task should be skipped.
Inputs may be anything and outputs are only files.
They can be modified through the options `input` and `output`.

If a task does not have inputs or outputs, then it is never skipped.
A task that has inputs or outputs is skipped only if its inputs have not changed, its outputs all exist, and its dependencies all either are [pure](#pure-tasks) or have been skipped.

Before bt exits, the `input` of every task that ran is written to a cache.
When a task is about to run, its `input` is checked against that in the cache: if they differ, then they have changed and the task runs.

File modification is tracked by mtime. If an input file does not exist, then an error is raised.

#### Input
```py
@task(input = "baz")
def golf(): pass
```
This task will run only once ever: Since `input` has not been cached before the first run, `golf` is run once.
Thereafter whenever the task is about to run, since `input` does not change, it matches the cached version and `golf` is skipped.
Therefore `golf` runs only once.
```sh
$ bt golf
> golf
$ bt golf
```

```py
@task(input = Files("foo"))
def hotel(): pass
```
When this task is called, it runs if this time is the first or `foo`'s mtime changed.
```sh
$ touch foo
$ bt hotel
> hotel
$ bt hotel
$ touch foo
$ bt hotel
> hotel
```

#### Output
bt ensures that the parent directories of all outputs exist.

```py
@task(output = "foo/bar/baz")
def india():
	sh("touch foo/bar/baz")
```
This task will be skipped if `foo/bar/baz` exists.
```sh
$ ls foo
ls: cannot access 'foo': No such file or directory
$ bt india
> india
$ ls foo/bar
baz
$ bt india
```

#### Ignoring the cache
A task can be forced to run by passing as an argument its name suffixed by `!`.
```py
@task(default = True, input = 0)
def juliett(): pass

@task(juliett, input = 0)
def kilo(): pass

@task(kilo, input = 0)
def lima(): pass
```
```sh
$ bt lima
> juliett
> kilo
> lima

$ bt kilo
$ bt kilo!
> kilo
```

Passing `!` forces all initial tasks to run.
```sh
$ bt !
> juliett

$ bt kilo !
> kilo
```

Passing `!` twice forces all required tasks to run.
```sh
$ bt ! !
> juliett

$ bt kilo ! !
> juliett
> kilo
```

#### Pure tasks
Pure tasks act like they don't have side effects: their execution does not prevent tasks that depend on them from being skipped.

```py
@task(pure = True)
def mike(): pass

@task(mike, input = 0)
def november(): pass
```
When `november` is called after the first run, it will be skipped but `mike` will run.
```sh
$ bt november
> mike
> november

$ bt november
> mike
```

#### Name
A task can be given a name different from that of its function by using the option `name`.
```py
for n in range(100):
	@task(name = str(n))
	def romeo():
		n = int(bt.current.name)
		print(f"{n} * {n} = {n * n}")
```
This will generate 100 tasks with the numbers 0-99 as their names.
```sh
$ bt 37
> 37
37 * 37 = 1369
```

### API
[Importing](#library) or [executing](#executable) bt gives a build script direct access to
- module `bt` containing
  - variable [`debug`](#debug)
  - variable [`current`](#current)
- classes
  - [`Arguments`](#arguments)
  - [`Files`](#files)
  - `Task`
- functions
  - [`parameter`](#parameter)
  - [`sh`](#sh)
  - [`task`](#tasks).

If a name is not listed here, then it should be assumed to be internal.

#### `debug`
This flag determines whether to print debugging information. Currently only names of tasks before they run are printed.

#### `current`
This variable stores the task that is currently running.

#### `parameter`
A parameter `name` can be set to `"value"` by passing `name=value` in the command line.

The function `parameter(name, default = None, require = False)` allows the build script to read parameter values.
If the parameter is not set, then
- if `require`, then an error message is printed and the build is terminated
- otherwise `default` is returned.

#### `sh`
bt exports function `sh` for running shell commands.
`sh` forwards its parameters to `subprocess.run` and sets `shell = True` and `text = True` by default.
If the command line is an [`Arguments`](#arguments), then it is converted into a string.
```py
sh("tr ab ba", input = "abr abz")
```

#### `Arguments`
`Arguments` is a `list` derivative that stores a full or partial command line.
It flattens every added `Iterable`. Supported element types are `str` and `Iterable`.
Its string representation joins its elements with spaces.
Its method `split` splits its string representation into a list.
```py
source = ["main.c"]
exe = "foo"
options = ["-Ofast", "-std=c2x"]
sh(Arguments("gcc", source, "-o", exe, options))
```
