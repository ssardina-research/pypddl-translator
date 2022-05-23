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


class Action(object):

    def __init__(self, name, params, precond, effects):
        """

        :param name: name of the operator (e.g., 'pick-up')
        :param params:  list of Term objects (e.g., '?x' of type 'blocks')
        :param precond: list of Literals objects
        :param effects: list of Literals objects
        """
        self._name    = name
        self._params  = params
        self._precond = precond
        self._effects = effects

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params[:]

    @property
    def precond(self):
        return self._precond[:]

    @property
    def effects(self):
        return self._effects[:]

    @precond.setter
    def precond(self, precond):
        self._precond = precond

    def __str__(self):
        operator_str  = '{0}({1})\n'.format(self._name, ', '.join(map(str, self._params)))
        operator_str += '>> precond: {0}\n'.format(', '.join(map(str, self._precond)))
        operator_str += '>> effects: {0}\n'.format(', '.join(map(str, self._effects)))
        return operator_str

 
    @staticmethod
    def __effect_to_str(effect):
        # print(effect)
        if isinstance(effect, list):    # list of effects: and them all
            if len(effect) > 1:
                return '(and {})'.format(' '.join(Action.__effect_to_str(x) for x in effect))
            else:
                return ' '.join(Action.__effect_to_str(x) for x in effect)
        elif isinstance(effect, tuple) and isinstance(effect[0], float):    # probabilistic atomic (1.0, literal)
            return repr(effect[1])  # representation of the literal
        elif isinstance(effect, tuple) and isinstance(effect[0], str):    # typed effect: when, oneof, labeled
            if effect[0] == "when":
                return f'(when {Action.__effect_to_str(effect[1])}) {Action.__effect_to_str(effect[2])})'
            if effect[0] == "oneof":
                return '(oneof {})'.format(' '.join(Action.__effect_to_str(x) for x in effect[1]))
            if effect[0] == "label":
                return f'({effect[1]} {Action.__effect_to_str(effect[2])})'
            else:
                print(f"This is a tuple with first argument str but cannot recognise type of first element: {effect[0]}")
        else:
            print("Something very wrong, an effect is empty...")



    def __repr__(self):
        # First compute effect string - self.effects is a list
        # print(self._effects)
        effect_str = Action.__effect_to_str(self._effects)
        # print(effect_str)
        # print("====================")
        
        
        # if isinstance(self._effects[0], list): # if only element in list is a list then it is oneof (...) 
        #     effect_str = Action.__det_effect_to_str(self._effects[0])
        # elif len(self._effects) == 1 and isinstance(self.effects[0][0][0][0], str): # Labeled effects
        #     effect_str = '(oneof {})'.format(' '.join(Action.__det_effect_to_str(x) for x in self._effects[0]))
        # elif len(self._effects) > 1:
        #     effect_str = '(oneof {})'.format(' '.join(Action.__det_effect_to_str(x) for x in self._effects))

        # Second compute precondition string
        def_precond = ''
        for p in self._precond:
            if not isinstance(p,list):
                def_precond += ' ' + repr(p)
            else:
                def_precond += ' (or {})'.format(' '.join(repr(x) for x in p))

        operator_str  = '\t(:action {name} \n' \
                        '\t\t:parameters ({param})\n' \
                        '\t\t:precondition (and {prec})\n' \
                        '\t\t:effect {effect}\n' \
                        '\t)'.\
            format(name = self._name,
                   param = ' '.join(repr(p) for p in self._params),
                   prec = def_precond,
                   #prec = ' '.join(repr(p) for p in self._precond),
                   effect = effect_str
                   )
        return operator_str
