import constents
import errors

class Position:
    def __init__(self, index, ln , col, file = '', file_text = ''):
        self.index = index
        self.ln = ln
        self.col = col
        self.file = file
        self.file_text = file_text
    
    def advance(self, current_char = None):
        self.index += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1 
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.index, self.ln, self.col, self.file, self.file_text)


class Token:

    pos_start = None
    pos_end   = None

    def __init__(self, type , value = None, pos_start = None, pos_end = None):
        self.type = type
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

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
            elif self.current_char in constents.LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char == '=':
                tokens.append(Token(constents.TT_EQ, pos_start = self.pos))
                self.advance()    
            elif self.current_char == '+':
                tokens.append(Token(constents.TT_PLUS, pos_start = self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(constents.TT_MINUS, pos_start = self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(constents.TT_MUL, pos_start = self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(constents.TT_DIV, pos_start = self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(constents.TT_LPAREN, pos_start = self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(constents.TT_RPAREN, pos_start = self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                
                return [],errors.IllegalCharError("'" + char + "'",pos_start,self.pos)
        tokens.append(Token(constents.TT_EOF))
        return tokens , None
    

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

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
            return Token(constents.TT_INT,int(num_str),pos_start,self.pos)
        else :
            return Token(constents.TT_FLOAT, float(num_str),pos_start,self.pos)

    def make_identifier(self):
        id_str = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in constents.LETTERS_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        token_type = constents.TT_KEYWORD if id_str in constents.KEYWORDS else constents.TT_IDENTIFIER
        
        return Token(tok_type, id_strpos_start,self.pos)

def run(file_name, text):
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error