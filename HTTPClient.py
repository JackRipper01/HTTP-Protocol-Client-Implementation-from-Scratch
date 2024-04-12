from socket import *

# Method to open a TCP connection, returns the tcp socket
def open_tcp_connection(port, host, retry_count=5):
    if retry_count == 0:
        raise Exception("All the retries to connect has been completed.")

    clientSocket = socket(AF_INET, SOCK_STREAM)  # Creating socket
    clientSocket.settimeout(10) #Set a timeout for the connection

    try:
        clientSocket.connect((gethostbyname(host), port))
    except timeout:
        print("Connection TimeOut. Retrying connection.")
        return open_tcp_connection(port=port, host=host, retry_count=retry_count - 1)
    except error as e:
        raise Exception(f"Error connecting to server: {e}")
    except Exception as e:
        raise Exception(f"An unexpected error has ocurred. {e}")
    print(
        "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!tcp connection has been opened!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    )
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


def send_http(path, headers={}, port=80, method="GET", host="localhost", body=""):
    version = "HTTP/1.1"
    msg = get_http_msg(
        path=path, headers=headers, method=method, host=host, body=body, version=version
    )
    print("VVVVVVVVVVVVVVV My Request VVVVVVVVVVVVVVV")
    print(msg)
    client_socket = open_tcp_connection(port=port, host=host)
    head,res_body = send_request(sock=client_socket, request=msg)
    client_socket.close()
    print('VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV RESPONSE VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV')
    print("VVVVVVVVVVVVVVV HEADERS VVVVVVVVVVVVVVV")
    print(head)
    print("VVVVVVVVVVVVVVV BODY VVVVVVVVVVVVVVV")
    print(res_body)
    return head,res_body

def get(host,path,headers={}):
    return send_http(path=path,headers=headers,method='GET',host=host)
def head(host,path,headers={}):
    return send_http(path=path,headers=headers,method='HEAD',host=host)
def post(host,path,headers={},body=''):
    return send_http(path=path,headers=headers,method='POST',host=host,body=body)
def put(host,path,headers={},body=''):
    return send_http(path=path,headers=headers,method='PUT',host=host,body=body)
def delete(host,path,headers={}):
    return send_http(path=path,headers=headers,method="DELETE",host=host)
def trace(host,path,headers={}):
    return send_http(path=path,headers=headers,method='TRACE',host=host)
def connect(host,path,headers={}):
    return send_http(path=path,headers=headers,method='CONNECT',host=host)
def options(host,path,headers={}):
    return send_http(path=path,headers=headers,method='CONNECT',host=host)
