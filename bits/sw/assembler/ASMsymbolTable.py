import sys


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.init()

    def init(self):
        for i in range(0, 17):
            self.table["R" + str(i)] = i

        self.table["KBD"] = 24576
        self.table["SCR"] = 16384
        self.table["SCREEN"] = 16384
        self.table["SP"] = 0
        self.table["LCL"] = 1
        self.table["ARG"] = 2
        self.table["THIS"] = 3
        self.table["THAT"] = 4

    def addEntry(self, symbol: str, address: int):
        self.table[symbol] = address

    def contains(self, symbol):
        return symbol in self.table

    def getAddress(self, symbol):
        return self.table[symbol]


if __name__ == "__main__":
    pass
