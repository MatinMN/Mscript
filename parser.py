import lexer

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
        token = self.current_token

        if token.type in (lexer.TT_FLOAT,lexer.TT_INT):
            self.advance()
            return NumberNode(token)

    def term(self):
        return self.bin_op(self.factor,(lexer.TT_MUL,lexer.TT_DIV))

    def expr(self):
        return self.bin_op(self.term,(lexer.TT_PLUS,lexer.TT_MINUS))
        

    def bin_op(self, func , ops):
        left = func()

        while self.current_token.type in ops:
            op_token = self.current_token
            self.advance()
            right = func()
            left = BinOpNode(left,op_token,right)

        return left

    def parse(self):
        res = self.expr()
        return res