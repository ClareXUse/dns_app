import socket
import json

DNS_FILE = 'dns_records.json'


def load_dns_records():
    try:
        with open(DNS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_dns_records(records):
    with open(DNS_FILE, 'w') as f:
        json.dump(records, f)


def handle_registration(data):
    lines = data.split('\n')
    record = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=')
            record[key] = value

    dns_records = load_dns_records()
    dns_records[record['NAME']] = record
    save_dns_records(dns_records)


def handle_query(data):
    lines = data.split('\n')
    query = {}
    for line in lines:
        if '=' in line:
            key, value = line.split('=')
            query[key] = value

    dns_records = load_dns_records()
    if query['NAME'] in dns_records:
        record = dns_records[query['NAME']]
        return f"TYPE={record['TYPE']}\nNAME={record['NAME']}\nVALUE={record['VALUE']}\nTTL={record['TTL']}\n"
    else:
        return "Error: not found"


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))

    print("AS is running on port 53533...")

    while True:
        data, addr = server_socket.recvfrom(1024)
        message = data.decode()

        if 'TYPE=A' in message and 'NAME' in message and 'VALUE' in message and 'TTL' in message:
            handle_registration(message)
            server_socket.sendto(b"Registration successful", addr)
        elif 'TYPE=A' in message and 'NAME' in message:
            response = handle_query(message)
            server_socket.sendto(response.encode(), addr)
        else:
            server_socket.sendto(b"Invalid request", addr)


if __name__ == '__main__':
    main()