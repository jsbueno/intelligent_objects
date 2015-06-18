from __future__ import division

class ExactDivision(float):
    def __new__(cls, value=0, denominator = None):
        if denominator:
            self = float.__new__(cls, float.__truediv__(float(value), float(denominator)))
        else:
            self = float.__new__(cls, value)
        self.numerator = value
        self.denominator = denominator
        return self
    
    def __truediv__(self, other):
        return ExactDivision(self, other)
    
    def __repr__(self):
        if self.denominator is None:
            return str(self.numerator)
        t = lambda x: isinstance(x, ExactDivision) and x.denominator is not None
        
        numerator = "({})".format(self.numerator) if t(self.numerator) else self.numerator
        denominator = "({})".format(self.denominator) if t(self.denominator) else self.denominator
        
        return "{}/{}".format(numerator, denominator)
    
    __str__ = __repr__


ED = ExactDivision

__doc__ = """
>>> a = ED(8)
>>> a
8
>>> a/3
8/3
>>> a/3/5
(8/3)/5
>>> round(a / 3, 3)
2.667
"""