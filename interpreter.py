import constents

class Number:
    def __init__(self, value):
        self.value = value

    def set_pos(self, pos_start=None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value)
    
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value)
    
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value)

    def dived_by(self, other):
        if isinstance(other, Number):
            return Number(self.value / other.value)

    def __repr__(self):
        return str(self.value)
    
class Interpreter:

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'

        method = getattr(self, method_name, self.no_visit_method)


        return method(node)


    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method defined')


    
    def visit_NumberNode(self, node):
        return Number(node.token.value).set_pos(node.pos_start, node.pos_end)

    def visit_BinOpNode(self, node):
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        if node.op_token.type == constents.TT_PLUS:
            results = left.added_to(right)
        elif node.op_token.type == constents.TT_MINUS:
            results = left.subbed_by(right)
        elif node.op_token.type == constents.TT_MUL:
            results = left.multed_by(right)
        elif node.op_token.type == constents.TT_DIV:
            results = left.dived_by(right)
        
        return results.set_pos(node.pos_start, node.pos_end)

    def visit_UnararyOpNode(self, node):
        number = self.visit(node.node)

        if node.op_token.type == constents.TT_MINUS:
            number = number.multed_by(Number(-1))
        
        return number.set_pos(node.pos_start, node.pos_end)