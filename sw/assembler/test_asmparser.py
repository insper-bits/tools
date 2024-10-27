#!/usr/bin/env python3

from .ASMparser import Parser


def test_advanced():
    fnasm = open('test_assets/mult.nasm', 'r')
    ptest = Parser(fnasm)

    assert ptest.advanced() is True
    assert ptest.command() == ['leaw', '$3', '%A']

    assert ptest.advanced() is True
    assert ptest.command() == ['movw', '$0', '(%A)']

    assert ptest.advanced() is True
    assert ptest.command() == ['loop:']

    assert ptest.advanced() is True
    assert ptest.command() == ['leaw', '$0', '%A']

    assert ptest.advanced() is True
    assert ptest.command() == ['movw', '(%A)', '%D']

    assert ptest.advanced() is True
    assert ptest.command() == ['end:']

    assert ptest.advanced() is False


def test_commandType():
    fnasm = open('test_assets/mult.nasm', 'r')
    ptest = Parser(fnasm)

    ptest.currentCommand = ['leaw', '$2', '%A']
    assert ptest.commandType() == ptest.CommandType['A']

    ptest.currentCommand = ['movw', '$1', '%A']
    assert ptest.commandType() == ptest.CommandType['C']

    ptest.currentCommand = ['WHILE:']
    assert ptest.commandType() == ptest.CommandType['L']

    ptest.currentCommand = ['leaw', '$31', '%A']
    assert ptest.commandType() == ptest.CommandType['A']

    ptest.currentCommand = ['addw', '%D', '%A', '%D']
    assert ptest.commandType() == ptest.CommandType['C']

    ptest.currentCommand = ['rsubw', '%D', '%A', '%D']
    assert ptest.commandType() == ptest.CommandType['C']


def test_symbol():
    fnasm = open('test_assets/symbol.nasm', 'r')
    ptest = Parser(fnasm)

    assert ptest.advanced() is True
    assert ptest.symbol() == '1'

    assert ptest.advanced() is True
    assert ptest.symbol() == '3'

    assert ptest.advanced() is True
    assert ptest.symbol() == '45'

    assert ptest.advanced() is False


def test_labol():
    fnasm = open('test_assets/labol.nasm', 'r')
    ptest = Parser(fnasm)

    assert ptest.advanced() is True
    assert ptest.label() == 'OI'

    assert ptest.advanced() is True
    assert ptest.advanced() is True
    assert ptest.label() == 'END'

    assert ptest.advanced() is True

    assert ptest.advanced() is True
    assert ptest.label() == 'WHILE_1'

    assert ptest.advanced() is True
    assert ptest.advanced() is False
