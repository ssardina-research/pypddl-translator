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

import itertools

from predicate import Predicate
from term      import Term


class Problem(object):

    def __init__(self, name, domain, objects, init, goal):
        """

        :param name: string name of the planning problem (e.g., 'BLOCKS-4-1')
        :param domain: string name of the planning domain (e.g., 'blocks')
        :param objects: dictionary, from type --> object names (e.g., {'block': ['d', 'b'], 'door': ['h']})
        :param init: a list of Predicate objects
        :param goal: list of Literal objects
        """
        self._name = name
        self._domain = domain
        self._objects = {}
        for obj in objects:
            self._objects[obj.type] = self._objects.get(obj.type, [])
            self._objects[obj.type].append(str(obj.value))
        self._init = init
        self._goal = goal

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def objects(self):
        return self._objects.copy()

    @property
    def init(self):
        return self._init.copy()

    @property
    def goal(self):
        return self._goal.copy()

    def __str__(self):
        problem_str  = '@ Problem: {0}\n'.format(self._name)
        problem_str += '>> domain: {0}\n'.format(self._domain)
        problem_str += '>> objects:\n'
        for type, objects in self._objects.items():
            problem_str += '{0} -> {1}\n'.format(type, ', '.join(sorted(objects)))
        problem_str += '>> init:\n{0}\n'.format(', '.join(sorted(map(str, self._init))))
        problem_str += '>> goal:\n{0}\n'.format(', '.join(sorted(map(str, self._goal))))
        return problem_str

    def __repr__(self):
        pddl_str = '(define (problem {problem_name})\n' \
                   '\t(:domain {domain})\n' \
                   '\t(:objects {objects})\n' \
                   '\t(:init\n' \
                   '\t\t{init})\n' \
                   '\t(:goal (and \n' \
                   '\t\t{goal}))\n' \
                   ')'. \
            format(problem_name=self._name,
                   domain=self._domain,
                   objects=' '.join('{} - {}'.format(x[1], x[0]) for x in
                                    [(o, self._objects[o][i]) for o in self._objects for i in
                                     range(len(self._objects[o]))]),
                   init= '\n\t\t'.join(repr(pred) for pred in self._init),
                   goal = '\n\t\t'.join(repr(pred) for pred in self.goal)
        )

        return pddl_str


    def add_object(self, name_obj, type_obj):
        if type_obj in self._objects:
            self._objects[type_obj].append(name_obj)
        else:
            self._objects[type] = [name_obj]


    def add_to_init(self, pred):
        self._init.append(pred)


   # problem.add_to_init('open', ['1', '2', 'c'])
    def add_to_init(self, name, constants_args):
        args2 = []
        for a in constants_args:
            args2.append(Term(value=a))
        self._init.append(Predicate(name, args2))


   # problem.add_to_init('open', ['1', '2', 'c'])
    def add_to_goal(self, name, constants_args):
        args2 = []
        for a in constants_args:
            args2.append(Term(value=a))
        self._goal.append(Predicate(name, args2))
