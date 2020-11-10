import constents

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
            elif self.current_char in constents.DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(constents.TT_PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(constents.TT_MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(constents.TT_MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(constents.TT_DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(constents.TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(constents.TT_RPAREN))
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

        while self.current_char != None and self.current_char in constents.DIGITS + '.':
            if self.current_char == '.':
                if dot_count ==  1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(constents.TT_INT,int(num_str))
        else :
            return Token(constents.TT_FLOAT, float(num_str))


def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error