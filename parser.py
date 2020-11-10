import lexer
import constents
import errors

class NumberNode:
    def __init__(self, token):
        self.token = token


    def __repr__(self):
        return f'{self.token}'

class BinOpNode:
    def __init__(self, left_node, op_token, right_node):
        self.left_node = left_node
        self.op_token = op_token
        self.right_node = right_node
    
    def __repr__(self):
        return f'({self.left_node}, {self.op_token}, {self.right_node})'

class UnararyOpNode:
    def __init__(self, op_token, node):
        self.op_token = op_token
        self.node = node

    def __repr__(self):
        return f'({self.op_token}, {self.node})'


class ParserResult:

    def __init__(self):
        self.error = None
        self.node = None 

    def register(self, res):
        if isinstance(res, ParserResult):
            if res.error: self.error = res.error
            return res.node 
        return res

    def success(self, node):
        self.node = node 
        return self

    def failure(self, error):
        self.error = error
        return self


class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_index = -1
        self.current_token = None
        self.advance()

    
    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        
        return self.current_token

    def factor(self):
        res = ParserResult()
        token = self.current_token

        if token.type in (constents.TT_PLUS,constents.TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:return res
            return res.success(UnararyOpNode(token, factor))


        if token.type in (constents.TT_FLOAT,constents.TT_INT):
            res.register(self.advance())
            return res.success(NumberNode(token))

        if token.type in (constents.TT_LPAREN):
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error : return res
            if self.current_token.type == constents.TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(errors.InvalidSyntaxError(
            self.current_token.pos_start, self.current_token.pos_end,
            'Exptected ) after ( but not found'
        ))


        return res.failure(errors.InvalidSyntaxError(
            token.pos_start, token.pos_end,
            'Exptected int or float'
        ))

    def term(self):
        return self.bin_op(self.factor,(constents.TT_MUL,constents.TT_DIV))

    def expr(self):
        return self.bin_op(self.term,(constents.TT_PLUS,constents.TT_MINUS))
        

    def bin_op(self, func , ops):
        res = ParserResult()
        left = res.register(func())

        if res.error: return res

        while self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = res.register(func())
            if res.error : return res
            left = BinOpNode(left,op_token,right)

        return res.success(left)

    def parse(self):
        res = self.expr()

        if not res.error and self.current_token.type != constents.TT_EOF:
            return res.failure(errors.InvalidSyntaxError(
                self.current_token.pos_start , self.current_token.pos_end,
                "Syntax error"
            ))
        return res