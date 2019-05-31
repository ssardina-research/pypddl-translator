# This file is part of pypddl-PDDLParser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.


import argparse

from pddlparser import PDDLParser

from predicate import Predicate
from term      import Term
from literal   import Literal
from action    import Action

# just for testing
def add_to_domain(domain):
    ############################################
    # Let's now create  TYPES AND PREDICATES
    ############################################
    domain.add_type('boxes')
    domain.add_pred('open', [('?x', 'boxes'), ('?z', 'block')])
    domain.del_pred('handempty', 0)

    # print(repr(domain.operators[3]))


    ############################################
    # Let's now create an OPERATOR
    ############################################
    # print(domain.operators[3].precond)
    params = [Term.variable('?x', type='blocks'), Term.variable('?y', type='blocks')]

    precond=[]
    precond.append(Literal(Predicate('=', [Term.variable('?x'), Term.variable('?y')]), False))
    precond.append(Literal(Predicate('on', [Term.variable('?x'), Term.variable('?y')]), True))
    precond.append(Literal(Predicate('clear', [Term.variable('?x')]), True))
    precond.append(Literal(Predicate('handempty', []), True))

    # print(domain.operators[3].effects)
    effect=[]
    effect.append((1.0, Literal(Predicate('holding', [Term.variable('?x')]), True)))
    effect.append((1.0, Literal(Predicate('clear', [Term.variable('?y')]), True)))
    effect.append((1.0, Literal(Predicate('clear', [Term.variable('?x')]), False)))
    effect.append((1.0, Literal(Predicate('handempty', []), False)))
    effect.append((1.0, Literal(Predicate('on', [Term.variable('?x'), Term.variable('?y')]), False)))
    # print(repr(effect))

    domain.add_action('pick-up-b', params, precond, effect)


# just for testing
def add_to_problem(problem):
    problem.add_object('z', 'block')    # add a new block object

    problem.add_to_init('open', ['1', '2'])
    # print(problem.init)

    problem.add_to_goal('open', ['3', '4'])
    # print(problem.goal)



if __name__ == '__main__':
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'pypddl-parser is a PDDL parser built on top of ply.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')

    args = parser.parse_args()

    domain  = PDDLParser.parse(args.domain)
    problem = PDDLParser.parse(args.problem)

    ## Pretty-printing of domain and problem
    # print(domain)
    # print(problem)

    # test modifications to domain and problem
    add_to_domain(domain)
    add_to_problem(problem)

    # print(repr(domain))
    print(repr(problem))