from os.path import basename
import traceback


def extract_traceback(e):
    # Extract traceback details
    tb = traceback.extract_tb(e.__traceback__)
    
    if tb:
        # Get the last traceback frame (where the error occurred)
        last_frame = tb[-1]
        filepath = basename(last_frame.filename)  # Get only the file name
        func_name = last_frame.name
        line_no = last_frame.lineno
        code_line = last_frame.line.strip() if last_frame.line else "N/A"
        
        # If the exception occurred inside the user's function, adjust the file path
        # This is useful when the error comes from a decorated function.
        if filepath.endswith("errors.py"):
            # Find the next frame in the stack, which should be the user's code
            last_frame = tb[-2] if len(tb) > 1 else last_frame
            filepath = basename(last_frame.filename)  # Get only the file name
            func_name = last_frame.name
            line_no = last_frame.lineno
            code_line = last_frame.line.strip() if last_frame.line else "N/A"
            
        # Log the error in the desired format
        return f"{filepath}/{func_name}:{line_no} | {code_line} | {type(e).__name__}: {e}"