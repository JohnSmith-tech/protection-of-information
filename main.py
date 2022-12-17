from server import Server
from node import Node


if __name__ == "__main__":
    server = Server()
    client1 = Node(1, server=server, answer=1)
    client2 = Node(2, server=server, answer=2)
    client3 = Node(3, server=server, answer=3)
    client4 = Node(3, server=server, answer=1)
    client5 = Node(5, server=server, answer=2)