import socket
import os

def udp_server(server_ip, server_port):
    # 创建一个UDP套接字
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        # 将套接字绑定到指定的IP地址和端口上
        server_socket.bind((server_ip, server_port))
        print(f"Server listening on {server_ip}:{server_port}")

        while True:
            # 接收数据和客户端地址
            data, client_address = server_socket.recvfrom(4096)  # 增大缓冲区大小

            # 如果没有数据，退出循环
            if not data:
                break

            # 解析文件名和文件大小信息
            file_name, file_size = data.decode().split(',')
            file_size = int(file_size)
            received_data = b''

            # 打印正在接收的文件信息
            print(f"Receiving {file_name} from {client_address[0]}:{client_address[1]}")

            # 循环接收文件数据
            while len(received_data) < file_size:
                chunk, addr = server_socket.recvfrom(4096)  #缓冲区
                received_data += chunk

            # 将接收到的文件写入本地
            with open(file_name, 'wb') as file:
                file.write(received_data)

            # 打印文件接收成功的信息
            print(f"File {file_name} received successfully.")

    except KeyboardInterrupt:
        # 用户通过Ctrl+C中断程序
        print("Server stopped by user.")
    finally:
        # 关闭服务器套接字
        server_socket.close()

if __name__ == "__main__":
    # 配置服务器的IP地址和端口号
    server_ip = "192.168.16.131"  # 虚拟机IP地址
    server_port = 12345

    # 启动UDP服务器
    udp_server(server_ip, server_port)
    """
    这是一个基于UDP协议的文件传输服务器端程序,用于接收客户端发送的文件。运行环境:Python 3.x,在Windows、Linux 或 macOS上
    
    配置选项：
    虚拟机 IP 地址： 将 server_ip 变量设置为服务器的虚拟机 IP 地址。例如,server_ip = "192.168.16.131"
    服务器端口号： 将 server_port 变量设置为服务器监听的端口号。例如,server_port = 12345
    
    运行程序：
    在终端或命令行界面中执行以下命令以启动服务器：
    python3 transUDP.py
    在程序运行期间，可以通过 Ctrl+C 中断程序。
    """
