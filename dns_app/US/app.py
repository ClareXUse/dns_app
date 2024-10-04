from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

@app.route('/fibonacci')
def fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request: Missing parameters", 400

    # Query AS for IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=A\nNAME={hostname}\n"
    sock.sendto(message.encode(), (as_ip, int(as_port)))
    data, _ = sock.recvfrom(1024)
    response = data.decode().split('\n')
    fs_ip = None
    for line in response:
        if line.startswith('VALUE='):
            fs_ip = line.split('=')[1]
            break
    sock.close()

    if not fs_ip:
        return "Not Found: Could not resolve hostname", 404

    # Query FS for Fibonacci number
    try:
        fs_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
        response = requests.get(fs_url)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return f"Error from FS: {response.text}", response.status_code
    except requests.RequestException as e:
        return f"Error connecting to FS: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)