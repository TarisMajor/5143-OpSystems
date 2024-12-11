#!/usr/bin/env python
from subprocess import call

def cat(**kwargs):
    """   
    NAME
        cat - concatenate files and print on the standard output
    SYNOPSIS
        cat [OPTION]... [FILE]...
    DESCRIPTION
        Concatenate FILE(s) to standard output.

        -A, --show-all
                equivalent to -vET

        -b, --number-nonblank
                number nonempty output lines, overrides -n

        -e     equivalent to -vE

        -E, --show-ends
                display $ at end of each line

        -n, --number
                number all output lines

        -s, --squeeze-blank
                suppress repeated empty output lines

        -t     equivalent to -vT

        -T, --show-tabs
                display TAB characters as ^I

        --help display this help and exit

        --version
                output version information and exit
    EXAMPLES
        cat f - g
                Output f's contents, then standard input, then g's contents.

        cat    Copy standard input to standard output.
    """
    if 'params' in kwargs:
        params = kwargs['params']
    if 'flags' in kwargs:
        flags = kwargs['flags']
    command = ["cat"]

    for f in params:
        command.append(f)

    call(command)

    if __name__=='__main__':
        cat(files=['somefile','otherfile'])
        
# Cat command beta
#import os
#import sys
#from subprocess import call

# Define the cat function
def cat_command(**kwargs):
    """
    Implements the 'cat' command in Python with support for file paths and flags.
    
    :param parameters: List of file paths to read
    :param flags: Dictionary of flags, e.g., {'-n': True, '-E': True}
    """
    line_number_flag = file_path.get('-n', False)  # Check if the '-n' flag is passed
    end_of_line_flag = file_path.get('-E', False)  # Check if the '-E' flag is passed

    # Iterate over the parameters (file paths)
    
    for file_path in file_path['params']:
        if file_path.exists(file_path):  # Check if the file exists
            print(f"Success: {file_path} found.")
        else:
            print(f"Error: {file_path} not found.")
            continue  # Skip to the next file

        with open(file_path, 'r') as file:
            # Read each line from the file
            for line_num, line in enumerate(file, start=1):
                # Handle the line number flag
                if line_number_flag:
                    print(f"{line_num}\t", end='')

                # Print the line content
                if end_of_line_flag:
                    print(line.rstrip() + "$")  # Append $ to mark the end of line
                else:
                    print(line, end='')  # Print the line without an extra newline at the end

# Example usage of the cat_command
if __name__ == "__main__":
    # Example of calling cat_command with parameters and flags
    # The user can pass parameters and flags like this:
    
    # Parameters are file names or paths, flags are passed as a dictionary
    cat_command("file1.txt", "file2.txt", "-n", "-E")
