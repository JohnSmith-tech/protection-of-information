from sympy import randprime, isprime
from methods_for_crypto.methods import *
import random
import hashlib
from server import Server


class Node:

    def __init__(self, id, server: Server, answer: int) -> None:
        self.rnd = random.getrandbits(512)
        self.r = random.randint(0, 1 << 1024)
        while gcd(self.r, server.n) != 1:
            self.r = random.randint(2, server.N)

        self.n = int(str(self.rnd << 512) + str(answer))

        h = int(hashlib.sha3_256(repr(self.n).encode()).hexdigest(), 16) % self.n
        self.h2 = h * exp_mod(self.r, server.d, server.n) % server.n

        s = server.request_for_get_bullet(id, self.h2)
        if s == -1:
            print("Response from the server: User has already voted")
            return

        eval_signature = s * \
            euclidean_algorithm(self.r, server.n)[1] % server.n
        response = 'correct' if server.send_data(
            self.n, eval_signature) else 'not correct'
        print(f'Response from the server: Bulletin is {response}')
