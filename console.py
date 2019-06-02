import formtrans
import calc2
import ops

if __name__ == '__main__':
    op_list = ops.OpList()
    print('= scicalc console =')
    while True:
        print('', end='> ', flush=True)
        line = input()
        if line.replace(' ', '') == '':
            pass
        elif line.lower() == 'help' or line.lower() == '-help' or line.lower() == '--help'\
             or line == '?' or line == '-?':
            print('- help -\n'
                  '  ?       : print this message\n'
                  '  ? op    : print operator list\n'
                  '  ? func  : print function list\n'
                  '  ? const : print all constants\n'
                  '  drg     : display angel unit\n'
                  '  deg     : turn angel unit into DEG\n'
                  '  rad     : turn angel unit into RAD\n'
                  '  grad    : turn angel unit into GRAD\n'
                  '  quit    : exit this program')
        elif line == '? op':
            print('- operators -\n'
                  '  + A             : A itself\n'
                  '  - A             : negative a\n'
                  '  abs A           : |A|; absolute value of A\n'
                  '  A + B           : A plus B\n'
                  '  A - B           : A minus B\n'
                  '  A * B   : A x B : A multiplies B\n'
                  '  A / B           : A dividend by B\n'
                  '  A mod B : A % B : remainder of A dividend by B\n'
                  '  X ^ Y           : X power of Y\n'
                  '  Y rt X  : Y,/X  : X\'s root of Y; X^(1/Y)\n'
                  '  B log A         : logarithm of B with the base A\n'
                  '  n !     : fac n : factorial of n; (1*2*...*n)\n'
                  '  n P m           : P(n, m); n!/(n-m)!\n'
                  '  n C m           : C(n, m); n!/(m!*(n-m)!)\n'
                  '  a E b           : a * 10 ^ b\n'
                  '  p %     : pcn p : p / 100')
        elif line == '? func':
            print('- power/exponential/logarithmic functions -\n'
                  '  sqrt X  : ,/ X  : square root of X; X^0.5\n'
                  '  ln X            : logarithm of X with the base e=2.71828...\n'
                  '  lg X            : logarithm of X with the base 10\n'
                  '  exp X           : e^X; e=2.71828...\n'
                  '- trigonometric functions -\n'
                  '   sin :  cos :  tan :  cot :  sec :  csc\n'
                  '- inverse trigonometric functions -\n'
                  '  asin : acos : atan : acot : asec : acsc\n'
                  '- hyperbolic functions -\n'
                  '  sinh : cosh : tanh : coth : sech : csch\n'
                  '- inverse hyperbolic functions -\n'
                  '  asinh: acosh: atanh: acoth: asech: acsch')
        elif line == '? const':
            print('- constants -\n'
                  '    i    :    j   : the imaginary unit\n'
                  '    pi            : =3.1415926...\n'
                  '    e             : natural constant; =2.71828...')
        elif line == 'drg':
            print('-', op_list.drg)
        elif line in ['deg', 'rad', 'grad']:
            op_list.drg = line
            print('-', op_list.drg)
        elif line == 'quit':
            break
        else:
            try:
                p = formtrans.translate(line, op_list)
                print('<', calc2.calc(p))
            except Exception as e:
                print('- %s: %s' % (type(e), e))
