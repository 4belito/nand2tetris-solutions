''' 
This is an example for creating a function to be imported and look at human readable bytecode (.pyc) files
We also print the bytecode of the function at the end.
'''

def add(a,b):
    return a + b

import dis

bytecode = dis.dis(add)  # Disassemble the function to see its bytecode
print(bytecode)  # Print the disassembled bytecode