# pypddl-translator

## Archived, now using pddl parser: https://github.com/AI-Planning/pddl


PDDL's domain and problem parser+translator in Python3 using [ply](http://www.dabeaz.com/ply/) library.

This is an significant extension and refactoring of [pypddl-parser](https://github.com/thiagopbueno/pypddl-parser), by Sebastian Sardina and Alberto Pozanco (2019-2020).

## Features

* Can read PDDL planning domains and problems as one single file, or in two separated files (domain and problem).
* Ability to printout planning domains and problems to console or files.
* Interface to modify planning domains and problems.
* Can handle typed and un-typed (if there is only one) objects and parameters.
* Can read labeled PDDL planning domains and problems given in two separated files (domain and problem)
* Can produce MTP domain and problem files from a labeled PDDL planning and problem description

**Planning domains:**

* Supports ```:requirements :strips, :typing, :equality, :probabilistic-effects```.
* Relations between types:  `(:types type1 type2 ... typen - type ...)`
* Non-deterministic effects via `oneof` (arbitrary form).
* Conditional effects via `when` keyword.
* Labelled effects (used in MTP to label `oneof`).

**Problems:**

* Planning problems, via keyword  `problem`.
* Labeled `oneof` goals (used in MTP).

## Setup

Please make sure you have the [`ply` library](https://www.dabeaz.com/ply/) installed on your system to perform parsing.

```shell
$ pip install ply
```

We can install the system as an [editable project](https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/#working-in-development-mode) `pypddl`:

```
$ pip install -e .  # install as editable project as per setup.py
```

Effectively this adds the folder to `sys.path` variable which is used by Python to search for modules. This means you can now use/run the planner from anywhere, as it is installed as a packge, and any change in the source of the planner will be seen automatically.

We can then run the system from everyone via `-m pypddl.main` as follows:

```shell
python -m pypddl.main -h
usage: main.py [-h] [--print-domain] [--print-problem] [--out-domain OUT_DOMAIN] [--out-problem OUT_PROBLEM]
               [--test-changes] [--multi-tier-compilation]
               domain-problem [domain-problem ...]

Parse and translate a planning domain and problem.
```

We can also check the package is installed:

```shell
$ pip show pypddl
Name: pypddl
Version: 1.5
Summary: A parser and translator of PDDL files
Home-page: https://github.com/ssardina-planning/pypddl-translator
Author: Sebastian Sardina
Author-email: ssardina@gmail.com
License: UNKNOWN
Location: /mnt/ssardina-research/nitinseb/pypddl-translator.git/src
Requires: ply
Required-by: 
```

To uninstall the system:  `pip uninstall pypddl`

## Usage examples

Parse a domain and planning problem and print them both on console (this test file contains rich nested constructs):

```shell
$ python src/pypddl/main.py pddl/test/domain.pddl pddl/test/problems/probBLOCKS-04-0.pddl  --print-domain --print-problem
```

If the system was installed as an editable package (see above):

```shell
$ python -m pypddl.main pddl/test/domain.pddl pddl/test/problems/probBLOCKS-04-0.pddl  --print-domain --print-problem
```

Parse a domain and planning problem and save them into new files:

```shell
$ python src/pypddl/main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-0.pddl  \
    --out-domain new-domain.pddl --out-problem new-problem.pddl
```

Generate MTP domain and problem from a labeled domain and problem description:

```shell
$ python src/pypddl/main.py pddl/mtp-example/labeled-domain.pddl pddl/mtp-example/labeled-problem.pddl --multi-tier-compilation --out-problem mtp-problem.pddl --out-domain mtp-domain.pddl
```

### Unit testing

Uses package [unittest](https://docs.python.org/3/library/unittest.html):

```shell
$ python -m unittest src/pypddl/unit_tests.py
```


## Formats

### Planning Domains

```
(define (domain blocksworld)
    (:requirements :strips)
(:predicates (clear ?x)
                (on-table ?x)
                (arm-empty)
                (holding ?x)
                (on ?x ?y)
            (ftrue))
    
(:action pickup
    :parameters (?ob)
    :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
    :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob)) 
                (not (arm-empty))))

(:action putdown
    :parameters  (?ob)
    :precondition (and (holding ?ob))
    :effect (and (clear ?ob) (arm-empty) (on-table ?ob) 
                (not (holding ?ob))))

(:action stack
    :parameters  (?ob ?underob)
    :precondition (and (clear ?underob) (holding ?ob))
    :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
                (not (clear ?underob)) (not (holding ?ob))))

(:action unstack
    :parameters  (?ob ?underob)
    :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
    :effect (and (holding ?ob) (clear ?underob)
                (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty))))

)
```

### Planning Problems

```
(define (problem test)
    (:domain blocksworld)
    (:objects b1 b2 )
    (:init
        (arm-empty)
        (on b1 b2)
        (on-table b2)
        (clear b1)
        (ftrue)
    )
    (:goal (and (clear b1) (clear b2) ) )
    ; (:goal (clear b1) (clear b2) ) ; also legal
)
```

The goal can also not mention the `and` and just list the literals.


### Labeled Planning Domains

Here non-deterministic `oneof` effects may be labelled with a name.

```
(define (domain no_running_1)

(:requirements
    :typing
)

(:types Cell)

(:constants
    c0 c1 c2 - Cell
)

(:predicates
    (at ?c - Cell)
    (adj ?o - Cell ?d - Cell)
    (broken)
    (scratch)
)

(:action walk
:parameters (?o - Cell ?d - Cell)
:precondition (and
(at ?o)
(adj ?o ?d)
(not (broken))
)
:effect (oneof

(d3
    (and 
    (not (at ?o))
    (at ?d)
    )
)

(d2
    (and 
    (not (at ?o))
    (at ?d)
    (scratch)
    )
)

(d1
    (and 
    (scratch)
    )
)
)
)

(:action run
:parameters ()
:precondition (and
(at c2)
(not (broken))
)
:effect (oneof

(d3
    (and 
    (not (at c2))
    (at c0)
    )
)

(d2
    (and 
    (not (at c2))
    (at c0)
    (scratch)
    )
)

(d1
    (and 
    (broken)
    )
)
)
)
)
```

### Labeled Planning Problems

Here disjunct goals via `oneof` may be labelled with names.

```
(define (problem p1)
(:domain no_running_1)
(:init 
    (at c2)
    (adj  c2 c1)
    (adj  c1 c0)
    (adj c0 c1)
    (adj c1 c2)
)
(:goal (oneof
    (d3 (and (at c0) (not (scratch)) (not (broken))))
    (d2 (and (at c0) (not (broken))))
    (d1 (and (at c2) (not (broken))))
)
)
)
```

The domain markers (`d3`,`d2`, and `d1` in this example), must appear ordered both in the domain and problem files, i.e., effects (and goals) of higher domain levels are written before effects (and goals) of lower domain levels in order to denote the domain hierarchy (e.g. `d3 > d2 > d1`).


## License

This translator was developed by Sebastian Sardina (2019) and is basically an extension of [pypddl-parser](https://github.com/thiagopbueno/pypddl-parser), which is under GNU Lesser General Public License as published by the Free Software Foundation.

The extension to MTP was done by Alberto Pozanco and Sebastian Sardina in 2020.

`pypddl-translator` is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

`pypddl-translator` is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with `pypddl-parser`. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
