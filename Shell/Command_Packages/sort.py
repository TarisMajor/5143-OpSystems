# Command_Packages/sort.py
from shell import get_CWD
from .dbCommands import DbCommands


db_path = './P01/ApiStarter/data/filesystem.db' 

def sort(**kwargs):
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    content = params[0]
    
    size = len(content.encode('utf-8'))
    
    if flags:
        return(f"This function does not accept flags")
    else:
        if size < 100:
            if DbCommands.this_file_exists(db_path, content):
                file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, content)
                file_contents = DbCommands.get_Content(db_path, file_id, dir_id)
                
                words = file_contents.split()
                sorted_words = sorted(words)
                sorted_file_contents = ' '.join(sorted_words)
                
                return(sorted_file_contents)
            else:
                return(f"The file does not exist.")
                
        else:
            words = content.split()
            sorted_words = sorted(words)
            sorted_file_contents = ' '.join(sorted_words)
            
            return(sorted_file_contents)