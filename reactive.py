
from collections import defaultdict, namedtuple


Rule = namedtuple("Rule", "name attrs action")


class Reactor(object):
    def __init__(self):
        self.rules = defaultdict(list)
    def _rule_setter(self, rule):
        for attrname in rule.attrs:
            self.rules[attrname].append(rule)

    def __setattr__(self, attrname, value):
        if isinstance(value, Rule):
            self._rule_setter(value)
            self._exec_rule(value)
            return
        super(Reactor, self).__setattr__(attrname, value)
        rules = self.rules
        for rule in self.rules[attrname]:
            self._exec_rule(rule)

    def _exec_rule(self, rule):
        try:
            result =  rule.action(**dict((name, getattr(self, name)) for name in rule.attrs))
        except AttributeError:
            result = None
        setattr(self, rule.name, result)
            
            
R = Reactor()

__doc__= """
>>> from reactive import R, Rule
>>> R.c = Rule("c", ("a", "b"), lambda a, b: a + b)
>>> R.c
>>> R.a = 10
>>> R.b = 5
>>> R.c
15
>>> 
>>> R.d = Rule("d", ("c",), lambda c: c * 2)
>>> R.d
30
>>> 
>>> R.a = -1
>>> 
>>> R.d
8
"""
