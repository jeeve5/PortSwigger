#! /usr/bin/env python 

import requests #to make web requests
import sys  #system module to use for arguments

def exploit(base_url: str) -> None:
    pass

def main() -> None:
    if len(sys.argv)!= 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    exploit(sys.argv[1].rstrip("/"))
    
if __name__ =="__main__":
    main()
        