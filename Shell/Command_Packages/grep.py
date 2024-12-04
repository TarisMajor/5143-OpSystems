# Command_Packages/grep.py
import re
from rich.console import Console
from rich.text import Text
from .dbCommands import DbCommands

db_path = './P01/ApiStarter/data/filesystem.db'

# def replace_pattern(text, pattern, replacement):
#     # Define a function to format the replacement text
#     def format_replacement(match):
#         return Text(replacement, style="bold red")

#     # Use regex to substitute the pattern with formatted text
#     new_text = re.sub(pattern, format_replacement, text)
#     return new_text

def replace_pattern_with_format(plain_text, pattern, replacement, replacement_style="bold red"):
    # Initialize a list to store parts of the rich Text (to preserve formatting)
    result_text = Text()

    # Use regular expression to find all occurrences of the pattern in the plain text
    last_end = 0
    for match in re.finditer(pattern, plain_text):
        # Append the text before the match (if any)
        result_text.append(plain_text[last_end:match.start()])

        # Append the replacement with desired style
        formatted_text = Text(replacement, style=replacement_style)
        result_text.append(formatted_text)

        # Update the last_end index to the end of the current match
        last_end = match.end()

    # Append any remaining text after the last match
    result_text.append(plain_text[last_end:])
    
    return result_text

def grep(**kwargs):
    
   """
    NAME
       grep, egrep, fgrep, rgrep - print lines that match patterns

    SYNOPSIS
       grep [OPTION...] PATTERNS [FILE...]
       grep [OPTION...] -e PATTERNS ... [FILE...]
       grep [OPTION...] -f PATTERN_FILE ... [FILE...]

    DESCRIPTION
       grep  searches  for  PATTERNS in each FILE.  PATTERNS is one or more patterns separated by newline characters,
       and grep prints each line that matches a pattern.  Typically PATTERNS should be quoted when grep is used in  a
       shell command.

       A  FILE  of  “-”  stands  for  standard  input.   If  no FILE is given, recursive searches examine the working
       directory, and nonrecursive searches read standard input.

       In addition, the variant programs egrep, fgrep and rgrep are  the  same  as  grep -E,  grep -F,  and  grep -r,
       respectively.  These variants are deprecated, but are provided for backward compatibility.
    """
    
    # Grep doesn't handle flags but handles params
   flags = kwargs.get("flags")
   params = kwargs.get("params")
    
   #Grep gets the first parameter as a pattern which is a string
   pattern = params[0] 
   console = Console()
   valid_flags = ['l', 'c']
    
   #grep gets the next parameter as the file to read from
   file = params[-1]
   count = 0
   string = ''
   string = Text(string)
   newline = '\n'
   newline = Text(newline)
   decoy = file
   
   size = len(decoy.encode('utf-8'))
   
   if size < 100:
      if "./P01" in file:
         # If looking in a local file 
         with open(file, 'r') as open_file:
            for line_number, line in enumerate(open_file, start=0):
                  if pattern in line:
                     replaced_pattern = pattern
                     formatted_line = replace_pattern_with_format(line, pattern, replaced_pattern)
                     count += 1
                     string = string + formatted_line + newline
            if flags:
               if len(flags) == 1:
                  flags = flags[0]
                  flags = flags.strip('-')
                  if flags in valid_flags:
                     if flags == 'c':
                        return(f'{count}')
                     elif flags == 'l':
                        return(f'{file}')
               else:
                  return(f'Only -l and -n are supported in this shell.')
            else:
               console.print(string)
                  
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
                     
               for line_number, line in enumerate(contents, start=0):
                  if pattern in line:
                     replaced_pattern = pattern
                     formatted_line = replace_pattern_with_format(line, pattern, replaced_pattern)
                     count += 1
                     string = string + formatted_line + newline
                           
                     if flags:
                        if len(flags) == 1:
                           flags = flags[0]
                           flags = flags.strip('-')
                           if flags in valid_flags:
                              if flags == 'c':
                                 return(f'{count}')
                              elif flags == 'l':
                                 return(f'{file}')
                           else:
                              return(f'Only -l and -n are supported in this shell')
                     else:
                        console.print(string)
            else:
               return('File does not exist.')
         else:
            return('Directory does not exist.')
      else:
            return("Please enter a text file to be searched.")
   else:
      file = file.split('\n')
      string = []
      
      for line_number, line in enumerate(file, start=0):
         if pattern in line:
            replaced_pattern = pattern
            formatted_line = replace_pattern_with_format(line, pattern, replaced_pattern)
            count += 1
            # console.print(formatted_line)
            string.append(formatted_line)
            
      if flags:
         if len(flags) == 1:
            flags = flags[0]
            flags = flags.strip('-')
            if flags in valid_flags:
               if flags == 'c':
                  return(f'{count}')
               elif flags == 'l':
                  return(f'{file}')
         else:
            return(f'Only -l and -n are supported in this shell')
      else:
         for i in range(len(string)):
            console.print(string[i])
    
         
                    
    