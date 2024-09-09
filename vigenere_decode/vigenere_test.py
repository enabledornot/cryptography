from vigenere import *
# m for math
class m:
    def __init__(self, c):
        if isinstance(c,m):
            self.d = c.d
        elif isinstance(c,int):
            self.d = c
        else:
            self.d = char_to_num(c)
    def __str__(self):
        return num_to_chr(self.d)
    def __add__(self, other):
        print(type(other))
        if isinstance(other, m):
            return m(self.d + other.d)
        elif isinstance(other, int):
            return m(self.d + other)
        else:
            return m(self.d + char_to_num(other))
    def __sub__(self, other):
        if isinstance(other, m):
            return m(self.d - other.d)
        elif isinstance(other, int):
            return m(self.d - other)
        else:
            return m(self.d - char_to_num(other))
    def __repr__(self):
        return str(self)
class ms:
    def __init__(self, c):
        self.ds = []
        for i in c:
            self.ds.append(m(i))
    def __str__(self):
        tmp = ""
        for c in self.ds:
            tmp += str(c)
        return tmp
    def __add__(self, other):
        tmp = []
        for s, o in zip(self.ds, other.ds):
            tmp.append(s + o)
        return ms(tmp)
    def __sub__(self, other):
        tmp = []
        for s, o in zip(self.ds, other.ds):
            tmp.append(s - o)
        return ms(tmp)
    def __repr__(self):
        return str(self)
if __name__ == "__main__":
    pass