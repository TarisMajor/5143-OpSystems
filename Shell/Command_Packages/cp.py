# Command_Packages/cp.py
from .dbCommands import DbCommands
import base64

db_path = './P01/ApiStarter/data/filesystem.db'  

def cp(**kwargs):
    """
    NAME
        cp - copy files and directories

    SYNOPSIS
        cp [OPTION]... [-T] SOURCE DEST
        cp [OPTION]... SOURCE... DIRECTORY
        cp [OPTION]... -t DIRECTORY SOURCE...

    DESCRIPTION
        Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY.

        Mandatory arguments to long options are mandatory for short options too.

    """
    # Gets the flags and params from the kwargs
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    # Since cp doesn't accept flags, we'll let the user know
    if flags:
        return(f'This function does not accept flags.')
    else:
        # cp must have more than one param in order to work
        if len(params) > 1:
            # We split the file paths of source and destination
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
            
            # Get the directory id of the files
            copy_dir_id = DbCommands.get_dir_id(db_path, copy_dir)
            paste_dir_id = DbCommands.get_dir_id(db_path, paste_dir)
            
            if DbCommands.file_exists(db_path, copy_file, copy_dir_id):
                if DbCommands.file_exists(db_path, paste_file, paste_dir_id):
                    if copy_dir == paste_dir:
                        if copy_file == paste_file:
                            return('Files in the same directory cannot have the same name.')  
                    return('The file already exists, choose another name.')
                else: 
                    paste_dir_id = DbCommands.get_dir_id(db_path, paste_dir)
                    result = DbCommands.copy(db_path, copy_file, paste_file, paste_dir_id)
            else:
               return('File to be copied does not exist.')
        else:
            return('cp needs two files to function.')
                
    return(result)
    