#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Curso de Elementos de Sistemas
# Desenvolvido por: Rafael Corsi <rafael.corsi@insper.edu.br>
# ref: https://solarianprogrammer.com/2017/10/25/ppm-image-python-3/
# Adaptado de https://github.com/Insper/Z01-tools/blob/master/scripts/genImg.py

import array
from pathlib import Path
import sys, subprocess
import os
from myhdl import bin

LCD_INIT = 16384
LCD_END = 21183
LCD_PX_PER_LINE = 16


class memTopgm(object):
    def __init__(self, memIn, imgOut, quiet=False):
        self.memIn = memIn
        self.imgOut = imgOut + ".pgm"
        self.width = 320
        self.height = 240
        self.maxval = 1
        self.ppm_header = f"P1 {self.width} {self.height} {self.maxval}\n"
        self.img = [0] * (self.width * self.height)
        self.quiet = quiet
        self.do()

    def do(self):
        if not self.quiet:
            self.genImg()
            self.saveImg()

    def genImg(self):
        for key, value in self.memIn.items():
            if key >= LCD_INIT and key <= LCD_END:
                refAddress = key - LCD_INIT
                ramAddress = refAddress * LCD_PX_PER_LINE
                pxs = bin(value, 16)
                for i in range(LCD_PX_PER_LINE):
                    self.img[ramAddress + i] = pxs[i]

    def saveImg(self):
        if not self.quiet:
            print(self.imgOut)

        with open(self.imgOut, "wb") as fw:
            fw.write(bytearray(self.ppm_header, "ascii"))
            for n in self.img:
                fw.write("{} ".format(n).encode())


if __name__ == "__main__":
    lcd = lcdToimg("R-LCD0_lcd.mif", "lcd.pgm")
    lcd.genImg()
    lcd.saveImg2()
