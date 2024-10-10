import math
import sympy
from .utilities import *

class pump:

    def __init__(
        self,
        file,
        dia,
        time=0,
    ):
        self.file = file
        self.dia = dia
        self.time = time
        self.loop = []

    def init(*args):
        for self in args:
            self.file.write(f"dia {self.dia}\nal 1\nbp 1\nPF 0\n")

    def rat(self, rate: int, vol: int, dir: str):
        self.file.write(f"\nphase\nfun rat\nrat {rate} mm\nvol {vol}\ndir {dir}\n")
        self.time += vol / rate * 60 * self.getloop()

    def pas(self, length: int):
        if length <= 99:
            self.file.write(f"\nphase\nfun pas {length}\n")
            self.time += length * self.getloop()

        elif length <= 99 * 3:
            self.pas(99)
            self.pas(length - 99)
        else:
            multiples = factor_check(decompose_dict(sympy.factorint(length)))
            if multiples != (0, 0) and len(multiples) <= 3:
                for i in range(len(multiples) - 1):
                    self.loopstart(multiples[1 + i])
                self.pas(multiples[0])
                for i in range(len(multiples) - 1):
                    self.loopend()
            else:
                self.pas(length % 50, self.getloop())
                length -= length % 50
                self.pas(length, self.getloop())

    def loopstart(self, count):
        self.loop.append(count)
        if len(self.loop) > 3:
            raise Exception("Up to three nested loops, you have too many")
        self.file.write(f"\nphase\nfun lps\n")

    def loopend(self):
        self.file.write(f"\nphase\nfun lop {self.loop.pop()}\n")

    def getloop(self):
        if len(self.loop) >= 1:
            return self.loop[-1]
        else:
            return sympy.prod(self.loop)

    def stop(*args):
        for self in args:
            self.file.write(f"\nphase\nfun stp\n")

    def sync(*args):
        max_time = 0
        for arg in args:
            if arg.time > max_time:
                max_time = arg.time
        for arg in args:
            time_diff = max_time - arg.time
            if time_diff > 0:
                arg.pas(math.ceil(time_diff))

