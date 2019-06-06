import ops
import re

__atom_pattern = re.compile(r'@'
                            r'|'
                            r'\$[A-Za-z0-9_]+'
                            r'|'
                            r'\d+[`°]\d{0,2}\'?\d{0,2}"?\d*'
                            r'|'
                            r'\d+\.?\d*'
                            r'|'
                            r'_?[+\-*/%!^()\[\]{},;~\:?<>.]'
                            r'|'
                            r'[A-Za-z]+'
                            r'|'
                            r'\s+'
                            )

var_format = re.compile(r'@|\$[A-Za-z0-9]$')

ans = '@'


def __try_get(key, *funcs):
    for f in funcs:
        try:
            return f(key)
        except:
            pass
    raise KeyError


def translate(formula_str: str, oplist: ops.OpList)-> list:
    def _get_var(s):
        if re.match(var_format, s) is not None:
            return oplist[s]
        else:
            raise KeyError

    origin_list = re.findall(__atom_pattern, formula_str)
    formula = [oplist.head]
    for piece in origin_list:
        if re.match(r'\s+', piece) is not None:
            pass
        else:
            if oplist.is_number(formula[-1]) or oplist.is_right_bracket(formula[-1]):
                try:
                    t = __try_get(piece, oplist.get_right_bracket, oplist.get_binary)
                    formula.append(t)
                except KeyError:
                    try:
                        t = __try_get(piece, oplist.get_left_bracket, oplist.get_const,
                                      oplist.string_to_real, oplist.get_unary, _get_var)
                        formula.append(oplist.connector)
                        formula.append(t)
                    except KeyError:
                        t = oplist.get_unary(oplist.postpos_unary_dict[piece])
                        count = 0
                        for i in range(len(formula) - 1, -1, -1):
                            if oplist.is_right_bracket(formula[i]):
                                count += 1
                            elif oplist.is_left_bracket(formula[i]):
                                count -= 1
                            if count == 0:
                                formula.insert(i, t)
                                break
            else:
                formula.append(__try_get(piece, oplist.get_unary, oplist.get_const, oplist.string_to_real,
                                         oplist.get_left_bracket, oplist.get_right_bracket, _get_var))
    return formula

