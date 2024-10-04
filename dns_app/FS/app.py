from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

AS_IP = None
AS_PORT = None
HOSTNAME = None
FS_IP = None

@app.route('/register', methods=['PUT'])
def register():
    global AS_IP, AS_PORT, HOSTNAME, FS_IP
    data = request.json
    HOSTNAME = data['hostname']
    FS_IP = data['ip']
    AS_IP = data['as_ip']
    AS_PORT = int(data['as_port'])

    # Register with AS
    message = f"TYPE=A\nNAME={HOSTNAME}\nVALUE={FS_IP}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (AS_IP, AS_PORT))
    sock.close()

    return "", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    try:
        n = int(number)
        result = calculate_fibonacci(n)
        return jsonify({"fibonacci": result}), 200
    except ValueError:
        return "Bad Request: 'number' must be an integer", 400

def calculate_fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
