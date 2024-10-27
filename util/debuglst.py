#!/usr/bin/env python3

from io import StringIO
import argparse
import sys
import os

from bits.sw.simulator.lst_parser import *

from rich.live import Live
from rich.table import Table
from rich import print
from rich.console import Console
from rich.layout import Layout

dissa = {
    "100001101110010000": "addw %A, $1, %D",
    "100011101110010000": "addw (%A), $1, %D",
    "100000111110001000": "addw %D, $1, %A",
    "100010111110100000": "addw %D, $1, (%A)",
    "100011101110001000": "addw (%A), $1, %A",
    "100000000100001000": "addw %D, %A, %A",
    "100010000100100000": "addw %D, %A, (%A)",
    "100010000100010000": "addw (%A), %D, %D",
    "100010000100001000": "addw (%A), %D, %A",
    "100001100100010000": "subw %A, $1, %D",
    "100011100100010000": "subw (%A), $1, %D",
    "100000011100001000": "subw %D, $1, %A",
    "100011100100001000": "subw (%A), $1, %A",
    "100000100110001000": "subw %D, %A, %A",
    "100000100110010000": "subw %D, %A, %D",
    "100010100110100000": "subw %D, %A, (%A)",
    "100010001110010000": "subw (%A), %D, %D",
    "100010001110001000": "subw (%A), %D, %A",
    "100000100110010000": "subw %D, %A, %D",
    "100000000000001000": "andw %D, %A, %A",
    "100010000000100000": "andw %D, %A, (%A)",
    "100010000000010000": "andw (%A), %D, %D",
    "100010000000001000": "andw (%A), %D, %A",
    "100000101010001000": "orw %D, %A, %A",
    "100010101010100000": "orw %D, %A, (%A)",
    "100010101010010000": "orw (%A), %D, %D",
    "100010101010001000": "orw (%A), %D, %A",
    "100001100000010000": "movw %A, %D",
    "100001100000110000": "movw %A, %D, (%A)",
    "100000011000001000": "movw %D, %A",
    "100000011000101000": "movw %D, %A, (%A)",
    "100000011000100000": "movw %D, (%A)",
    "100011100000001000": "movw (%A), %A",
    "100011100000010000": "movw (%A), %D",
    "100011100000011000": "movw (%A), %D, %A",
    "100001101110001000": "incw %A",
    "100000111110010000": "incw %D",
    "100001100100001000": "decw %A",
    "100000011100010000": "decw %D",
    "100001100110001000": "negw %A",
    "100000011110010000": "negw %D",
    "100000011010010000": "notw %D",
    "100001100010001000": "notw %A",
    "100000011000000111": "jmp",
    "100000011000000010": "je",
    "100000011000000101": "jne",
    "100000011000000001": "jg",
    "100000011000000011": "jge",
    "100000011000000110": "jle",
    "100000011000000100": "jl",
    "100001010100000000": "nop",
}


def dissasembly(op):
    if op[0] == "0":
        dec = int(op, 2)
        instrucao = f"leaw ${dec}, %A"
    else:
        if op in dissa:
            instrucao = dissa[op]
        else:
            instrucao = op
    return instrucao


def debugLst(name, quiet=False):
    name_lst = name + ".lst"
    name_ram_in = name + "_ram_init.txt"
    name_ram_end = name + "_ram_end.txt"

    if os.path.exists(name_lst):
        file_lst = open(name_lst, "r")
    else:
        print("Arquivo lst não encontrado")
        return

    if os.path.exists(name_ram_in):
        file_ram = open(name_ram_in, "r")
    else:
        file_ram = None

    app = LSTParser(file_lst)

    layout = Layout()
    layout.split_row(Layout(name="in_ram"), Layout(name="cpu"), Layout(name="end_ram"))

    console = Console(file=StringIO() if quiet else None, record=quiet)
    table = Table()
    table.add_column("pcount")
    table.add_column("OP")
    table.add_column("%A")
    table.add_column("%D")
    table.add_column("RAM")

    in_ram = {}
    if file_ram is not None:
        for n in file_ram.readlines():
            try:
                addr, value = n.split(":")
                in_ram[int(addr)] = int(value, 2)
            except:
                pass

    tableInRam = Table()
    tableInRam.add_column("Address")
    tableInRam.add_column("Value")
    for key, value in in_ram.items():
        tableInRam.add_row(f"{key}", f"{value}")

    pcoutOld = 0
    state = app.advance()
    ram = {}
    while app.has_more():
        state = app.advance()

        op = dissasembly(state["instruction"])

        if op == "100000000000000000":
            break

        reg_a = f"{int(state['s_regAout'], 2)}"
        reg_d = f"{int(state['s_regDout'], 2)}"

        pcoutInt = int(state["pcout"], 2)
        if (pcoutOld + 1) != pcoutInt:
            table.add_row("[green bold]SALTOU", "---", "---", "---", "---")
        elif op in ["jmp", "jne", "je", "jle", "jl", "jge", "jg"]:
            table.add_row("[red bold]NÃO SALTOU", "---", "---", "---", "---")

        pcount = f"{pcoutInt}"

        if state["writeM"] == "1":
            address = f"{int(state['s_regAout'], 2)}"
            value = f"{int(state['outM'], 2)}"
            ram[address] = value

        ramp = ""
        if state["writeM"] == "1":
            ramp = f"RAM[{address}]={value}"

        table.add_row(
            pcount,
            op,
            reg_a,
            reg_d,
            ramp,
        )
        pcoutOld = pcoutInt

    tableEndRam = Table()
    tableEndRam.add_column("Address")
    tableEndRam.add_column("Value")
    for key, value in ram.items():
        tableEndRam.add_row(f"{key}", f"{value}")

    layout["in_ram"].update(tableInRam)
    layout["cpu"].update(table)
    layout["end_ram"].update(tableEndRam)
    console.print("---- RAM INICIAL ----")
    console.print(tableInRam)
    console.print("---- SIMULAÇÃO CPU ----")
    console.print(table)
    console.print("--- RAM FINAL ALTERADA ---")
    console.print(tableEndRam)
    # console.print(layout)
    return console
