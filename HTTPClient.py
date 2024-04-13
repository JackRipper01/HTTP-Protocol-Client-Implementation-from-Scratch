from socket import *
from urllib.parse import urlparse
from time import sleep
import ssl
# Method to open a TCP connection, returns the tcp socket
def open_tcp_connection(port, host, retry_count=0):
    if retry_count == 6:
        raise Exception("All the retries to connect has been completed unsuccessfully.")

    clientSocket = socket(AF_INET, SOCK_STREAM)  # Creating socket
    clientSocket.settimeout(10) #Set a timeout for the connection

    context=ssl.create_default_context()
    clientSocket=context.wrap_socket(sock=clientSocket,server_hostname=host)
    
    try:
        clientSocket.connect((gethostbyname(host), port))
        print("\n!> TCP CONNECTION OPENED")
        print(f'!>  The connection is secure and using {clientSocket.cipher()}\n') 
    except timeout:
        print("Connection TimeOut. Retrying connection.")
        sleep(2^retry_count)
        return open_tcp_connection(port=port, host=host, retry_count=retry_count + 1)
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


def send_http(path, headers={}, port=443, method="GET", host="localhost", body="",counter=5):
    version = "HTTP/1.1"
    msg = get_http_msg(
        path=path, headers=headers, method=method, host=host, body=body, version=version
    )
    print()
    print("!> REQUEST MESSAGE")
    print(msg)
    client_socket = open_tcp_connection(port=port, host=host)
    head,res_body = send_request(sock=client_socket, request=msg)
    client_socket.close()
    print('!>RESPONSE')
    print("!>  HEADERS")
    print(head,"\n")
    print("!>  BODY")
    print(res_body)
    res_headers=get_headers_from_res_headers(head)
    if counter>0 and str(res_headers['Status']).startswith('3'):
        url_parsed=urlparse(res_headers['Location'])
        print('!> redirectioning...')
        return send_http(path=url_parsed.path,headers=headers,port=port,method=method,host=url_parsed.hostname,body=body,counter=counter-1)
    return head,res_body

def get(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method='GET',host=host, port = port)
def head(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method='HEAD',host=host, port = port)
def post(host, port, path,headers={},body=''):
    return send_http(path=path,headers=headers,method='POST',host=host,body=body, port = port)
def put(host, port, path,headers={},body=''):
    return send_http(path=path,headers=headers,method='PUT',host=host,body=body, port = port)
def delete(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method="DELETE",host=host, port = port)
def trace(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method='TRACE',host=host, port = port)
def connect(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method='CONNECT',host=host, port = port)
def options(host, port, path,headers={}):
    return send_http(path=path,headers=headers,method='CONNECT',host=host, port = port)

if __name__=='__main__':
    send_http(path='/',method='GET',host='www.google.com',port=443)