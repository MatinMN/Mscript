import constents
import errors
from context import Context

class RunTimeResult:
    def __init__(self):
        self.value = None
        self.error = None


    def register(self, res):
        if res.error : self.error = res.error
        return res.value
    
    def success(self, value):
        self.value = value 
        return self

    def failure(self, error):
        self.error = error
        return self


class Number:

    context = None

    def __init__(self, value):
        self.value = value

    def set_pos(self, pos_start=None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context = None):
        self.context = context
        return self

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
    
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, errors.RunTimeError('Invalid operation Division by zero', other.pos_start, other.pos_end, self.context)
            return Number(self.value / other.value).set_context(self.context)

    def __repr__(self):
        return str(self.value)
    
class Interpreter:

    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'

        method = getattr(self, method_name, self.no_visit_method)


        return method(node, context)


    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')


    
    def visit_NumberNode(self, node, context):
        return RunTimeResult().success(
            Number(node.token.value).set_pos(node.pos_start, node.pos_end).set_context(context)
        )

    def visit_BinOpNode(self, node, context):
        res = RunTimeResult()
        left = res.register(self.visit(node.left_node, context))
        right = res.register(self.visit(node.right_node, context))

        if res.error : return res

        error = None

        if node.op_token.type == constents.TT_PLUS:
            results,error  = left.added_to(right)
        elif node.op_token.type == constents.TT_MINUS:
            results,error = left.subbed_by(right)
        elif node.op_token.type == constents.TT_MUL:
            results,error = left.multed_by(right)
        elif node.op_token.type == constents.TT_DIV:
            results,error  = left.dived_by(right)
        
        if error:
            return res.failure(error)
        
        return res.success(results.set_pos(node.pos_start, node.pos_end))

    def visit_UnararyOpNode(self, node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node, context))

        if res.error : return res

        error = None
        if node.op_token.type == constents.TT_MINUS:
            number,error  = number.multed_by(Number(-1))

        if error : return res.failure(error)

        return res.success(number.set_pos(node.pos_start, node.pos_end))