# Command_Packages/less.py
import shutil
from Command_Packages.getch import Getch
from Command_Packages.dbCommands import DbCommands
import os

db_path = './P01/ApiStarter/data/filesystem.db'

def less(**kwargs):
    """
    NAME
       less - opposite of more

    DESCRIPTION
       Less  is  a  program similar to more(1), but it has many more features.  Less does not have to read the entire
       input file before starting, so with large input files it starts up faster than text editors like vi(1).   Less
       uses  termcap  (or  terminfo on some systems), so it can run on a variety of terminals.  There is even limited
       support for hardcopy terminals.  (On a hardcopy terminal, lines which should be printed  at  the  top  of  the
       screen are prefixed with a caret.)

       Commands  are  based  on  both more and vi.  Commands may be preceded by a decimal number, called N in the de‐
       scriptions below.  The number is used by some commands, as indicated.

    """
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    file = params[0]
    
    size = len(file.encode('utf-8'))
    
    getch = Getch()
        
    contents = []
    
    if size < 100:
        # If looking in a local file 
        if "./P01" in file:
            with open(file, 'r') as open_file:
                for line in open_file:
                    contents.append(line)
                  
        elif "/1000" in file:
            file = file.split('/')
            file = file[1:]
            file_dir = file[-2]
            file_name = file[-1]
               
            if DbCommands.dir_exists(db_path, file_dir):
                dir_id = DbCommands.get_dir_id(db_path, file_dir)
                if DbCommands.file_exists(db_path, file_name, dir_id):
                    file_id, dir_id = DbCommands.get_file_and_dir_id(db_path, file_name)
                    contents = DbCommands.get_Content(db_path, file_id, dir_id)
                    contents = contents.splitlines()
                else:
                    return('File does not exist.')
            else:
                return('Directory does not exist.')
        else:
            return("Please enter a text file to be searched.")
    else:
        contents = file.splitlines()
    
    os.system('clear')
    
    top = 0
    terminal_size = shutil.get_terminal_size()
    
    width, height = terminal_size
    end = height - 1
        
    bleh = contents[top:end]
    for item in bleh:
        print(item)
        
    
    while True:
        terminal_size = shutil.get_terminal_size()
    
        width, height = terminal_size
        end = top + height - 1
        
        char = getch()
                
        # Arrow key pressed
        if '\x1b' in char:
                        
            ignore = getch()
            arrow = getch()
           
            if 'A' in arrow:
                if top == 0:
                    pass
                else:
                    os.system('clear')
                    
                    top -= 1
                    end = top + height - 1
                    out = contents[top:end]
                    for line in out:
                        print(line)
        
            #Down Arrow    
            elif 'B' in arrow:
                
                if end >= len(contents):
                    os.system('clear')
                    end = len(contents) - 1
                    top = end - height
                    out = contents[top:end]
                    for line in out:
                        print(line)
                    print('(END)')
                    
                elif end == len(contents):
                    pass
                
                else:
                    os.system('clear')
                    top += 1
                    end = top + height - 1
                    out = contents[top:end]
                    for line in out:
                        print(line)
            
            #Right Arrow    
            elif 'C' in arrow:
                os.system('clear')
                print('Right arrow pressed')
            
            # Left Arrow    
            elif 'D' in arrow:
                os.system('clear')
                print('Left arrow pressed.')
            
        # Page up
        elif char == 'w':
            # if top == 0:
            #     pass
            # else:
            os.system('clear')
            top -= height - 1
            end = top + height - 1
            out = contents[top:end]
            for line in out:
                print(line)
                
        # Page down
        elif char == 'd':
            if end >= len(contents):
                os.system('clear')
                end = len(contents)
                top = end - height
                out = contents[top:end]
                for line in out:
                    print(line)
                print('(END)')
                
            elif end == len(contents):
                pass
            
            else:
                os.system('clear')
                top += height - 1
                end = top + height - 1
                out = contents[top:end]
                for line in out:
                    print(line)
                
        # Page up
        elif char == 'q':
            break