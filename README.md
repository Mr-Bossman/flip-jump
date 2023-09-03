# FlipJump

[![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/tomhea/flip-jump)](https://github.com/tomhea/flip-jump#project-structure)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/tomhea/flip-jump)](https://github.com/tomhea/flip-jump/releases/latest)
[![GitHub Discussions](https://img.shields.io/github/discussions/tomhea/flip-jump)](https://github.com/tomhea/flip-jump/discussions)
[![GitHub](https://img.shields.io/github/license/tomhea/flip-jump)](LICENSE)
[![Website](https://img.shields.io/website?down_color=red&down_message=down&up_message=up&url=https%3A%2F%2Fesolangs.org%2Fwiki%2FFlipJump)](https://esolangs.org/wiki/FlipJump)

FlipJump is the simplest programing language.<br>
Yet, it can do **any modern computation**.

It's an Esoteric language ([FlipJump esolangs page](https://esolangs.org/wiki/FlipJump)), with just 1 operation `a;b`:  
- `not *a; jump b`

Which means - **Flip** a bit, then **Jump**.

The operation takes 2 memory addresses - it flips (inverts) the bit the first address points to, and jumps to (continue execution from) the second address.  

This project is a **Macro Assembler**, an **Interpreter** and a **Tested Standard Library** to the language.

This calculator was built with only FlipJump ([source](programs/calc.fj)):
![Calculations using only FlipJump](res/calc.gif)

## Hello, World!

A simple fj [hello-world](programs/print_tests/hello_no-stl.fj) program, not using the standard library:

```c
def startup @ code_start > IO  {
    ;code_start
  IO:
    ;0              // the second op is reserved for Input/Output.
  code_start:
}


def output_bit bit < IO {
    IO + bit;       // flipping IO+0 outputs 0; flipping IO+1 outputs 1.
}
def output_char ascii {
    rep(8, i) output_bit ((ascii>>i)&1)
}

def end_loop @ loop_label {
    loop_label:
    ;loop_label     // fj finishes on a self loop
}

    startup
    
    output_char 'H'
    output_char 'e'
    output_char 'l'
    output_char 'l'
    output_char 'o'
    output_char ','
    output_char ' '
    
    output_char 'W'
    output_char 'o'
    output_char 'r'
    output_char 'l'
    output_char 'd'
    output_char '!'
    
    end_loop

```

The FlipJump assembly supports a ```"Hello, World!"``` syntax for initializing a variable with a string value.
Look at the [hello_world.fj](programs/print_tests/hello_world.fj) program for more info.

Note that all of these macros are already implemented in the standard library (all in [runlib.fj](stl/runlib.fj)):
- startup
- end_loop     (loop)
- output_char
- output       (for printing string consts, e.g. output "Hello, World!")

# How to install?

```shell
pip install flipjump
```

You can also install it with its extras:
- **stats:** support for viewing macro usage in an interactive graph.
- **tests:** all the testing libraries needed.
```shell
pip install flipjump[stats,tests]
```


Pycharm Extensions:
- Add <span style="color:orange">syntax highlighting</span> support for *.fj files - just import the [PycharmHighlighting.zip](ide-extensions/pycharm/PycharmHighlighting.zip) settings.
- Add a ctrl+shift+click (find fj-macro definition) functionality by using the [AutoHotKey script](ide-extensions/pycharm/fj-pycharm-def-finder.ahk).

# How to run?

Use the `fj` utility:
```shell
fj hello_world.fj
```

![Hello World in FlipJump](res/hello.gif)

  - The --no-stl flag tells the assembler not to include the standard library. for example: `fj programs/print_tests/hello_no-stl.fj --no-stl`.
  - the -w [WIDTH] flag allows compiling the .fj files to a WIDTH-bits memory width. WIDTH is 64 by default.
  - You can use the -o flag to save the assembled file for later use too.
  - you can find all the different flags with `fj -h`.

You can also **[Test the project](tests/README.md)** with the project's tests, and with your tests.

You can also assemble and run separately:

```bash
fj --asm hello.fj -o hello_world.fjm
fj --run hello_world.fjm
```

- The first line will assemble your code.
- The second line will run your code.

You can also use the faster [cpp-based interpreter](https://github.com/tomhea/fji-cpp):

```bash
>>> fji hello.fjm -s
Hello, World!
```

### How to Debug?
Programs won't work on their first run. They just can't. That's why we support the next debugging flags.

- No debugging flags at all: Shows the last 10 executed addresses of tests that failed their run (i.e. finished not by looping). 
- `-d [PATH]`: Save debug information: Adds [very extensive label names](tests/README.md#example-label-name-youll-get-with-using---debuginfo-len), Which are like a "**macro-stack**" for each of the last executed address. (can be used with `--debug-ops-list LEN`)
- `--debug-ops-list LEN`: Shows the last _LEN_ executed addresses (instead of 10). (can be used with `-d`)
- `-b NAME [NAME ...]`: Places breakpoints at every specified label NAMEs (note that label names are long: [more information about labels](src/flipjump/README.md#generated-label-names)). (requires `-b`)
- `-B NAME [NAME ...]`: Places breakpoints at every label that contains one of the given NAMEs. (requires `-b`)

# Project Structure

**[src](src/flipjump/README.md)** (assembler + interpreter source files):
  - fj.py - the FlipJump Assembler & Interpreter script.
  - fjm.py - read/write .fjm (flip-jump-memory) files.
  - fjm_run.py - interpret / debug assembled fj files.
  - fj_parser.py - pythonic lex/yacc parser.
  - preprocessor.py - unwind all macros and reps.
  - assembler.py - assembles the macro-less fj file.
  - [more...](src/flipjump/README.md)

**[stl](stl/README.md)** (standard library files - macros. [list of all macros](https://esolangs.org/wiki/FlipJump#The_Standard_Library)):
  - runlib.fj - constants and initialization macros. output constant strings.
  - [bit/](stl/README.md#bit) - macros for io/manipulating binary variables and vectors (i.e. numbers).
  - [hex/](stl/README.md#hex) - macros for io/manipulating hexadecimal variables and vectors.
  - mathlib.fj - advanced math macros (mul/div).
  - casting.fj - casting between bit/hex.
  - ptrlib.fj - pointers, stack and functions.
  - conf.json - standard library list file.

**[programs](programs)** (FlipJump programs), for example:
  - [hello_world.fj](programs/print_tests/hello_world.fj) - prints hello world :)
  - [calc.fj](programs/calc.fj) - command line calculator for 2 hex/dec numbers: ```a [+-*/%] b```.
  - [func_tests/](programs/func_tests) - performs function calls and operations on stack.
  - [hexlib_tests/](programs/hexlib_tests) - tests for the macros in stl/hexlib.fj.
  - [quine16.fj](programs/quine16.fj) - a 16-bits quine by [lestrozi](https://github.com/lestrozi); when assembled with `-w16 -v0` - prints itself.
  - [pair_ns.fj](programs/concept_checks/pair_ns.fj) - simulating the concept of a Class using a namespace.
  - [print_dec.fj](programs/print_tests/print_dec.fj) - prints binary variables as decimals.
  - [multi_comp/](programs/multi_comp) - simulates a big project (compilation of multiple files).

**[tests](tests/README.md)** (FlipJump programs), for example:
  - compiled/   - the designated directory for the assembled tests files.
  - inout/      - .in and .out files for each test in the folder above.
  - conftest.py - pytest configuration file.
  - test_fj.py  - tests for compilation and running ([how to run](tests/README.md#run-the-tests)).
  - test_compile_*.csv  - all compilation tests arguments ([compile test format](tests/README.md#compile-csvs-format)).
  - test_run_*.csv      - all running tests arguments ([run test format](tests/README.md#run-csvs-format)).
  - conf.json   - tests list file.


# Read More

A very extensive explanation can be found on the [GitHub wiki page](https://github.com/tomhea/flip-jump/wiki/Learn-FlipJump).

More detailed explanation and the **specifications of the FlipJump assembly** can be found on the [FlipJump esolangs page](https://esolangs.org/wiki/FlipJump).

Read more about the [flip-jump source files](src/flipjump/README.md) and [how to run the tests](tests/README.md). 

If you want to contribute to this project, read the [CONTRIBUTING.md](CONTRIBUTING.md) file, and take a look at the [Discussions](https://github.com/tomhea/flip-jump/discussions/148).

If you are new to FlipJump and you want to learn how modern computation can be executed using FlipJump, Start by reading the [bit/math.fj](stl/bit/math.fj) standard library file (start with `xor`, `if`). That's where the FlipJump magic begins.

You can also write and run programs for yourself! It is just [that](README.md#how-to-run) easy :)

