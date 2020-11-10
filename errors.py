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