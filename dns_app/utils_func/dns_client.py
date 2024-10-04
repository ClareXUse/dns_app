import socket
import sys


def register_dns():
    # 创建注册消息
    message = "TYPE=A\nNAME=fibonacci.com\nVALUE=172.18.0.2\nTTL=10\n"

    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 向 AS 容器发送消息（假设 AS 运行在本地 127.0.0.1，端口 53533）
    sock.sendto(message.encode(), ("127.0.0.1", 53533))

    # 接收回复
    data, _ = sock.recvfrom(1024)
    print("Registration Response:", data.decode())

    # 关闭 socket
    sock.close()


def query_dns():
    # 创建查询消息
    message = "TYPE=A\nNAME=fibonacci.com\n"

    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 向 AS 容器发送消息（假设 AS 运行在本地 127.0.0.1，端口 53533）
    sock.sendto(message.encode(), ("127.0.0.1", 53533))

    # 接收回复
    data, _ = sock.recvfrom(1024)
    print("Query Response:", data.decode())

    # 关闭 socket
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python dns_client.py <register|query>")
        sys.exit(1)

    action = sys.argv[1]

    if action == 'register':
        register_dns()
    elif action == 'query':
        query_dns()
    else:
        print("Invalid action. Use 'register' or 'query'.")
        sys.exit(1)
