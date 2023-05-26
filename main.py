import random
import socket
import datetime
import sys

def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 43234))

    print("Server started")

    while True:
        print()
        m, a = sock.recvfrom(1024)

        print(f"Connection: {a}\nMessage: {m.decode()}")

        lost = random.randint(0, 100) > 10
        if lost:
            print("Sent\n")
            sock.sendto(m.upper(), a)
        else:
            print("Loss\n")

        print(f"Connection closed\n")

def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.settimeout(1.0)

    lost = 0
    sum = 0
    
    mx = 0
    mn = int(1e9)

    for pings in range(1, 11):
        print()
        
        time = datetime.datetime.now()
        sock.sendto(f"Ping {pings} {datetime.datetime.now().time()}".encode(), ("127.0.0.1", 43234))
        try:
            response, err = sock.recvfrom(1024)
            timenow = datetime.datetime.now()
        
            sum += (timenow - time).microseconds
            mx = max(mx, (timenow - time).microseconds)
            mn = min(mn, (timenow - time).microseconds)

            print(f"Response: {response.decode()}\n")
        except socket.timeout:
            print("It seems that the package has been lost\n")
            lost += 1

    print(f"\nLost: {lost} from 10\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] == 'client':
        start_client()
    elif args[0] == 'server':
        start_server()

