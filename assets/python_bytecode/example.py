''' 
This is for importing the add_example function to look at the Python bytecode file created.

When you import a module, Python compiles the .py into bytecode.
	•	That bytecode is saved as a .pyc in __pycache__.
	•	Next time you import the same module, Python just loads the cached .pyc → faster startup.
	•	This is why you see .pyc files for modules you import.

When you run python my_script.py:
	•	Python still compiles the code into bytecode (because the interpreter needs bytecode to execute).
	•	But for top-level scripts, it usually doesn’t save the .pyc — the bytecode is just kept in memory and executed immediately.
	•	Once the process ends, that in-memory bytecode is discarded.
'''

from add_axample import add

a = 5
b = 10
print(f'{a} + {b} = {add(a, b)}')