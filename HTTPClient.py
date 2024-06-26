from socket import *
from urllib.parse import urlparse
from time import sleep
import ssl
from coloring import *

#import traceback

# Method to open a TCP connection, returns the tcp socket
def open_tcp_connection(port, host, retry_count=0, use_ssl = True):
    if retry_count == 6:
        raise Exception("All the retries to connect has been completed unsuccessfully.")

    clientSocket = socket(AF_INET, SOCK_STREAM)  # Creating socket
    clientSocket.settimeout(10) #Set a timeout for the connection

    if use_ssl:
        context=ssl.create_default_context()
        clientSocket=context.wrap_socket(sock=clientSocket,server_hostname=host)
    
    try:
        clientSocket.connect((gethostbyname(host), port))
        print_success("\n!> TCP CONNECTION OPENED")
        if use_ssl:
            print_success(f'!>  The connection is secure and using {clientSocket.cipher()}\n') 
    except timeout:
        print_warning("Connection TimeOut. Retrying connection.")
        sleep(2^retry_count)
        return open_tcp_connection(port=port, host=host, retry_count=retry_count + 1,use_ssl=use_ssl)
    except error as e:
        raise Exception(f"Error connecting to server: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error has ocurred. {e}")
    
    return clientSocket


# Method to send a TCP message
def send_request(sock: socket, request: str):
    # sends the request to the server throught the connected socket.
    sock.send(request.encode())
    raw_headers, raw_body = recv_res(sock)
    return raw_headers, raw_body

# Parses the response headers to a dict and adds the key_value 'Status': status_int
def get_headers_from_res_headers(res_headers:str):
    lines = res_headers.split("\r\n")
    headers = {}
    # print(lines[0].split(' ')[1])
    for i in range(len(lines)):
        if i==0:
            headers['Status']=int(lines[i].split(' ')[1])
        elif ": " in lines[i]:
            header,val = lines[i].split(": ",1)
            headers[header] = val
    return headers

# Receives the response headers from the server
def recv_res(sock: socket):
    response = ''
    while(not response.endswith('\r\n\r\n')):
        byte=sock.recv(1)
        if not byte: break
        response+=byte.decode()
    # print(response)
    headers=get_headers_from_res_headers(response)
    if 'Content-Length' in headers:
        body = sock.recv(int(headers['Content-Length']))
        response +=body.decode()
    elif 'Transfer-Encoding' in headers:
        if headers['Transfer-Encoding'] == 'chunked':
            chunk=''
            while not chunk.endswith('\r\n0'):
                chunk_bytes=sock.recv(1)
                try:
                    decoded=chunk_bytes.decode()
                    chunk+=decoded
                except:
                    pass    
            response+=chunk
    if response:
        head_body=response.split('\r\n\r\n',1)
        head=head_body[0]
        body=head_body[1]
        return head,body
    else:
        return "ERROR","ERROR"



# Method to form an http message
def get_http_msg(path, headers, method, host, body, version):
    rhost = f"{host}"
    rpath = path
    rpath = parse_to_str(path)
    rheaders = parse_to_str(headers)
    return f"{method} {rpath} {version}\r\nHost: {rhost}{rheaders}\r\n\r\n{body}"


def parse_to_str(input):
    if type(input) == str:
        return input
    return format_iter(input, type(input) == dict)


def format_iter(iter, isdict=False):
    rpath = ""
    for e in iter:
        if isdict:
            rpath += f"\r\n{e}: {iter[e]}"
        else:
            rpath += f"/{e}"
    return rpath


def send_http(path, headers={}, port=443, method="GET", host="localhost", body="",counter=5, use_ssl = True):
    version = "HTTP/1.1"
    msg = get_http_msg(
        path=path, headers=headers, method=method, host=host, body=body, version=version
    )

    print_header("\n!> REQUEST MESSAGE")
    print(msg)
    client_socket = open_tcp_connection(port=port, host=host, use_ssl = use_ssl)
    head,res_body = send_request(sock=client_socket, request=msg)
    client_socket.close()

    res_headers=get_headers_from_res_headers(head)

    print_header('!>RESPONSE')
    print_header("!>  HEADERS")

    if str(res_headers['Status']).startswith('2'): 
        print_OK_200(head,"\n")
    elif str(res_headers['Status']).startswith('3'):
        print_warn_300(head,"\n")
    elif str(res_headers['Status']).startswith('4'):
        print_fail_400(head,"\n")
    else:
        print_fail_400(head,"\n")

    print_header("!>  BODY")
    print(res_body)
    
    if counter>0 and str(res_headers['Status']).startswith('3'):
        url_parsed=urlparse(res_headers['Location'])
        print_linebold("\n!> redirecting to:", bcolors.UNDERLINE+res_headers['Location'])
        #print(url_parsed.path,'\n',headers,'\n',port,'\n', url_parsed.hostname, '\n', body, '\n', counter)
        return send_http(path=url_parsed.path,headers=headers,port=port,method=method,host=url_parsed.hostname,body=body,counter=counter-1, use_ssl= use_ssl)
    return head,res_body

def get(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method='GET',host=host, port = port, use_ssl = use_ssl)
def head(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method='HEAD',host=host, port = port, use_ssl = use_ssl)
def post(host, port, path,headers={},body='', use_ssl = True):
    return send_http(path=path,headers=headers,method='POST',host=host,body=body, port = port, use_ssl = use_ssl)
def put(host, port, path,headers={},body='', use_ssl = True):
    return send_http(path=path,headers=headers,method='PUT',host=host,body=body, port = port, use_ssl = use_ssl)
def delete(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method="DELETE",host=host, port = port, use_ssl = use_ssl)
def trace(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method='TRACE',host=host, port = port, use_ssl = use_ssl)
def connect(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method='CONNECT',host=host, port = port, use_ssl = use_ssl)
def options(host, port, path,headers={}, use_ssl = True):
    return send_http(path=path,headers=headers,method='OPTIONS',host=host, port = port, use_ssl = use_ssl)

if __name__=='__main__':
    send_http(path='/',method='GET',host='google.com',port=443)