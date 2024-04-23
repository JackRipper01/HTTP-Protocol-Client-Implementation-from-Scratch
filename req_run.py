from HTTPClient import *

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
        options(host, port, path, headers, use_ssl = _use_ssl)
    print_linebold("\n!> end of request response")