import formtrans
import calc2
import ops
import re


def main(line, _out, _info, op_list):
    if line.replace(' ', '') == '':
        pass
    elif line == 'drg':
        _info(op_list.drg)
    elif line in ['deg', 'rad', 'grad']:
        op_list.drg = line
        _info(op_list.drg)
    elif line == 'dms':
        _info('dms' if op_list.dms() else 'point')
    elif line.startswith('prec'):
        try:
            op_list.prec = int(line[line.find('prec') + 4:])
        finally:
            _info('prec %s' % op_list.prec)
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
    print('= Said the Calculator demo =')
    op_list = ops.OpList()
    while True:
        print('', end='> ', flush=True)
        main(input(), console_out, console_info, op_list)
