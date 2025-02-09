#!/usr/bin/env python
"""
Simple reverse proxy using Flask and Requests.
For development only.
Install dependencies via:
    pip install flask requests
"""

from flask import Flask, request, Response
import requests

app = Flask(__name__)

def get_target():
    host = request.host.lower()
    # Use appropriate upstream based on host
    if host.startswith("www"):
        return "http://localhost:4000"
    elif host.startswith("app"):
        return "http://localhost:4001"

    # Default upstream target
    return "http://localhost:3000"

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
def proxy(path):
    target = get_target()
    url = f"{target}/{path}"
    if request.query_string:
        url = f"{url}?{request.query_string.decode('utf-8')}"

    # Forward headers except the Host header, but add x-forwarded headers
    headers = {key: value for key, value in request.headers if key.lower() != 'host'}
    
    # Add forwarding headers
    headers['x-forwarded-host'] = request.host
    headers['x-forwarded-proto'] = request.scheme
    headers['x-forwarded-for'] = request.remote_addr
    
    # If origin header exists, forward it
    if 'origin' in headers:
        headers['x-forwarded-origin'] = headers['origin']

    # Forward the request using the same method, data, and cookies.
    resp = requests.request(
        method=request.method,
        url=url,
        headers=headers,
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False,
        stream=True
    )

    # Exclude specific hop-by-hop response headers.
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    response_headers = [(name, value) for name, value in resp.raw.headers.items() if name.lower() not in excluded_headers]

    return Response(resp.content, resp.status_code, response_headers)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80) 