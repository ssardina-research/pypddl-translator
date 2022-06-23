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


class Term(object):

    def __init__(self, **kwargs):
        """
            Construct a Term object

            for variables ?x name is '?x'
            for typed variables like ?x - block, name is '?x' and type is 'block'
            constants like 'east' do not have ? in their name


        :param kwargs: up to three kwarg arguments that are all strings:
            name = the name of the term if variable (for example '?x' or 'table')
            type = the type of the term (for example 'blocks')
            var  = is this a variable? (otherwise it is a constant)
        """
        self._name  = kwargs.get('name')    # name of the term (includes ? for vars)
        self._type  = kwargs.get('type',  None) # subtype of term
        self._variable = kwargs.get('var', True)    # is it a var or a constat?
        self._constant = True if not self._variable else False

    @classmethod
    def variable(cls, name, type=None):
        return Term(name=name, type=type, var=True)

    @classmethod
    def constant(cls, name, type=None):
        return Term(name=name, type=type, var=False)

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def is_variable(self):
        return self._variable

    def is_typed(self):
        return self._type is not None

    def is_constant(self):
        return self._constant

    @type.setter
    def type(self, type):
        self._type = type


    
    def __str__(self):
        if self.is_variable() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_variable():
            return '{0}'.format(self._name)
        if self.is_constant() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_constant():
            return '{0}'.format(self._name)

    def __repr__(self):
        if self.is_variable() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_variable():
            return '{0}'.format(self._name)
        if self.is_constant() and self.is_typed():
            return '{0} - {1}'.format(self._name, self._type)
        if self.is_constant():
            return '{0}'.format(self._name)

    def __eq__(self, other):
        if self._name == other._name and self._type == other._type:
            return True
