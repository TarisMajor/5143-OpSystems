# Command_Packages/who.py

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
    
    return("root")