import mpmath
import calc2

mpmath.mp.dps = 50
mpmath.mp.frac = int(mpmath.mp.dps * 10 / 3)



class OpList:
    @staticmethod
    def __analyse_list(x):
        if isinstance(x, mpmath.matrix):
            if x.rows == 1:
                x = x.transpose()
            assert x.cols == 1, 'must one line'
            return [x[i, 0] for i in range(x.rows)]
        return [x]

    @staticmethod
    def __analyse_pair(x):
        r = OpList.__analyse_list(x)
        assert len(r) == 2, 'must a pair'
        return r

    @staticmethod
    def __analyse_as_pair(x):
        r = OpList.__analyse_list(x)
        assert len(r) <= 2 and len(r) != 0, 'must a number or a pair'
        if len(r) == 1:
            return [int(r[0]), int(r[0])]
        else:
            return [int(r[0]), int(r[1])]

    @staticmethod
    def __log(b, a):
        return mpmath.log(a, b)

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
                'pi': mpmath.mpf(mpmath.pi),
                'e': mpmath.mpf(mpmath.e),
                }[item]

    def get_unary(self, item):
        return {**{k: calc2.UnaryOperator(s, f, 80)
                   for k, s, f in [('abs',   'abs',   abs),
                                   ('fac',   'fac',    mpmath.factorial),
                                   ('sqrt',  'sqrt',  mpmath.sqrt),
                                   ('_/',    'sqrt',  mpmath.sqrt),
                                   ('ln',    'ln',    mpmath.ln),
                                   ('lg',    'log10', mpmath.log10),
                                   ('exp',   'e^',    mpmath.exp),
                                   ('floor', 'floor', mpmath.floor),
                                   ('ceil',  'ceil',  mpmath.ceil),
                                   ]
                   },
                'pcn': calc2.UnaryOperator('a%',
                                           lambda x: x / 100,
                                           80),
                '+': calc2.UnaryOperator('(+)',
                                         lambda x: x,
                                         0),
                '-': calc2.UnaryOperator('+/-',
                                         lambda x: -x,
                                         80),
                'conj': calc2.UnaryOperator('conj',
                                            lambda x: x.conjugate()
                                            if isinstance(x, mpmath.matrix)
                                            else mpmath.conj(x),
                                            80),
                '~': calc2.UnaryOperator('conj',
                                         lambda x: x.conjugate()
                                         if isinstance(x, mpmath.matrix)
                                         else mpmath.conj(x),
                                         80),
                'O': calc2.UnaryOperator('[O]',
                                         lambda x: mpmath.zeros(*OpList.__analyse_as_pair(x)),
                                         80),
                'I': calc2.UnaryOperator('[I]',
                                         lambda x: mpmath.ones(*OpList.__analyse_as_pair(x)),
                                         80),
                'E': calc2.UnaryOperator('[E]',
                                         lambda x: mpmath.eye(int(x)),
                                         80),
                'diag': calc2.UnaryOperator('[diag]',
                                            lambda x: mpmath.diag(OpList.__analyse_list(x)),
                                            80),
                'log': calc2.UnaryOperator('logbA',
                                           lambda x: OpList.__log(*OpList.__analyse_pair(x)),
                                           80),
                'tran': calc2.UnaryOperator('[T]',
                                            lambda x: x.transpose()
                                            if isinstance(x, mpmath.matrix)
                                            else x,
                                            80),
                **{k: calc2.UnaryOperator(k, (lambda u: lambda x: u(self._drg2r(x)))(v), 80)
                   for k, v in {'sin': mpmath.sinpi,
                                'cos': mpmath.cospi,
                                'tan': lambda x: mpmath.sinpi(x) / mpmath.cospi(x),
                                'cot': lambda x: mpmath.cospi(x) / mpmath.sinpi(x),
                                'sec': lambda x: 1 / mpmath.cospi(x),
                                'csc': lambda x: 1 / mpmath.sinpi(x),
                                }.items()
                   },
                **{k: calc2.UnaryOperator(k, (lambda u: lambda x: self._r2drg(1/v(x)))(v), 80)
                   for k, v in {'asin': mpmath.asin,
                                'acos': mpmath.acos,
                                'atan': mpmath.atan,
                                'acot': mpmath.acot,
                                'asec': mpmath.asec,
                                'acsc': mpmath.acsc}.items()
                   },
                **{k: calc2.UnaryOperator(k, v, 80)
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
        def _comma(a, b):
            if not isinstance(a, mpmath.matrix):
                a = mpmath.matrix([[a]])
            if not isinstance(b, mpmath.matrix):
                b = mpmath.matrix([[b]])
            assert a.rows == b.rows, 'matrix rows not equal'
            r = mpmath.matrix(a.rows, a.cols + b.cols)
            for i in range(a.rows):
                for j in range(a.cols):
                    r[(i, j)] = a[(i, j)]
                for j in range(b.cols):
                    r[(i, j + a.cols)] = b[(i, j)]
            return r

        def _semicolon(a, b):
            if not isinstance(a, mpmath.matrix):
                a = mpmath.matrix([[a]])
            if not isinstance(b, mpmath.matrix):
                b = mpmath.matrix([[b]])
            assert a.cols == b.cols, 'matrix cols not equal'
            r = mpmath.matrix(a.rows + b.rows, a.cols)
            for j in range(a.cols):
                for i in range(a.rows):
                    r[(i, j)] = a[(i, j)]
                for i in range(b.rows):
                    r[(i + a.rows, j)] = b[(i, j)]
            return r

        def _mul(a, b):
            r = a * b
            if isinstance(r, mpmath.matrix) and r.rows == 1 and r.cols == 1:
                return r[(0, 0)]
            else:
                return r

        def _dot(a, b):
            if isinstance(a, mpmath.matrix) and isinstance(b, mpmath.matrix):
                if a.rows == b.rows == 1 and a.cols == b.cols:
                    return _mul(a, b.transpose())
                elif a.cols == b.cols == 1 and a.rows == b.rows:
                    return _mul(a.transpose(), b)
            return _mul(a, b)

        return {'+': calc2.BinaryOperator('+', lambda x, y: x + y, 30),
                '-': calc2.BinaryOperator('-', lambda x, y: x - y, 30),
                '*': calc2.BinaryOperator('*', _dot, 31),
                'x': calc2.BinaryOperator('*', _mul, 31),
                '/': calc2.BinaryOperator('/', lambda x, y: x / y, 31),
                'mod': calc2.BinaryOperator('mod', mpmath.fmod, 31),
                '^': calc2.BinaryOperator('^', mpmath.power, 32),
                'rt': calc2.BinaryOperator('y_/x', lambda y, x: mpmath.root(x, y), 32),
                '_/': calc2.BinaryOperator('y_/x', lambda y, x: mpmath.root(x, y), 32),
                'log': calc2.BinaryOperator('blogA', lambda b, a: OpList.__log(b, a), 32),
                'P': calc2.BinaryOperator('nPr',
                                          lambda n, r: mpmath.factorial(n) / mpmath.factorial(n - r),
                                          50),
                'C': calc2.BinaryOperator('nCr',
                                          lambda n, r: mpmath.factorial(n) /
                                                       (mpmath.factorial(n - r) * mpmath.factorial(r)),
                                          50),
                'E': calc2.BinaryOperator('*10^',
                                          lambda s, e: mpmath.fmul(s, mpmath.power(10, e)),
                                          70),
                ',': calc2.BinaryOperator(',', _comma, 22),
                ';': calc2.BinaryOperator(';', _semicolon, 21),
                }[item]

    @property
    def postpos_unary_dict(self):
        return {'!': 'fac',
                '%': 'pcn',
                'T': 'tran',
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

    def is_matrix(self, m):
        return isinstance(m, mpmath.matrix)

    def is_left_bracket(self, o):
        return isinstance(o, calc2.LeftBracket)

    def is_right_bracket(self, o):
        return isinstance(o, calc2.RightBracket)

    def is_unary_operator(self, o):
        return isinstance(o, calc2.UnaryOperator)

    def is_binary_operator(self, o):
        return isinstance(o, calc2.BinaryOperator)
