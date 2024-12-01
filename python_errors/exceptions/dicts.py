class DictSizeChange(Exception):
    def __init__(self, func_name, file_path, line_no, initial_len, final_len):
        self.func_name = func_name
        self.file_path = file_path 
        self.line_no = line_no 
        self.initial_len = initial_len
        self.final_len = final_len
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | The number of keys has changed during execution | Inital Length: '{self.initial_len}' | Final Length: '{self.final_len}'"


class DictNotFound(Exception):
    def __init__(self, arg, func_name, file_path, line_no):
        self.arg = arg
        self.func_name = func_name
        self.file_path = file_path 
        self.line_no = line_no 
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | First argument must be a dict | Argument '{self.arg}' of type <'{type(self.arg).__name__}'> is invalid."
    

class DictTypeError(Exception):
    """
    Custom exception for errors related to dict type issues.
    """
    def __init__(self, func_name, key, value, expected_type, file_path, line_no, secure_key=False, secure_value=False):
        self.func_name = func_name
        self.key = key
        self.value = value
        self.type = type(self.key).__name__ if secure_key else type(self.value).__name__
        self.expected_type = expected_type  
        self.file_path = file_path 
        self.line_no = line_no  
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | Elements in the array must contain the same type. Found (Key '{self.key}' | Value '{self.value}' | Type <'{self.type}'> | Expected <'{self.expected_type}'>)"

