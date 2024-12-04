# Command_Packages/cd.py
from shell import modify_CWD
from shell import get_CWD

global db_Path

default = "/1000-Spacial_Data_Structures"

def cd(**kwargs):
    
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    if not params:
        modify_CWD(default)
        
    else:
        get_CWD(params)
    