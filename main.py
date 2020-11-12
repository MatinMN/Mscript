import lexer
from parser import Parser
from interpreter import Interpreter
from context import Context
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
    root_ctx = Context('<main>')
    result = interpreter.visit(ast.node,root_ctx)


    print(result.value, result.error)

    
    