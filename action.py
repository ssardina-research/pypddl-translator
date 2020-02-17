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
    def __det_effect_to_str(effect):
        if len(effect) > 1  and isinstance(effect[0][0],float): # No labeled effects
            if all(isinstance(x,tuple) for x in effect): # Conjunction of predicates as effects
                effect_str = '(and {})'.format(' '.join(repr(e[1]) for e in effect))
            else: # We have conditional effects
                effect_str = '(and '
                for x in effect:
                    if isinstance(x,tuple): # Simple predicate
                        effect_str += repr(x[1])
                    else: # Conditional effect
                        effect_str += ' (when '
                        for set_of_pred in x:
                            effect_str += '(and {})'.format(' '.join(repr(y[1]) for y in set_of_pred))
                        effect_str += ')'

        elif len(effect) == 1:
            effect_str = ' '.join(repr(e[1]) for e in effect)
        elif len(effect) > 1 and not isinstance(effect[0][0],float): # Labeled effects
            effect_str = '(' + effect[0] + ' (and ' + ' '.join(repr(pred[1]) for pred in effect[1][0]) + '))\n\t\t'
        else:
            print("Something very wrong, an effect is empty...")
        return effect_str

    def __repr__(self):
        effect_str = ''
        if len(self._effects) == 1 and isinstance(self.effects[0][0][0],float) : # No labeled effects
            effect_str = Action.__det_effect_to_str(self._effects[0])
        elif len(self._effects) > 1:
            effect_str = '(oneof {})'.format(' '.join(Action.__det_effect_to_str(x) for x in self._effects))
        elif len(self._effects) == 1 and isinstance(self.effects[0][0][0][0],str): # Labeled effects
            effect_str = '(oneof {})'.format(' '.join(Action.__det_effect_to_str(x) for x in self._effects[0]))

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
