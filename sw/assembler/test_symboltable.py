#!/usr/bin/env python3
#

from .ASMsymbolTable import SymbolTable


def test_init():
    s = SymbolTable()

    assert s.table["R5"] == 5
    assert s.table["KBD"] == 24576


def test_addEntry():
    s = SymbolTable()
    s.addEntry("abobrina", 13)
    assert s.table["abobrina"] == 13


def test_contains():
    s = SymbolTable()
    assert s.contains("abobrina") == False
    assert s.contains("R13") == True


def test_getAddress():
    s = SymbolTable()
    assert s.getAddress("R10") == 10
