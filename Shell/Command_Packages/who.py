# Command_Packages/who.py
from rich.text import Text

def who(**kwargs):
    """
    NAME
       who - displays current users

    SYNOPSIS
       who [OPTION]...

    DESCRIPTION
       Print a list of users currently logged in.
    """
    
    # WHO doesn't handle flags nor params
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    if flags:
        return(f"This function does not accept flags")
    else:
        if params:
            return(f"This function does not accept params")
         
    name = "root"
    name = Text(name)
    name.stylize("red")
    
    return name