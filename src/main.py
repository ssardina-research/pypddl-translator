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
import copy

from pypddl.pddlparser import PDDLParser

from pypddl.predicate import Predicate
from pypddl.term      import Term
from pypddl.literal   import Literal
from pypddl.action    import Action
from pypddl.problem import Problem
from pypddl.mtp import multi_tier_compilation_problem, multi_tier_compilation_domain



# just for testing
def test_change_domain(domain):
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

    domain.add_action('pick-up-b', params, precond, [effect, effect])


# just for testing
def test_change_problem(problem):
    problem.add_object('z', 'block')    # add a new block object

    problem.add_to_init('open', ['1', '2'])
    # print(problem.init)

    problem.add_to_goal('open', ['3', '4'])
    # print(problem.goal)


if __name__ == '__main__':
    # usage = 'python main.py <domain> [<problem>]'
    description = 'Parse and translate a planning domain and problem. '
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('domain-problem',
                        nargs = '+',
                        help='path to at least one file, possibly two, encoding the domain and problem')
    parser.add_argument('--print-domain',
                        action='store_true',
                        default=False,
                        help='print the translated PDDL domain (default: %(default)s). True if --out-problem used')
    parser.add_argument('--print-problem',
                        action='store_true',
                        default=False,
                        help='print the translated PDDL problem (default: %(default)s). True if --out-domain used')
    parser.add_argument('--out-domain',
                        default='',
                        help='filename to write the output PDDL domain')
    parser.add_argument('--out-problem',
                        default='',
                        help='filename to write the output PDDL problem')
    parser.add_argument('--test-changes',
                        action='store_true',
                        default=False,
                        help='do some testing changes to domain and problem (default: %(default)s)')
    parser.add_argument('--multi-tier-compilation',
                        action='store_true',
                        default=False,
                        help='translate labeled PDDL to MTD and MTP (default: %(default)s)')

    args = vars(parser.parse_args())    # vars returns a dictionary of the arguments

    if args['out_problem']:
        args['print_problem'] = True
    if args['out_domain']:
        args['print_domain'] = True
    #print(args)  # just print the options that will be used


    # Parse the domain and problem given, build data structures
    domain  = PDDLParser.parse(args['domain-problem'][0])
    # print("==========> Domain parsed into memory....")

    problem = None
    
    # the first file already contained both domain + problem
    # So, extract domain and problem
    if type(domain) is tuple:
        problem = domain[1]
        domain = domain[0]

    # two files have been given: domain and problem, load problem now
    if len(args['domain-problem']) == 2:
        print(args['domain-problem'][1])
        problem = PDDLParser.parse(args['domain-problem'][1])
        # print("==========> Problem parsed into memory....")


    if args['multi_tier_compilation']:
        # We extract the hierarchy from the problem definition just because it is easier
        # and is useful when compiling the domain
        domain_models_hierarchy,goal_statement = multi_tier_compilation_problem(problem,args['out_problem'])
        multi_tier_compilation_domain(domain,domain_models_hierarchy,goal_statement,args['out_domain'])

    # test modifications to domain and problem
    if args['test_changes']:
        test_change_domain(domain)
        test_change_problem(problem)


    if args['print_domain']:
        if not args['out_domain']:
            print('=================================== TRANSLATED PDDL DOMAIN =================================== ')
            print(repr(domain))
            # print(domain)  # Pretty-printing
        else:
            with open(args['out_domain'], 'w') as f:
                print(repr(domain), file=f)

    if args['print_problem'] and not problem == None:
        if not args['out_problem']:
            print('=================================== TRANSLATED PDDL PROBLEM =================================== ')
            print(repr(problem))
            # print(problem)
        else:
            with open(args['out_problem'], 'w') as f:
                print(repr(problem), file=f)
    elif args['print_problem'] and problem == None:
        print("There was no problem found in the files provided")




