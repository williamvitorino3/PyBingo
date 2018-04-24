import socket
import struct
import sys
from random import randint 


def gerar_cartela():
    numbers = list(range(1, 76))
    sorteados = []
    for i in range(25):
        pos = randint(0, len(numbers)-1)
        sorteados.append(numbers[pos])
        numbers.remove(numbers[pos])
    return sorteados

multicast_group = '224.3.29.71'
server_address = (input("Endereço do servidor: "), 10000)
cartela = gerar_cartela()
print(cartela)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
sock.settimeout(60)

# Receive/respond loop
while True:
    try: 
        data, address = sock.recvfrom(1024)
    except socket.timeout:
        break
    if(data.decode("utf-8") == "fim"): break
    pedras = list(map(int, data.decode("utf-8")[1 : -1].split(", ")))
    for i in pedras:
        if i in cartela:
            cartela.remove(i)
            print(cartela)
    print(pedras[-1])

    if len(cartela) == 0:
      sock.sendto('ganhei'.encode("utf-8"), address)  

    # print('sending acknowledgement to', address)
    # sock.sendto('ack'.encode("utf-8"), address)
else:
    sock.close()