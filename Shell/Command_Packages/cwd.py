# Command_Packages/cwd.py

from shell import get_CWD

def cwd(**kwargs):
    cwd = get_CWD()
    return(f'{cwd}')