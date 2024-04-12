from HTTPClient import *
from urllib.parse import urlparse

def process_text_short(splitted_text):

    op = ""
    host = ""
    path = ""
    headers = {}
    body = ""
    additional_headers = False
    ended = False

    # get op

    if splitted_text[0] == '':
        print("!> no operation provided")
    elif (splitted_text[0].strip()).upper() not in [
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "TRACE",
        "CONNECT",
        "OPTIONS",
        "GET+",
        "HEAD+",
        "POST+",
        "PUT+",
        "DELETE+",
        "TRACE+",
        "CONNECT+",
        "OPTIONS+",
    ]:
        print("!> invalid operation")
    else:
        op = (splitted_text[0].strip()).upper()
        
        if str(op).endswith('+'):
            op = op[:-1]
            additional_headers = True

        # get host
        if 1 >= len(splitted_text):
            print("!> invalid host")
        else:
            host = splitted_text[1].strip()

            # get path

            if 2 >= len(splitted_text):
                print("!> invalid path")
            else:
                path = splitted_text[2].strip()

                ended = True

                # get headers
                if 3 >= len(splitted_text):
                    print("!> not passing headers inline, neither body")
                else:
                    try:
                        headers = eval(splitted_text[3].strip())
                    except:
                        print("!> invalid headers")

                    # get body
                    if 4 >= len(splitted_text):
                        print("!> not passing body")
                    else:
                        body = splitted_text[4].strip()
                        headers["Content-length"] = str(len(body))

    if additional_headers:
        headers['User-Agent'] = "MyHTTPClient/1.0 (Python) Sockets/ Python/31"
        headers['Connection'] = "keep-alive"
    print("AAAAAAAAAAAAAAAAAAAAAAAa")
    print(headers)
    return op, host, path, headers, body, ended

def process_text_long(splitted_text):

    op = ""
    host = ""
    path = ""
    headers = {}
    body = ""
    additional_headers = False
    ended = False

    # get op

    if splitted_text[0] == '':
        print("!!> no operation provided")
    elif (splitted_text[0].strip()).upper() not in [
        "GET",
        "HEAD",
        "POST",
        "PUT",
        "DELETE",
        "TRACE",
        "CONNECT",
        "OPTIONS",
        "GET+",
        "HEAD+",
        "POST+",
        "PUT+",
        "DELETE+",
        "TRACE+",
        "CONNECT+",
        "OPTIONS+",
    ]:
        print("!!> invalid operation")
    else:
        op = (splitted_text[0].strip()).upper()
        
        if str(op).endswith('+'):
            op = op[:-1]
            additional_headers = True

        # get host and path
        if 1 >= len(splitted_text):
            print("!!> invalid url")
        else:
            url = splitted_text[1].strip()
            
            urlparts = urlparse(url)
            
            host = str(urlparts.hostname)
            path = str(urlparts.path)

            if urlparts.scheme == 'https':
                print("!!> https not suported")
            else:
                ended = True

                # get headers
                if 2 >= len(splitted_text):
                    print("!!> not passing headers inline, neither body")
                else:
                    try:
                        headers = eval(splitted_text[3].strip())
                    except:
                        print("!!> invalid headers")
                    # get body
                    if 3 >= len(splitted_text):
                        print("!!> not passing body")
                    else:
                        body = splitted_text[4].strip()
                        headers["Content-length"] = str(len(body))

    if additional_headers:
        headers['User-Agent'] = "MyHTTPClient/1.0 (Python) Sockets/ Python/31"
        headers['Connection'] = "keep-alive"

    return op, host, path, headers, body, ended

def run_req(op: str, host, path, headers, body):
    if op == "GET":
        get(host, path, headers)
    elif op == "HEAD":
        head(host, path, headers)
    elif op == "POST":
        post(host, path, headers, body)
    elif op == "PUT":
        put(host, path, headers, body)
    elif op == "DELETE":
        delete(host, path, headers)
    elif op == "TRACE":
        trace(host, path, headers)
    elif op == "CONNECT":
        connect(host, path, headers)
    elif op == "OPTIONS":
        options(host, path, headers)

def long():
    splitted_text = [""]
    print("!!> (long) session opened")
    while True:

        print('??> ',end = '')

        text = input()
        splitted_text = text.split(";", 3)

        if splitted_text[0] == "e":
            break
        if splitted_text[0] == "ls":
            short()
            break

        op, host, path, headers, body, correct = process_text_long(splitted_text)
        if not correct:
            continue
        print("!!> running "+op+" request to '"+host+"', with path '"+ path+"'")
        run_req(op, host, path, headers, body)

    print("!!> session closed")

def short():
    splitted_text = [""]
    print("!> (short) session opened")
    while True:

        print('?> ',end = '')

        text = input()
        splitted_text = text.split(";", 4)

        if splitted_text[0] == "e":
            break
        if splitted_text[0] == "ls":
            long()
            break

        op, host, path, headers, body, correct = process_text_short(splitted_text)
        if not correct:
            continue
        print("!> running "+op+" request to '"+host+"', with path '"+ path+"'")
        run_req(op, host, path, headers, body)

    print("!> session closed")

if __name__ == "__main__":
    short()