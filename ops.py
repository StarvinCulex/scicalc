import mpmath
import calc2

mpmath.mp.dps = 100
mpmath.mp.frac = int(mpmath.mp.dps * 10 / 3)

class OpList:
    _r2drg_formula = {'deg': lambda r: r / mpmath.pi * 180,
                      'rad': lambda r: r,
                      'grad': lambda r: r / mpmath.pi * 200}
    _drg2r_formula = {'deg': lambda d: d * mpmath.pi / 180,
                      'rad': lambda r: r,
                      'grad': lambda g: g * mpmath.pi / 200}

    def __init__(self):
        self._drg_mode = 'deg'

    @property
    def drg(self):
        return self._drg_mode

    @drg.setter
    def drg(self, val):
        val = str(val).lower()
        if val in ('deg', 'rad', 'grad'):
            self._drg_mode = val
        else:
            raise ValueError

    def _r2drg(self, value):
        return OpList._r2drg_formula[self._drg_mode](value)

    def _drg2r(self, value):
        return OpList._drg2r_formula[self._drg_mode](value)

    def __getitem__(self, item):
        return {'i': mpmath.mpc(1j),
                'j': mpmath.mpc(1j),
                'pi': mpmath.pi,
                'e': mpmath.e,

                **{k: calc2.UnaryOperator(s, f, 8)
                   for k, s, f in [('abs',   '|a|',   mpmath.fabs),
                                   ('neg',   '+/-',   mpmath.fneg),
                                   ('fac',   'n!',    mpmath.factorial),
                                   ('sqrt',  '_/',    mpmath.sqrt),
                                   ('ln',    'ln',    mpmath.ln),
                                   ('lg',    'log10', mpmath.log10),
                                   ('exp',   'e^',    mpmath.exp),
                                   ]
                   },
                'rec': calc2.UnaryOperator('1/',
                                           lambda x: 1 / x,
                                           8),
                **{k: calc2.UnaryOperator(k, lambda x: v(self._drg2r(x)), 8)
                   for k, v in {'sin': mpmath.sin,
                                'cos': mpmath.cos,
                                'tan': mpmath.tan,
                                'cot': mpmath.cot,
                                'sec': mpmath.sec,
                                'csc': mpmath.csc}.items()
                   },
                **{k: calc2.UnaryOperator(k, lambda x: self._r2drg(v(x)), 8)
                   for k, v in {'asin': mpmath.asin,
                                'acos': mpmath.acos,
                                'atan': mpmath.atan,
                                'acot': mpmath.acot,
                                'asec': mpmath.asec,
                                'acsc': mpmath.acsc}.items()
                   },
                **{k: calc2.UnaryOperator(k, v, 8)
                   for k, v in {'sinh': mpmath.sinh,
                                'cosh': mpmath.cosh,
                                'tanh': mpmath.tanh,
                                'coth': mpmath.coth,
                                'sech': mpmath.sech,
                                'csch': mpmath.csch,
                                'asinh': mpmath.asinh,
                                'acosh': mpmath.acosh,
                                'atanh': mpmath.atanh,
                                'acoth': mpmath.acoth,
                                'asech': mpmath.asech,
                                'acsch': mpmath.acsch}.items()
                   },

                '+': calc2.BinaryOperator('+', mpmath.fadd, 2),
                '-': calc2.BinaryOperator('-', mpmath.fsub, 2),
                '*': calc2.BinaryOperator('*', mpmath.fmul, 3),
                '/': calc2.BinaryOperator('/', mpmath.fdiv, 3),
                'mod': calc2.BinaryOperator('mod', mpmath.fmod, 3),
                '^': calc2.BinaryOperator('^', mpmath.power, 4),
                'rt': calc2.BinaryOperator('y_/x', lambda y, x: mpmath.root(x, y), 4),
                'log': calc2.BinaryOperator('blogA', lambda b, a: mpmath.log(a, b), 4),
                'P': calc2.BinaryOperator('nPr',
                                          lambda n, r: mpmath.factorial(n) / mpmath.factorial(n - r),
                                          5),
                'C': calc2.BinaryOperator('nCr',
                                          lambda n, r: mpmath.factorial(n) /
                                                       (mpmath.factorial(n - r) * mpmath.factorial(r)),
                                          5),
                'E': calc2.BinaryOperator('*10^',
                                          lambda s, e: mpmath.fmul(s, mpmath.power(10, e)),
                                          6),
                }[item]

