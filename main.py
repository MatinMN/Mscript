import lexer
from parser import Parser
from interpreter import Interpreter
while True:
    text = input("Mscript :>>> ")

    tokens, error = lexer.run('<stdin>',text)

    if error :
        print(error.as_string())
        continue

    print(tokens)
    parse = Parser(tokens)
    ast = parse.parse()

    interpreter = Interpreter()
    result = interpreter.visit(ast.node)


    print(result)

    
    