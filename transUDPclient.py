import socket
import os
import sys

def send_file(client_socket, server_ip, server_port, file_path):
    """
    辅助函数：递归地发送文件或文件夹到服务器。

    Parameters:
    - client_socket (socket): 客户端套接字。
    - server_ip (str): 服务器的IP地址。
    - server_port (int): 服务器的端口号。
    - file_path (str): 要传输的文件或文件夹的本地路径。
    """
    if os.path.isfile(file_path):
        # 如果是文件，发送文件
        send_single_file(client_socket, server_ip, server_port, file_path)
    elif os.path.isdir(file_path):
        # 如果是文件夹，递归地发送文件夹中的所有文件
        for root, dirs, files in os.walk(file_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                send_single_file(client_socket, server_ip, server_port, file_path)

def send_single_file(client_socket, server_ip, server_port, file_path):
    """
    辅助函数：发送单个文件到服务器。

    Parameters:
    - client_socket (socket): 客户端套接字。
    - server_ip (str): 服务器的IP地址。
    - server_port (int): 服务器的端口号。
    - file_path (str): 要传输的文件的本地路径。
    """
    try:
        # 获取文件名和文件大小
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        # 发送文件名和文件大小信息到服务器
        client_socket.sendto(f"{file_name},{file_size}".encode(), (server_ip, server_port))

        # 打开文件并逐块发送数据
        with open(file_path, 'rb') as file:
            data = file.read(1024)
            while data:
                client_socket.sendto(data, (server_ip, server_port))
                data = file.read(1024)

        # 文件发送成功的提示
        print(f"File {file_name} sent successfully.")

    except FileNotFoundError:
        # 处理文件未找到的错误
        print(f"Error: File not found at {file_path}")

def udp_client(server_ip, server_port, file_path):
    """
    客户端通过UDP协议传输文件或文件夹到指定的服务器。

    Parameters:
    - server_ip (str): 服务器的IP地址。
    - server_port (int): 服务器的端口号。
    - file_path (str): 要传输的文件或文件夹的本地路径。
    """

    # 创建一个UDP套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 判断是文件还是文件夹，并发送到服务器
        send_file(client_socket, server_ip, server_port, file_path)

    finally:
        # 关闭套接字
        client_socket.close()

if __name__ == "__main__":
    # 检查命令行参数或获取用户输入
    if len(sys.argv) != 4:
        server_ip = input("Enter server IP: ")
        server_port = int(input("Enter server port: "))
        file_path = input("Enter file or folder path: ")
    else:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        file_path = sys.argv[3]

    # 调用客户端函数传输文件或文件夹
    udp_client(server_ip, server_port, file_path)
"""
这是一个基于UDP协议的文件传输客户端程序,用于将文件或文件夹发送到服务器。

运行环境:
Python 3.x
在 Windows、Linux 或 macOS 上

配置选项：
虚拟机 IP 地址： 将 server_ip 变量设置为服务器的虚拟机 IP 地址。例如, server_ip = "192.168.16.131"
服务器端口号： 将 server_port 变量设置为服务器监听的端口号。例如, server_port = 12345

运行程序：
在终端或命令行界面中执行以下命令以启动客户端：
python3 transUDPclient.py  server_ip  server_port   file_path
在程序运行期间，可以通过 Ctrl+C 中断程序。
"""