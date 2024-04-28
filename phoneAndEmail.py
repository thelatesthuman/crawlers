#!python3

#Finds phone numbers and emails on webpage
import re
import requests
import pyinputplus as pyip

# Phone number Regex
phoneRegex = re.compile(r'''(
                        (\d{3}|\(\d{3}\))?              #Area code
                        (\s|\.|-)?                      #Separator
                        (\d{3})                         #First 3 digits
                        (\s|\.|-)                       #Separator
                        (\d{4})                         #Last 4 digits
                        (\s*|ext|ext.|x)\s*(\d{2,5})?   #Extension
                        )''', re.VERBOSE)

# Email Regex
emailRegex = re.compile(r'''(
                        [a-zA-Z0-9._%+-]+               #Username
                        @                               #@ symbol
                        [a-zA-Z0-9._%+-]+               #Domain
                        (\.[a-zA-Z]{2,4})               #Dot Something
                        )''',re.VERBOSE)
# Request webpage
try:    
    webpage = requests.get(pyip.inputStr("What webpage you want dawg? "))
    
    # Find matches in webpage
    text = webpage.text
    matches = []
    for groups in phoneRegex.findall(text):
        phoneNum = '-'.join([groups[1],groups[3],groups[5]])
        if groups[7] != '':
            phoneNum += ' x' + groups[7]
        matches.append(phoneNum)
    for groups in emailRegex.findall(text):
        matches.append(groups[0])

    # Print matches
    if len(matches) > 0:
        print('Matches found: ')
        print('\n'.join(matches))
    else:
        print('No phone numbers or emails found.')
except:
    print("Webpage not available.")
