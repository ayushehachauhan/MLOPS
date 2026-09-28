import sys
#sys module is used to get the details of the exception as sys,exc_info() returns a tuple of three values: (type, value, traceback).
#  The traceback object contains information about the call stack at the point where the exception occurred.
#  It allows you to access details such as the filename, line number, and function name where the exception was raised.


from src.logger import logging
def error_message_details(error,error_details:sys):  # this is for readability purpose, we can pass any name instead of error_details
    _,_,exc_tb=error_details.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in pyhton script [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error)
    )
    return error_message
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_details(error_message,error_details=error_detail)

    def __str__(self):
        return self.error_message