class Error :
    def __init__(self, error_name, details, pos_start, pos_end):
        self.error_name = error_name
        self.details = details
        self.pos_start = pos_start
        self.pos_end = pos_end


    def as_string(self):
        return f'{self.error_name}: {self.details}' + f'File {self.pos_start.file}, line {self.pos_start.ln + 1}'
        
    def __repr__(self):
        return f'{self.error_name}: {self.details}' + f'File {self.pos_start.file}, line {self.pos_start.ln + 1}'

class IllegalCharError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("Illegal Character" ,details, pos_start, pos_end)

class InvalidSyntaxError(Error):
    def __init__(self, details, pos_start, pos_end):
        super().__init__("Invalid Syntax" ,details, pos_start, pos_end)

class RunTimeError(Error):
    def __init__(self, details, pos_start, pos_end, context):
        super().__init__("Runtime Error" ,details, pos_start, pos_end)
        self.context = context

    def as_string(self):
        return f'{self.error_name}: {self.details}' + f'File {self.pos_start.file}, line {self.pos_start.ln + 1}'
        
    def __repr__(self):
        result = self.get_trace()
        result += f'{self.error_name}: {self.details}' + f'File {self.pos_start.file}, line {self.pos_start.ln + 1}'
        return result

    def get_trace(self):
        trace = ""

        context = self.context

        while context != None:
            trace += f'\n{context.display_name} : {context.parent_entry_pos}\n'
            context = context.parent

        return 'Traceback ( most recent call): \n' + trace
