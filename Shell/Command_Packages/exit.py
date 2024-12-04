import sys

def exit(**kwargs):
    
    return False

    
if __name__ == "__main__" :
    string = "Hello, World"
    
    b = string.encode('utf-8')
    
    t = string.encode('latin-1')
        
    print(b)
    print(t)