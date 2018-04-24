import socket
import struct
import sys
from random import randint 
from time import sleep

multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(1)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 2)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
def send(msg):
    try:
        # Send data to the multicast group
        sent = sock.sendto(msg.encode("utf-8"), multicast_group)

        # Look for responses from all recipients
        # while True:
        #     print('waiting to receive')
        #     try:
        #         data, server = sock.recvfrom(1024)
        #     except socket.timeout:
        #         print('timed out, no more responses')
        #         break
        #     else:
        #         print('received "%s" from %s' % (data, server))
    finally:
        print('closing socket')
        sock.close()

numbers = list(range(1, 76))
sorteados = []

def sorteio():
    if len(numbers) > 0:
        sorteado = randint(0, len(numbers)-1)
        sorteados.append(numbers[sorteado])
        numbers.remove(numbers[sorteado])

while len(numbers) > 0:
    sorteio()
    sent = sock.sendto(str(sorteados).encode("utf-8"), multicast_group)
    try:
        data, server = sock.recvfrom(1024)
        print("Ganhador: {}".format(server))
        numbers = []
    except socket.timeout:
        continue
else:
    send('fim')

