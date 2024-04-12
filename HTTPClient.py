from socket import *

# Method to open a TCP connection, returns the tcp socket
def open_tcp_connection(port, host, retry_count=5):
    if retry_count == 0:
        raise Exception("All the retries to connect has been completed.")

    clientSocket = socket(AF_INET, SOCK_STREAM)  # Creating socket
    # clientSocket.settimeout(10) Set a timeout for the connection

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
    print("vvvvvvvvvvvvvvvvvvvvvRESPONSEvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv")
    raw_headers, raw_body = recv_res(sock)
    print(raw_headers)
    print("^^^^^^^^^^^^^^^^^^^headers^^^^^^^^^^^^^^^^^^^^^")
    return raw_headers, raw_body


# Receives the response headers from the server
def recv_res(sock: socket):
    return NotImplementedError


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
    print(msg)
    print("^^^^^^^^^^^^^^^^^^ My Request ^^^^^^^^^^^^^^^^^^")
    client_socket = open_tcp_connection(port=port, host=host)
    response = send_request(sock=client_socket, request=msg)
    client_socket.close()
    print(response)
    return response
