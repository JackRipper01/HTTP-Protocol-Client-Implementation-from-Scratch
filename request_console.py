from HTTPClient import *
from urllib.parse import urlparse
import re

def parse_prompt(prompt: str):
    get_op_re = r"GET|HEAD|POST|PUT|DELETE|TRACE|CONNECT|OPTIONS"
    
    op = re.search(get_op_re,prompt,re.IGNORECASE)
    
    if op == None:
        raise Exception("could not find OP")
    op=op[0]
    prompt = prompt.replace(op,"", 1).strip()+" "

    get_url_re = r"^[^\s]*(?=\s)"
    url = re.search(get_url_re, prompt)
    if url == None:
        raise Exception("could not find URL")
    url=url[0]
    urlData=urlparse(url)
    host=urlData.hostname
    if host==None:
        raise Exception("could not resolve hostname")
    path = '/'
    if urlData.path!='':
        path=urlData.path
    port=443
    if urlData.port != None:
        port=urlData.port

    prompt = prompt.replace(url,"", 1).strip()+" "
    
    get_headers_re=r"^{[^{}]*}(?=\s)"
    headers={}
    body=''
    headers_string=re.search(get_headers_re, prompt)
    if headers_string==None:
        print("!> could not find headers")
        body=prompt.strip()
    else:
        headers_string=headers_string[0]
        try:
            headers=eval(headers_string)
            if not (type(headers) is dict):
                raise Exception(type(headers)+" no coincide con dict")
            body = prompt.replace(headers_string,"", 1).strip()
            if len(body)!=0:
                headers["Content-length"] = str(len(body))
        except:
            print("!> Error evaluating Headers:") 
            print(headers_string)

    return op.upper(), host, path, port, headers, body

def run_req(op: str, host, port, path, headers, body):
    if op == "GET":
        get(host, port, path, headers)
    elif op == "HEAD":
        head(host, port, path, headers)
    elif op == "POST":
        post(host, port, path, headers, body)
    elif op == "PUT":
        put(host, port, path, headers, body)
    elif op == "DELETE":
        delete(host, port, path, headers)
    elif op == "TRACE":
        trace(host, port, path, headers)
    elif op == "CONNECT":
        connect(host, port, path, headers)
    elif op == "OPTIONS":
        options(host, port, path, headers)

def run_time():
    print("!> session opened")
    while True:
        op = host = port = path = headers = body = None
        print('?> ',end = '')

        text = input()

        if text == "e":
            break
        try:
            op, host, path, port, headers, body = parse_prompt(text)
            
            try:
                print("!> running","OP:",op,"| Host:",host,"| Port:",port,"| Path:",path)
                if len(headers.keys())>0:
                    print("!>  Added Headers:",headers)
                if len(body)>0:
                    print("!>  Body:\n",body)
            
                run_req(op, host, port, path, headers, body)
            except Exception as e:
                print("!> error while running request")
                print("!> details:",e)
            
        except Exception as e:
            print('!> parsing error')
            print("!> details:",e)
        
        
    print("!> session closed")

if __name__ == "__main__":
    run_time()
