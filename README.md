# pypddl-translator

PDDL's domain and problem parser+translator in Python3 using [ply](http://www.dabeaz.com/ply/) library. 

This is an significant extension and refactoring of [pypddl-parser](https://github.com/thiagopbueno/pypddl-parser), by Sebastian Sardina and Alberto Pozanco (2019-2020).


# Features

* Can read PDDL planning domains and problems as one single file, or in two separated files (domain and problem).
* Ability to printout planning domains and problems to console or files.
* Interface to modify planning domains and problems.
* Can handle typed and untyped (if there is only one) objects and parameters.
* Can read labeled PDDL planning domains and problems given in two separated files (domain and problem)
* Can produce MTP domain and problem files from a labeled PDDL planning and problem description

**Planning domains:**

* Supports the ```:requirements :strips, :typing, :equality, :probabilistic-effects```.
* Supports non-deterministic effects via `oneof` keyword.
* Supports relations between types:  `(:types type1 type2 ... typen - type ...)`
* Supports conditional effects via `when` keyword.

**Problems:**

* Planning problems, via keyword  `problem`.
* Labeled domains (labeled effects) for multi-tier planning problems (MTP).

# Install

Please make sure you have the ```ply``` library installed on your system. If you don't have it, you can use pip3 to install it.

```bash 
$ pip3 install ply
```


# Formats

## Planning Domains

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

## Planning Problems

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
    )


## Labeled Planning Domains

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

## Labeled Planning Problems

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

The domain markers (`d3`,`d2`, and `d1` in this example), must appear ordered both in the domain and problem files, i.e., effects (and goals) of higher domain levels are written before effects (and goals) of lower domain levels in order to denote the domain hierarchy (e.g. `d3 > d2 > d1`).


# Examples


Parse a domain and planning problem and print them both on console:

    python3 main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-0.pddl  --print-domain --print-problem


Parse a domain and planning problem and save them into new files:

    python3 main.py pddl/blocksworld/domain.pddl pddl/blocksworld/problems/probBLOCKS-04-0.pddl  \
        ---out-domain new-domain.pddl --out-probem new-problem.pddl


Generate MTP domain and problem from a labeled domain and problem description:

    python3 main.py pddl/mtp-example/labeled-domain.pddl pddl/mtp-example/labeled-problem.pddl --multi-tier-compilation --out-problem mtp-problem.pddl --out-domain mtp-domain.pddl


# License

This translator was developed by Sebastian Sardina (2019) and is basically an extension of [pypddl-parser](https://github.com/thiagopbueno/pypddl-parser), which is under GNU Lesser General Public License as published by the Free Software Foundation.

The extension to MTP was done by Alberto Pozanco and Sebastian Sardina in 2020.

pypddl-translator is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

pypddl-translator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with pypddl-parser. If not, see [http://www.gnu.org/licenses/](http://www.gnu.org/licenses/).
