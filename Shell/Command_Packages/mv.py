# Command_Packages/mv.py
from .dbCommands import DbCommands
import base64
from shell import cwd


db_path = './P01/ApiStarter/data/filesystem.db'  

def mv(**kwargs):
    """
    NAME
       mv - move (rename) files

    SYNOPSIS
       mv [OPTION]... SOURCE... DIRECTORY
       mv [OPTION]... -t DIRECTORY SOURCE...

    DESCRIPTION
       Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY.
    """
    
    # MV doesn't handle flags but handles params
    flags = kwargs.get("flags")
    params = kwargs.get("params")
       
        
    if flags:
        return(f'This function does not accept flags.')
    else:
        if len(params) > 1:
            copy_file = params[0]
            copy_file = copy_file.split('/')
            copy_file = copy_file[1:]
            copy_dir = copy_file[-2]
            copy_file = copy_file[-1]
            
            paste_file = params[1]
            paste_file = paste_file.split('/')
            paste_file = paste_file[1:]
            paste_dir = paste_file[-2]
            paste_file = paste_file[-1]
            
            if DbCommands.file_exists(db_path, copy_file):
                if DbCommands.file_exists(db_path, paste_file):
                    if copy_dir == paste_dir:
                        if copy_file == paste_file:
                            return('Files in the same directory cannot have the same name.')  
                    return('The file already exists, choose another name.')
                else: 
                    paste_dir_id = DbCommands.get_dir_id(db_path, paste_dir)
                    result = DbCommands.move(db_path, copy_file, paste_file, paste_dir_id)
            else:
               return('File to be moved does not exist.')
        else:
            return('cp needs two files to function.')
                
    return(result)
    