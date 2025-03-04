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


from pypddl.term import Term


class Predicate(object):

    def __init__(self, name, args=[]):
        """
            Construct a Predicate object

        :param name: string with the name of the predicate
        :param args: list of Term objects
        """

        self._name = name
        self._args = args

    @property
    def name(self):
        return self._name

    @property
    def args(self):
        return self._args[:]

    @property
    def arity(self):
        return len(self._args)

    def __str__(self):
        if self._name == '=':
            return '{0} = {1}'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return self._name
        else:
            return '{0}({1})'.format(self._name, ', '.join(map(str, self._args)))

    # def __repr__(self):
    #     return "Predicate(name = %s, args = %s)" % (self._name, self._args)


    def __repr__(self):
        if self._name == '=':
            return '(= {0} {1})'.format(str(self._args[0]), str(self._args[1]))
        elif self.arity == 0:
            return '({})'.format(self._name)
        else:
            return '({0} {1})'.format(self._name, ' '.join(map(str, self._args)))

    def __eq__(self, other):
        if self.name == other.name \
                and self.args == other.args:
            return True
        else:
            return False

    def __hash__(self):
        #print(hash(str(self)))
        return hash((self.name,str(self.args)))