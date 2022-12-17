from abc import abstractmethod, ABC

class RsaSystem(ABC):

    @abstractmethod
    def generate_d_number(self, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_c_number(self, d: int, f: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def generate_p_q(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def eval_n(self, p: int, q: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def eval_f(self, p: int, q: int) -> int:
        raise NotImplementedError
