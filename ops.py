import mpmath
import calc2

mpmath.mp.dps = 50
mpmath.mp.frac = int(mpmath.mp.dps * 10 / 3)


class OpList:
    _r2drg_formula = {'deg': lambda r: r / mpmath.pi * 180,
                      'rad': lambda r: r,
                      'grad': lambda r: r / mpmath.pi * 200}
    _drg2r_formula = {'deg': lambda d: d / 180,
                      'rad': lambda r: r / mpmath.pi,
                      'grad': lambda g: g / 200}

    def __init__(self):
        self._drg_mode = 'deg'
        self._mem = dict()

    def __getitem__(self, key):
        try:
            return self._mem[key]
        except KeyError:
            return mpmath.mpf(0)

    def __setitem__(self, key, val):
        self._mem[key] = val

    def num_to_string(self, num):
        return str(num)

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

    def get_left_bracket(self, item):
        if item in ['(', '[', '{']:
            return calc2.get_left_bracket_op()
        raise KeyError

    def get_right_bracket(self, item):
        if item in [')', ']', '}']:
            return calc2.get_right_bracket_op()
        raise KeyError

    def get_const(self, item):
        return {'i': mpmath.mpc(1j),
                'j': mpmath.mpc(1j),
                'pi': mpmath.pi,
                'e': mpmath.e,
                }[item]

    def get_unary(self, item):
        return {**{k: calc2.UnaryOperator(s, f, 8)
                   for k, s, f in [('abs',   '|a|',   mpmath.fabs),
                                   ('-',     '-',   mpmath.fneg),
                                   ('fac',   'n!',    mpmath.factorial),
                                   ('sqrt',  'sqrt',    mpmath.sqrt),
                                   (',/',    'sqrt',    mpmath.sqrt),
                                   ('ln',    'ln',    mpmath.ln),
                                   ('lg',    'log10', mpmath.log10),
                                   ('exp',   'e^',    mpmath.exp),
                                   ]
                   },
                'pcn': calc2.UnaryOperator('a%',
                                            lambda x: x / 100,
                                            8),
                '+': calc2.UnaryOperator('#',
                                         lambda x: x,
                                         1),
                **{k: calc2.UnaryOperator(k, (lambda u: lambda x: u(self._drg2r(x)))(v), 8)
                   for k, v in {'sin': mpmath.sinpi,
                                'cos': mpmath.cospi,
                                'tan': lambda x: mpmath.sinpi(x) / mpmath.cospi(x),
                                'cot': lambda x: mpmath.cospi(x) / mpmath.sinpi(x),
                                'sec': lambda x: 1 / mpmath.cospi(x),
                                'csc': lambda x: 1 / mpmath.sinpi(x),
                                }.items()
                   },
                **{k: calc2.UnaryOperator(k, (lambda u: lambda x: self._r2drg(1/v(x)))(v), 8)
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
                   }
                }[item]

    def get_binary(self, item):
        return {'+': calc2.BinaryOperator('+', mpmath.fadd, 2),
                '-': calc2.BinaryOperator('-', mpmath.fsub, 2),
                '*': calc2.BinaryOperator('*', mpmath.fmul, 3),
                'x': calc2.BinaryOperator('*', mpmath.fmul, 3),
                '/': calc2.BinaryOperator('/', mpmath.fdiv, 3),
                '%': calc2.BinaryOperator('mod', mpmath.fmod, 3),
                'mod': calc2.BinaryOperator('mod', mpmath.fmod, 3),
                '^': calc2.BinaryOperator('^', mpmath.power, 4),
                'rt': calc2.BinaryOperator('y,/x', lambda y, x: mpmath.root(x, y), 4),
                ',/': calc2.BinaryOperator('y,/x', lambda y, x: mpmath.root(x, y), 4),
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

    @property
    def postpos_unary_dict(self):
        return {'!': 'fac',
                '%': 'pcn',
                }

    @property
    def connector(self):
        return self.get_binary('*')

    @property
    def head(self):
        return self.get_unary('+')

    def string_to_real(self, s):
        return mpmath.mpf(s)

    def is_number(self, n):
        return isinstance(n, mpmath.mpf) or isinstance(n, mpmath.mpc)

    def is_left_bracket(self, o):
        return isinstance(o, calc2.LeftBracket)

    def is_right_bracket(self, o):
        return isinstance(o, calc2.RightBracket)

    def is_unary_operator(self, o):
        return isinstance(o, calc2.UnaryOperator)

    def is_binary_operator(self, o):
        return isinstance(o, calc2.BinaryOperator)
