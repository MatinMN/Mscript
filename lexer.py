TT_FLOAT  = 'TT_FLOAT'
TT_INT    = 'TT_INT'
TT_PLUS   = 'TT_PLUS'
TT_MINUS  = 'TT_MINUS'
TT_MUL    = 'TT_MUL'
TT_DIV    = 'TT_DIV'
TT_LPAREN = 'TT_LPAREN'
TT_RPAREN = 'TT_RPAREN'

DIGITS = '0123456789'

class Error :
    def __init__(self, error_name, details, pos_start, pos_end):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end


    def as_string(self):
        return f'{self.error_name}: {self.details}' + f'File {self.pos_start.file}, line {self.pos_start.ln + 1}'

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("Illegal Character" ,details, pos_start, pos_end)

class Position:
    def __init__(self, index, ln , col, file = '', file_text = ''):
        self.index = index
        self.ln = ln
        self.col = col
        self.file = file
        self.file_text = file_text
    
    def advance(self, current_char):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1 
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.file, self.file_text)


class Token:
    def __init__(self, type , value = None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:

    def __init__(self,file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1 , 0 ,-1,file_name,text)
        self.current_char = None
    
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.index < len(self.text):
            self.current_char = self.text[self.pos.index] 
        else:
            self.current_char = None
    
    def make_tokens(self):
        tokens = []
        self.advance()
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                
                return [],IllegalCharError("'" + char + "'",pos_start,self.pos)

        return tokens , None
    

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count ==  1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT,int(num_str))
        else :
            return Token(TT_FLOAT, float(num_str))


def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error