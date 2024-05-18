"""
Author : Xarnia
Last Modified : 18/05/2024
Project : MoodleCalendarExporter
"""

class MoodleErrors(Exception):
    
    def __init__(self, msg=None, stacktrace=None):
        self.msg = msg
        self.stacktrace = stacktrace
        
    def __str__(self):
        exception_msg = "%s\n" % self.msg
        if self.stacktrace is not None:
            stacktrace = "\n".join(self.stacktrace)
            exception_msg += "Stacktrace:\n%s" % stacktrace
        return exception_msg
    
class LoginError(MoodleErrors):
    """
    Thrown when the user couldn't login.
    """
    
class CalendarNotRetrieved(MoodleErrors):
    """
    Thrown when the calendar isn't retrieved
    """
