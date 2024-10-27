import click
from .ASMsymbolTable import SymbolTable
from .ASMcode import Code
from .ASMparser import Parser


class ASM:
    def __init__(self, nasm, hack, quiet=False):
        self.hack = hack
        self.symbolTable = SymbolTable()
        self.parser = Parser(nasm)
        self.code = Code()
        self.quiet = quiet

    def run(self):
        try:
            self.fillSymbolTable()
            self.generateMachineCode()
            return 0
        except:
            if not self.quiet:
                print("--> ERRO AO TRADUZIR: {}".format(self.parser.currentLine))
            raise ValueError("--> ERRO AO TRADUZIR: {}".format(self.parser.currentLine))

    def fillSymbolTable(self):

        # label
        rom = 0
        while self.parser.advanced():
            if self.parser.commandType() == "L_COMMAND":
                label = self.parser.label()
                if self.symbolTable.contains(label):
                    raise Exception("Label ja declarado: {}".format(label))
                self.symbolTable.addEntry(label, rom)
            else:
                rom = rom + 1
        self.parser.reset()

        # leaw $MEM
        # talvez tirar isso aqui da entrega do assembler
        # e colocar no vmtranslator
        ram = 16
        while self.parser.advanced():
            if self.parser.commandType() == "A_COMMAND":
                name = self.parser.symbol()
                if not name.isdigit():
                    if not self.symbolTable.contains(name):
                        self.symbolTable.addEntry(name, ram)
                        ram = ram + 1
        self.parser.reset()

    def generateMachineCode(self):
        while self.parser.advanced():
            if self.parser.commandType() == "C_COMMAND":
                c = self.parser.command()
                bin = (
                    "1"
                    + "000"
                    + self.code.comp(c)
                    + "0"
                    + self.code.dest(c)
                    + self.code.jump(c)
                )
                self.hack.write(bin + "\n")
            elif self.parser.commandType() == "A_COMMAND":
                label = self.parser.symbol()
                if self.symbolTable.contains(label):
                    c = self.symbolTable.getAddress(label)
                else:
                    c = label
                bin = "0" + "0" + self.code.toBinary(c)
                self.hack.write(bin + "\n")


@click.command()
@click.argument("nasm", type=click.File("r"))
@click.argument("hack", type=click.File("w"))
def main(nasm, hack):
    assembler = Assembler(nasm, hack)
    assembler.run()

if __name__ == "__main__":
    main()
