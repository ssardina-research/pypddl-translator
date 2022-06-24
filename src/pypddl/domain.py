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


from pypddl.predicate import Predicate
from pypddl.term      import Term
from pypddl.literal   import Literal
from pypddl.action    import Action


class Domain(object):

    def __init__(self, name, requirements, types, constants, predicates, operators):
        """

        :param name: string name of the domain (e.g., blocks)
        :param requirements: list of domain requirement strings (e.g., [':strips', ':typing', ':equality'])
        :param types: dictionary from types to types ("" for non-typed types)
        :param constants: dictionary from types to list constants ("" for non-typed constants)
        :param predicates: list of Predicate objects
        :param operators: list of Action objects
        """
        self._name = name
        self._requirements = requirements
        self._types = types
        self._constants = constants
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
    def constants(self):
        return self._constants[:]

    @property
    def predicates(self):
        return self._predicates[:]

    @property
    def operators(self):
        return self._operators[:]

    @requirements.setter
    def requirements(self, requirements):
        self._requirements = requirements

    @predicates.setter
    def predicates(self, predicates):
        self._predicates = predicates

    @constants.setter
    def constants(self, constants):
        self._constants = constants

    @types.setter
    def types(self, types):
        self._types = types

    @operators.setter
    def operators(self, operators):
        self._operators = operators

    def __str__(self):
        domain_str  = '@ Domain: {0}\n'.format(self._name)
        if self._requirements is not None:
            domain_str += '>> requirements: {0}\n'.format(', '.join(self._requirements))
        domain_str += '>> types: {0}\n'.format(', '.join(self._types))
        domain_str += '>> predicates: {0}\n'.format(', '.join(map(str, self._predicates)))
        domain_str += '>> operators:\n    {0}\n'.format(
            '\n    '.join(str(op).replace('\n', '\n    ') for op in self._operators))
        return domain_str

    def __repr__(self):
        pddl_str = f'(define (domain {self._name})\n'

        if self._requirements is not None:
            requirements = ' '.join(self._requirements)
            pddl_str += f'\t(:requirements {requirements})\n'


        if len(self._types):    # if there are some :types defined
            types_txt = ' '.join(
                '\t\t{} - {}\n'.format(' '.join(self._types[t]), t) for t in self._types.keys() if not t == '')

            if '' in self._types.keys():    # the case of types without subtypes
                types_txt = '\t\t{} {}\n'.format(types_txt, ' '.join(t for t in self._types['']))

            pddl_str += f'\t(:types \n{types_txt}\t)\n'

        if len(self._constants):    # there are :constants defined
            constants_txt = ' '.join(
                '\t\t{} - {}\n'.format(' '.join(self._constants[t]), t) for t in self._constants.keys() if not t == '')

            if '' in self._constants.keys():
                constants_txt = '\t\t{} {}\n'.format(constants_txt, ' '.join(t for t in self._constants['']))

            pddl_str += f'\t(:constants \n{constants_txt}\t)\n'


        predicates = '\n\t\t'.join(repr(pred) for pred in self._predicates)
        pddl_str += f'\t(:predicates\n \t\t{predicates}\n\t)\n'

        actions='\n'.join(repr(act) for act in self._operators)
        pddl_str += f'{actions}\n'

        pddl_str += f')'

        return pddl_str

    def add_type(self, type, type_type=''):
        if type_type in self._types:
            self._types[type_type].append(type)
        else:
            self._types[type_type] = [type]
    def del_type(self, type_type=''):
        if type_type in self._types:
            self._types[type_type].remove(type)


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