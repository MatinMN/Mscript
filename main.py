import lexer
from parser import Parser

while True:
    text = input("Mscript :>>> ")

    tokens, error = lexer.run('<stdin>',text)

    if error :
        print(error.as_string())
        continue

    print(tokens)
    parse = Parser(tokens)
    ast = parse.parse()

    print(ast.node,ast.error)
    