import socket, time, sys
from multiprocessing import Process

def get_remote_ip(host):
    print("Getting ip for " + host)
    try:
        remote_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Hostname could not be resolved, exiting")
        sys.exit()
    print("Ip address of " + host + " is " + remote_ip)
    return remote_ip

def handle_request(conn, addr, proxy_end):
    send_full_data = conn.recv(BUFFER_SIZE)
    print("Sending received data " + send_full_data.decode("utf-8") + " to google")
    proxy_end.sendall(send_full_data)
    proxy_end.shutdown(socket.SHUT_WR)
    
    data = proxy_end.recv(BUFFER_SIZE)
    print("Sending received data " + data.decode("utf-8") + " to client")
    conn.send(data)

def main():
    host = "www.google.com"
    port = 80
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)
        while True:
            conn, addr = proxy_start.accept()
            print("Connected by", addr)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to google")
                remote_ip = get_remote_ip(host)
                
                proxy_end.connect((host, port))
                p = Process(target=handle_echo, args=(addr,conn))
                p.daemon = True
                p.start()
                print("Started process ", p)
                
            conn.close()
            
if __name__ == "__main__":
    main()