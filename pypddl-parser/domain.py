# This file is part of pypddl-parser.

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


from predicate import Predicate
from term      import Term
from literal   import Literal
from action    import Action


class Domain(object):

    def __init__(self, name, requirements, types, predicates, operators):
        """

        :param name: string name of the domain (e.g., blocks)
        :param requirements: list of domain requirement strings (e.g., [':strips', ':typing', ':equality'])
        :param types: list of types in the domain (e.g., ['block', 'box'])
        :param predicates: list of Predicate objects
        :param operators: list of Action objects
        """
        self._name = name
        self._requirements = requirements
        self._types = types
        self._predicates = predicates
        self._operators = operators

    @property
    def name(self):
        return self._name

    @property
    def requirements(self):
        return self._requirements[:]

    @property
    def types(self):
        return self._types[:]

    @property
    def predicates(self):
        return self._predicates[:]

    @property
    def operators(self):
        return self._operators[:]

    def __str__(self):
        domain_str  = '@ Domain: {0}\n'.format(self._name)
        domain_str += '>> requirements: {0}\n'.format(', '.join(self._requirements))
        domain_str += '>> types: {0}\n'.format(', '.join(self._types))
        domain_str += '>> predicates: {0}\n'.format(', '.join(map(str, self._predicates)))
        domain_str += '>> operators:\n    {0}\n'.format(
            '\n    '.join(str(op).replace('\n', '\n    ') for op in self._operators))
        return domain_str

    def __repr__(self):
        pddl_str =  '(define (domain {domain_name})\n' \
                    '\t(:requirements {requirements})\n' \
                    '\t(:types {types})\n' \
                    '\t(:predicates\n' \
                    '\t\t{predicates}\n' \
                    '\t)\n' \
                    '{actions}\n' \
                    ')'.\
            format(domain_name = self._name,
                   requirements =' '.join(self._requirements),
                   types =' '.join(self._types),
                   predicates = '\n\t\t'.join(repr(pred) for pred in self._predicates),
                   actions = '\n'.join(repr(act) for act in self._operators)
                   )

        return pddl_str


    def add_type(self, type):
        self._types.append(type)
    def del_type(self, type):
        self._types.remove(type)


    def add_pred(self, pred):
        self._predicates.append(pred)

    # domain.add_pred('open', [('?x', 'boxes'), ('y', 'block'))
    def add_pred(self, name, args):
        args2 = []
        for a in args:
            if type(a) is tuple:    # name of variable with type
                arg = Term(name=a[0], type=a[1])
            elif type(a) is str:    # a constant value
                arg = Term(value=a[0])
            else:
                print('ERROR: something went wrong, incorrect argument for predicate {}'.format(name))
            args2.append(arg)
        self._predicates.append(Predicate(name, args2))

    # domain.del_pred('handempty', 0)
    def del_pred(self, name, arity):
        for pred in self._predicates:
            if pred.name == name and len(pred.args) == arity:
                self._predicates.remove(pred)



    def add_action(self, action):
        self._operators.append(action)

    def add_action(self, name, params, precond, effects):
        self._operators.append(Action(name, params, precond, effects)
)