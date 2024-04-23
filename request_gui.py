from tkinter import *
from tkinter.ttk import *
from tkinter import scrolledtext
from HTTPClient import *
import subprocess

root = Tk()
root.title("cliente http")
root.geometry('500x311')

available_operations=[
"GET",
"HEAD",
"POST",
"PUT",
"DELETE",
"TRACE",
"CONNECT",
"OPTIONS"
]

opdrop=StringVar(root,'GET','GET')

drop = OptionMenu(root, opdrop,'GET',*available_operations) 
drop.grid(column=0,row=0)

url_entry = Entry(root,name='asdasfas', width = 37)
url_entry.grid(column = 1, row = 0)
url_entry.insert(INSERT, 'https://google.com:443')

header_entry = scrolledtext.ScrolledText(root, width = 70, height = 7)
header_entry.grid(column = 0,columnspan=230, row = 1)
header_entry.insert(INSERT, "{\n")
header_entry.insert(INSERT, "'User-Agent': 'Mozilla/5.0',\n")
header_entry.insert(INSERT, "'Connection': 'keep-alive'\n")
header_entry.insert(INSERT, "}")

body_entry = scrolledtext.ScrolledText(root, width = 70, height = 7)
body_entry.grid(column = 0,columnspan=230, row = 2)
body_entry.insert(INSERT, "<html>\n")
body_entry.insert(INSERT, "	<head><title>página de ejemplo</title></head>\n")
body_entry.insert(INSERT, "	<body>\n")
body_entry.insert(INSERT, "	recomendado borrar esto antes de hacer el request\n")
body_entry.insert(INSERT, "	en caso de no ser necesario este apartado\n")
body_entry.insert(INSERT, "	</body>\n")
body_entry.insert(INSERT, "</html>")

def parse_app():
    op = opdrop.get().strip()
    url = url_entry.get().strip()
    urlData=urlparse(url)
    host=urlData.hostname
    use_ssl = urlData.scheme == 'https'
    if host==None:
        raise Exception("could not resolve hostname")
    path = '/'
    if urlData.path!='':
        path=urlData.path
    port = 80
    if use_ssl:
        port = 443
    if urlData.port != None:
        port=urlData.port

    headers = {}

    try:
        headers=eval(header_entry.get("1.0",'end-1c'))
        if not (type(headers) is dict):
            headers = {}
            raise Exception(type(headers)+" no coincide con dict")
    except Exception as e:
        print("!> error parsing or evaluating Headers", e)
    
    body = body_entry.get("1.0",'end-1c').strip()
    if len(body)!=0:
        headers["Content-length"] = str(len(body))

    return op, host, port, path, headers, body, use_ssl

def erase_content_length(headers_c: dict):
    if 'Content-length' in headers_c.keys():
        headers_c.pop('Content-length')

def run_req(op: str, host, port, path, headers, body, _use_ssl):
    if op == "GET":
        erase_content_length(headers)
        get(host, port, path, headers, use_ssl = _use_ssl)
    elif op == "HEAD":
        erase_content_length(headers)
        head(host, port, path, headers, use_ssl = _use_ssl)
    elif op == "POST":
        post(host, port, path, headers, body, use_ssl = _use_ssl)
    elif op == "PUT":
        put(host, port, path, headers, body, use_ssl = _use_ssl)
    elif op == "DELETE":
        erase_content_length(headers)
        delete(host, port, path, headers, use_ssl = _use_ssl)
    elif op == "TRACE":
        erase_content_length(headers)
        trace(host, port, path, headers, use_ssl = _use_ssl)
    elif op == "CONNECT":
        erase_content_length(headers)
        connect(host, port, path, headers, use_ssl = _use_ssl)
    elif op == "OPTIONS":
        erase_content_length(headers)
        print(options)
        options(host, port, path, headers, use_ssl = _use_ssl)

def clicked():
    try:
        subprocess.run('cls',check=True)
    except:
        subprocess.run('clear', check= True)

    op = host = port = path = headers = body = use_ssl = None

    try:
        op, host, port, path, headers, body, use_ssl = parse_app()

        try:
            print("!> running", "OP:", op, "| Host:", host, "| Port:", port, "| Path:", path, "| SSL:", use_ssl)
            if len(headers.keys())>0:
                    print("!>  Added Headers:",headers)
            if len(body)>0:
                    print("!>  Body:\n",body)
            run_req(op,host,port,path,headers,body, use_ssl)
            print("\n!> end of request response")
        except Exception as e:
            print("!> error while running request")
            print("!> details:", e)
            #traceback.print_exc()

    except Exception as e:
        print("!> parse error")
        print("!> details:",e)

btn = Button(root, text = "send", command = clicked)
btn.grid(column = 3, row = 0)

url_entry.focus()

root.mainloop()