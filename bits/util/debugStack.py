#!/usr/bin/env python3

from myhdl import intbv
from bits.sw.simulator.lst_parser import *
from rich.live import Live
from rich.table import Table
from rich import print
from rich.console import Console
from rich.layout import Layout

SP = 0
LCL = 1
ARG = 2
THIS = 3
THAT = 4
STACK = 256
TEMP_0 = 5
TEMP_7 = 12

def genTablePointers(mem):
    table = Table()
    table.add_column("*p")
    table.add_column("val")
    table.add_row('SP', str(mem[SP]))
    table.add_row('LCL', str(mem[LCL]))
    table.add_row('ARG', str(mem[ARG]))
    table.add_row('THIS',str(mem[THIS]))
    table.add_row('THAT',str(mem[THAT]))
    return table

def genTableStack(mem):
    table = Table()
    table.add_column("Addr")
    table.add_column("val")

    sorted_stack = sorted(mem.keys())
    for address in sorted_stack:
        table.add_row(str(address), mem[address] )

    return(table)


def debugStack(lstFile):
    pointers = {SP:'256', LCL:0, ARG: 0, THIS:0, THAT:0}
    pointers_name = {0: 'SP', 1:'LCL', 2:'ARG', 3:'THIS', 4: 'THAT'}
    stack = {}
    temp = {}

    layout = Layout()
    layout.split_row(Layout(name="pointers"), Layout(name="temp"),  Layout(name="stack"))
    layout['pointers'].size = 18
    layout['temp'].size = 25
    layout['stack'].size = 25
    console = Console()
    console.size = (68, 10)

    update = False
    nop = False

    file_in = open(lstFile, "r")
    app = LSTParser(file_in)
    while app.has_more():

        state = app.advance()

        if nop is True:
            break

        if state["instruction"] == "100000000000000000":
            nop = True

        address = int(state['s_regAout'], 2)

        value_unsigned = int(state['outM'], 2)
        value_int = intbv(value_unsigned)[16:]
        value = int(value_int.signed())

        if state["writeM"] == "1":
            if address <= THAT:
                update = True
                pointers[address] = str(value)

            if address >= STACK:
                update = True
                stack[address] = str(value)

            if TEMP_0 <= address <= TEMP_7:
                update = True
                temp[address] = str(value)

        if update:
            table_p = genTablePointers(pointers)
            table_t = genTableStack(temp)
            table_s = genTableStack(stack)
            layout['pointers'].update(table_p)
            layout['temp'].update(table_t)
            layout['stack'].update(table_s)
            console.print(layout)


            update = False
