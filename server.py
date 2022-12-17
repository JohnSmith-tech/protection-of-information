from sympy import randprime, isprime
from methods_for_crypto.methods import *
import random
import hashlib
from ciphers.rsa import RsaSystem


class RsaBlindSignature(RsaSystem):
    def generate_d_number(self, f: int) -> int:
        d = 0
        while euclidean_algorithm(d, f)[0] != 1:
            d = random.randrange(2, f)
        return d

    def eval_c_number(self, d: int, f: int) -> int:
        return exp_mod(euclidean_algorithm(d, f)[1], 1, f)

    def generate_p_q(self) -> list:
        p = 0
        q = 0
        while p == q:
            p = randprime(1 << 1023, (1 << 1024) - 1)
            q = randprime(1 << 1023, (1 << 1024) - 1)
        return [p, q]

    def eval_n(self, p: int, q: int) -> int:
        return p * q

    def eval_f(self, p: int, q: int) -> int:
        return (p-1)*(q-1)


class Server(RsaBlindSignature):
    def __init__(self) -> None:
        super().__init__()
        self.bullets = set()
        self.voted = set()
        self.p, self.q = self.generate_p_q()
        self.n = self.p * self.q
        self.f = self.eval_f(self.p, self.q)
        self.d = self.generate_d_number(self.f)
        self.__c = self.eval_c_number(self.d, self.f)

    def request_for_get_bullet(self, id: int, hash: int) -> int:
        if len(self.voted) != 0:
            if id in self.voted:
                return -1
        self.voted.add(id)
        return exp_mod(hash, self.__c, self.n)

    def __check_correct(self, n: int, s: int) -> bool:
        return int(hashlib.sha3_256(repr(n).encode()).hexdigest(), 16) == exp_mod(s, self.d, self.n)

    def send_data(self, n: int, s: int) -> bool:
        if self.__check_correct(n, s) is True:
            self.bullets.add((n, s))
            return True
        else:
            return False
