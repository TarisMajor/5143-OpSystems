# Command_Packages/exclamation.py
import shell
import importlib
import pkgutil
import os
from .dbCommands import DbCommands
from .dbCommands import db_path

# Dictionary to store the commands
cmds = {}

def load_commands():
    global cmds
        
    # Get the current file's directory
    current_file_dir = os.path.dirname(__file__)

    # Get the parent directory
    parent_dir = os.path.abspath(os.path.join(current_file_dir, '..'))

    # Loop through all modules in the Command_Packages package
    for _, module_name, _ in pkgutil.iter_modules([parent_dir]):
        module = importlib.import_module(f"{module_name}")

        # Loop through the attributes in each module
        for name in dir(module):
            obj = getattr(module, name)
            # Check if it's a callable function and doesn't start with '__'
            if callable(obj) and not name.startswith("__"):
                cmds[name] = obj


def run_command(commandList):
    
    redirect = None
    append = None
    
    for item in commandList:
        cmd = item["cmd"]
        flags = item["flags"]
        params = item["params"]
        kwargs = {"flags":flags, "params": params}
        # Call the function dynamically from the dictionary
        if cmd in cmds:
            results = cmds[cmd](**kwargs)
            params.append(results)
      
        else:
            print(f"Command '{cmd}' not found.")
            
        if redirect:
            redirect = redirect.split('/')
            redirect = redirect[1:]
            redirect_dir = redirect[-2]
            redirect = redirect[-1]
            
            if DbCommands.file_exists(db_path, redirect):
                results = 'This file already exists.'
            else:           
                dir_id = DbCommands.get_dir_id(db_path, redirect_dir)
                results = DbCommands.new_file(db_path, redirect, results, dir_id)
        
        if append:
            append = append.split('/')
            append = append[1:]
            append_dir = append[-2]
            append = append[-1]
            
            if DbCommands.file_exists(db_path, append):
                dir_id = DbCommands.get_dir_id(db_path, append_dir)
                results = DbCommands.append_contents(db_path, append, dir_id, results)
            else:
                results = 'The file you are appending does not exist.'
    return(results)

def get_history():
    # Specify the path to your file
    file_path = './P01/history.txt'

    # Open the file and read lines into a list
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Remove newline characters from each line
    lines = [line.strip() for line in lines]

    # Print the list
    return(lines)


def exclamation(**kwargs):

    flags = kwargs.get("flags")
    params = kwargs.get("params")
    value = ''.join(params)
    load_commands()
        
    if params:
        if len(params) == 1:
            history = get_history()
            
            if value.isdigit():
                line_number = int(value)
                command = history[line_number]
                last_command, redirect, append = shell.parse(command)
                results = run_command(last_command)
                
                if redirect:
                    redirect = redirect.split('/')
                    redirect = redirect[1:]
                    redirect_dir = redirect[-2]
                    redirect = redirect[-1]
                    
                    if DbCommands.file_exists(db_path, redirect):
                        results = 'This file already exists.'
                    else:           
                        dir_id = DbCommands.get_dir_id(db_path, redirect_dir)
                        results = DbCommands.new_file(db_path, redirect, results, dir_id)
                
                if append:
                    append = append.split('/')
                    append = append[1:]
                    append_dir = append[-2]
                    append = append[-1]
                    
                    if DbCommands.file_exists(db_path, append):
                        dir_id = DbCommands.get_dir_id(db_path, append_dir)
                        results = DbCommands.append_contents(db_path, append, dir_id, results)
                    else:
                        results = 'The file you are appending does not exist.'
                    
            else:
                if value == "!":
                    command = history[-2]
                    last_command, redirect, append = shell.parse(command)
                    
                    results = run_command(last_command)
                    
                    if redirect:
                        redirect = redirect.split('/')
                        redirect = redirect[1:]
                        redirect_dir = redirect[-2]
                        redirect = redirect[-1]
                        
                        if DbCommands.file_exists(db_path, redirect, redirect_dir):
                            results = 'This file already exists.'
                        else:           
                            dir_id = DbCommands.get_dir_id(db_path, redirect_dir)
                            results = DbCommands.new_file(db_path, redirect, results, dir_id)
                    
                    if append:
                        append = append.split('/')
                        append = append[1:]
                        append_dir = append[-2]
                        append = append[-1]
                        dir_id = DbCommands.get_dir_id(db_path, append_dir)
                        
                        if DbCommands.file_exists(db_path, append, dir_id):
                            results = DbCommands.append_contents(db_path, append, dir_id, results)
                        else:
                            results = 'The file you are appending does not exist.'
                        
        else:
            results = 'This function accepts only one parameter'
    else:
        results = 'Do nothing'
    
    
    return(results)