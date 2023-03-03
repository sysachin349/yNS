import re

percentage_regex = re.compile(r'\d{1,3}\.?\d{0,2}%')

string = "1000%"

print(str(string).replace('%',''))
    
