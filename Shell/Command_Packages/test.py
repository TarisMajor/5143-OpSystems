import base64
import re
import requests
import sqlite3
from rich.text import Text
from rich.console import Console
import shutil

db_path = './P01/ApiStarter/data/filesystem.db'  

def encodeIt(plainText):
    # Encode the string as bytes, then to Base64
    encoded = base64.b64encode(plainText.encode("utf-8"))
    # Convert back to string for display
    return encoded


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

def decodeIt(encodedText):
    # Decode Base64 to original bytes
    decoded = base64.b64decode(encodedText)
    # Convert bytes back to string
    return decoded.decode("utf-8")

def test():
    cwd = "!!!!!9"
    cwd = list(cwd)
    cmd = cwd.split(" ")

    if "/" in cwd:
        
        path = cwd.split("/")
        
    print(path)

if __name__ == "__main__":
    
    terminal_size = shutil.get_terminal_size()
    
    width, height = terminal_size
    
    print(f"Console Size: {width} columns x {height} rows")
    