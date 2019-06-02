class Operator:
    def __init__(self, display, out_stack_rank, in_stack_rank):
        self.in_stack_rank = in_stack_rank
        self.out_stack_rank = out_stack_rank
        self.display = display

    def __str__(self):
        return "[%s]" % self.display

    def __gt__(self, other):
        if isinstance(other, Operator):
            return self.out_stack_rank > other.in_stack_rank
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, Operator):
            return self.out_stack_rank < other.in_stack_rank
        raise NotImplementedError

    def __ge__(self, other):
        return not self < other

    def __le__(self, other):
        return not self > other

    def calc_from_stack(self, stack_operands: list, stack_operators: list):
        raise NotImplementedError


class UnaryOperator(Operator):
    def __init__(self, display, compute, out_stack_rank, in_stack_rank=None):
        Operator.__init__(self, display, out_stack_rank,
                          in_stack_rank if in_stack_rank is not None else out_stack_rank + 1)
        self.compute = compute

    def calc(self, arg1):
        return self.compute(arg1)

    def calc_from_stack(self, stack_operands: list, _):
        stack_operands.append(self.calc(stack_operands.pop()))


class BinaryOperator(Operator):
    def __init__(self, display, compute, out_stack_rank, in_stack_rank=None):
        Operator.__init__(self, display, out_stack_rank,
                          in_stack_rank if in_stack_rank is not None else out_stack_rank)
        self.compute = compute

    def calc(self, arg1, arg2):
        return self.compute(arg1, arg2)

    def calc_from_stack(self, stack_operands: list, _):
        arg2 = stack_operands.pop()
        arg1 = stack_operands.pop()
        stack_operands.append(self.calc(arg1, arg2))


class LeftBracket(Operator):
    def __init__(self):
        Operator.__init__(self, '(', -2, 9)

    def calc_from_stack(self, _, __):
        raise TypeError


class RightBracket(Operator):
    def __init__(self):
        Operator.__init__(self, ')', 10, -1)

    def calc_from_stack(self, _, stack_operators: list):
        assert isinstance(stack_operators.pop(), LeftBracket), ''


class __EndOperator(Operator):
    def __init__(self):
        Operator.__init__(self, '=', 'impossible to get here', -10)

    def calc_from_stack(self, stack_operands: list, stack_operators: list):
        raise TypeError


__end_op = __EndOperator()
__lb_op = LeftBracket()
__rb_op = RightBracket()


def get_left_bracket_op():
    return __lb_op


def get_right_bracket_op():
    return __rb_op


def calc(ops: list):
    ops.append(__end_op)
    stack_operators = list()
    stack_operands = list()
    if not isinstance(ops[0], Operator):
        stack_operands.append(ops.pop(0))
    for operator in ops:
        if isinstance(operator, Operator):
            while len(stack_operators) != 0 and stack_operators[-1] >= operator:
                stack_operators.pop().calc_from_stack(stack_operands, stack_operators)
            stack_operators.append(operator)
        else:
            stack_operands.append(operator)
    assert len(stack_operands) == 1
    return stack_operands[0]

