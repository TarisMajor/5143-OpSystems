# Command_Packages/history.py

def history(**kwargs):
    """
NAME
       history - GNU History Library

COPYRIGHT
       The GNU History Library is Copyright (C) 1989-2020 by the Free Software Foundation, Inc.

DESCRIPTION
       Many  programs  read  input  from the user a line at a time.  The GNU History library is able to keep track of
       those lines, associate arbitrary data with each line, and utilize information from previous lines in composing
       new ones.

HISTORY EXPANSION
       The  history  library supports a history expansion feature that is identical to the history expansion in bash.
       This section describes what syntax features are available.

       History expansions introduce words from the history list into the input stream, making it easy to repeat  com‐
       mands,  insert the arguments to a previous command into the current input line, or fix errors in previous com‐
       mands quickly.

       History expansion is usually performed immediately after a complete line is  read.   It  takes  place  in  two
       parts.   The first is to determine which line from the history list to use during substitution.  The second is
       to select portions of that line for inclusion into the current one.  The line selected from the history is the
       event, and the portions of that line that are acted upon are words.  Various modifiers are available to manip‐
       ulate the selected words.  The line is broken into words in the same fashion as bash does when reading  input,
       so that several words that would otherwise be separated are considered one word when surrounded by quotes (see
       the description of history_tokenize() below).  History expansions are introduced by the appearance of the his‐
       tory  expansion  character, which is ! by default.  Only backslash (\) and single quotes can quote the history
       expansion character.

    """
    # History doesn't handle flags nor params so doing nothing with them
    flags = kwargs.get("flags")
    params = kwargs.get("params")
    
    # Open the file in read mode
    with open('./P01/history.txt', 'r') as file:
        
        data = file.read()
        file.close()
        data = data.split("\n")
        dataList = {}
        
        dataList = {index: item for index, item in enumerate(data[:-1])}        
        h = ''
            
        for key, value in dataList.items():
            h = h + f"{key}  {value}\n"

        # print(data)
        return h


if __name__ == "__main__":
     with open('./P01/history.txt', 'r') as file:
         
        data = file.read()
        file.close()
        data = data.split("\n")
        dataList = {}
        
        # for index, item in enumerate(data):
        #     dataList[index] = data
        dataList = {index: item for index, item in enumerate(data[:-1])}
        #print(dataList)
        h = ''
        for key, value in dataList.items():
            # print(f"{key}  {value}")
            h = h + f"{key}  {value}\n"
        print(h)
        #for key, value in dataList.items():
          #  print(f"{key}  {value}")


    # Print the content of the file
        #print(dataList)