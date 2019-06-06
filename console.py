import formtrans
import calc2
import ops
import re


def main(line, _out, _info):
    op_list = ops.OpList()
    if line.replace(' ', '') == '':
        pass
    elif line.lower() == 'help' or line.lower() == '-help' or line.lower() == '--help'\
            or line == '?' or line == '-?':
        _info('help -\n'
              '?       : print this message\n'
              '? op    : print operator list\n'
              '? func  : print function list\n'
              '? const : print all constants\n'
              '? var   : print tutorials about variables\n'
              'drg     : display angel unit\n'
              'deg     : turn angel unit into DEG\n'
              'rad     : turn angel unit into RAD\n'
              'grad    : turn angel unit into GRAD\n'
              'quit    : exit this program\n')
    elif line == '? op':
        _info('operators -\n'
              '+ A              : A itself\n'
              '- A              : negative a\n'
              'abs A            : |A|; absolute value of A\n'
              'A + B            : A plus B\n'
              'A - B            : A minus B\n'
              'A * B   : A x B  : A multiplies B\n'
              'A / B            : A dividend by B\n'
              'A mod B : A % B  : remainder of A dividend by B\n'
              'X ^ Y            : X power of Y\n'
              'Y rt X  : Y_/X   : X\'s root of Y; X^(1/Y)\n'
              'B log A :log(B,A): logarithm of B with the base A\n'
              'n !     : fac n  : factorial of n; (1*2*...*n)\n'
              'n P m            : P(n, m); n!/(n-m)!\n'
              'n C m            : C(n, m); n!/(m!*(n-m)!)\n'
              'a E b            : a * 10 ^ b\n'
              'p %              : pcn p : p / 100\n')
    elif line == '? func':
        _info('power/exponential/logarithmic functions -\n'
              'sqrt X  : _/ X  : square root of X; X^0.5\n'
              'ln X            : logarithm of X with the base e=2.71828...\n'
              'lg X            : logarithm of X with the base 10\n'
              'exp X           : e^X; e=2.71828...\n')
        _info('trigonometric functions -\n'
              ' sin :  cos :  tan :  cot :  sec :  csc\n'
              'inverse trigonometric functions -\n'
              'asin : acos : atan : acot : asec : acsc\n'
              'hyperbolic functions -\n'
              'sinh : cosh : tanh : coth : sech : csch\n'
              'inverse hyperbolic functions -\n'
              'asinh: acosh: atanh: acoth: asech: acsch\n')
    elif line == '? const':
        _info('constants -\n'
              'i :j: the imaginary unit\n'
              'pi  : =3.1415926...\n'
              'e   : natural constant; =2.71828...\n')
    elif line == '? var':
        _info('variable system -\n'
              'You can use variables in formula by its name.\n'
              "Strings beginning with $ and following English alphabets\n"
              "or Arabic numerals or underline are valid variable names.\n"
              "(e.g. $1, $1A2b_, $sin)\n")
        _info('last answer\n'
              'Every answer will be saved automatically\n'
              "in variable @ .\n")
        _info("modify variables -\n"
              "<variable> = <formula> : let variable be the value of formula\n"
              "<var> [+=][-=][*=][/=] <fm> : <var> = <var> [+][-][*][/] <fm>\n")
    elif line == 'drg':
        _info(op_list.drg)
    elif line in ['deg', 'rad', 'grad']:
        op_list.drg = line
        _info(op_list.drg)
    elif line == 'dms':
        _info('dms' if op_list.dms() else 'point')
    elif line == 'quit':
        _info('goodbye')
        exit(0)
    else:
        try:
            f = None
            if line.find('=') != -1:
                head = line[:line.find('=')]
                try:
                    f = {'+': lambda x, y: x + y,
                         '-': lambda x, y: x - y,
                         '*': lambda x, y: x * y,
                         '/': lambda x, y: x / y,
                         }[head[-1]]
                    head = head[:-1]
                except KeyError:
                    f = lambda x, y: y
                head = head.strip()
                if re.match(formtrans.var_format, head) is None:
                    raise ValueError('Invalid var name %s' % head)
                formula = line[line.find('=') + 1:]
            else:
                head = None
                formula = line
            form = formtrans.translate(formula, op_list)
            p = calc2.calc(form)
            if head is not None:
                op_list[head] = f(op_list[head], p)
            op_list[formtrans.ans] = p
            _out(op_list.num_to_string(p))
        except ZeroDivisionError:
            _info('division by zero')
        except IndexError:
            _info('syntax error')
        except Exception as e:
            _info('syntax error' if str(e) == '' else str(e))


def __console_print(text, prompt):
    lines = str(text).splitlines(keepends=False)
    for l in lines[:1]:
        print(prompt + l)
    for l in lines[1:]:
        print(' ' * len(prompt) + l)


def console_out(text):
    return __console_print(text, '< ')


def console_info(text):
    return __console_print(text, '- ')


if __name__ == '__main__':
    while True:
        print('', end='> ', flush=True)
        main(input(), console_out, console_info)
