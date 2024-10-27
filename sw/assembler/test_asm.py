#!/usr/bin/env python3
#
import filecmp
from .ASM import ASM

NASM_IN = 'test_assets/factorial.nasm'
HACK_OUT = 'test_assets/factorial_out.hack'
HACK_REF = 'test_assets/factorial.hack'

def initASM():
    fNasm = open(NASM_IN, 'r')
    fHack = open(HACK_OUT, "w")
    return ASM(fNasm, fHack)


def test_fillSymbolTtable_labels():
    asm = initASM()
    asm.fillSymbolTable()

    assert asm.symbolTable.contains('CASOZERO') is True
    assert asm.symbolTable.contains('BATATA') is False
    assert asm.symbolTable.contains('WHILE') is True
    assert asm.symbolTable.contains('END') is True
    assert asm.symbolTable.contains('ENDD') is True


def test_fillsymboltable_address():
    asm = initASM()
    asm.fillSymbolTable()

    assert asm.symbolTable.getAddress('CASOZERO') == 39
    assert asm.symbolTable.getAddress('WHILE') == 16
    assert asm.symbolTable.getAddress('END') == 41
    assert asm.symbolTable.getAddress('ENDD') == 53


def test_asm_run():
    asm = initASM()

    try:
        asm.run()
    except:
        assert False

    try:
        fout = open(HACK_OUT, 'r')
    except:
        assert False


def test_asm_hack():
    fNasm = open(NASM_IN, 'r')
    fHack = open(HACK_OUT, "w")
    asm = ASM(fNasm, fHack)
    asm.run()
    fHack.close()

    assert filecmp.cmp(HACK_OUT, HACK_REF)
