class ArrayTypeError(Exception):
    """
    Custom exception for errors related to array type issues.
    """
    def __init__(self, func_name, array_value, array_index, expected_type, file_path, line_no):
        self.func_name = func_name
        self.array_value = array_value
        self.array_type = type(self.array_value).__name__  
        self.array_index = array_index
        self.expected_type = expected_type  
        self.file_path = file_path 
        self.line_no = line_no  
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | Elements in the array must contain the same type. Found (Value '{self.array_value}' | Index '{self.array_index}' | Type <'{self.array_type}'> | Expected <'{self.expected_type}'>)"
    

class ArrayNotFound(Exception):
    def __init__(self, arg, func_name, file_path, line_no):
        self.arg = arg
        self.func_name = func_name
        self.file_path = file_path 
        self.line_no = line_no 
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | First argument must be a list | Argument '{self.arg}' of type <'{type(self.arg).__name__}'> is invalid."
    

class ArraySizeChange(Exception):
    def __init__(self, func_name, file_path, line_no, initial_len, final_len):
        self.func_name = func_name
        self.file_path = file_path 
        self.line_no = line_no 
        self.initial_len = initial_len
        self.final_len = final_len
        super().__init__() 
    
    def __str__(self):
        return f"{self.file_path}/{self.func_name}:{self.line_no} | The size of the array has changed during execution | Inital Length: '{self.initial_len}' | Final Length: '{self.final_len}'"
    

