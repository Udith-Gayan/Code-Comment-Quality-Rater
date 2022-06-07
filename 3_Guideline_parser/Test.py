

import re

import matplotlib.pyplot as plt


#---------------------------------------Flask  localhost:5000-----------------------------------------------
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
   return 'Hello World'

@app.route('/ff')
def hello_worlddd():
   return 'Hello World 22'

if __name__ == '__main__':
   app.run()
   
#-------------------------------------------------------------------------------------

search_list = ['one', 'two', 'three']
long_string = 'someoNe elongtw phrasethre'
if re.compile('|'.join(search_list),re.IGNORECASE).search(long_string): #re.IGNORECASE is used to ignore case
    # Do Something if word is present
    print("Present")
else:
    # Do Something else if word is not present
    print("absent")
    
    
    
    
    
# Python3 code to demonstrate working of
# Get all substrings of string
# Using list comprehension + string slicing
  
# initializing string 
test_str = "I am Udith Gayan"
  
# printing original string 
print("The original string is : " + str(test_str))
  
# Get all substrings of string
# Using list comprehension + string slicing
res = [test_str[i: j] for i in range(len(test_str))
          for j in range(i + 1, len(test_str) + 1)]
  
# printing result 
print("All substrings of string are : " + str(res))

# -------------------------------------------------------------------------------------

s = 'ASFFaF233.DFF##$@&##'

print('True') if s.isupper() else print('False')







