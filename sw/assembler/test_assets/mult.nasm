; Arquivo: Abs.nasm
; Curso: Elementos de Sistemas
; Criado por: Luciano Soares
; Data: 27/03/2017

; Multiplica o valor de RAM[1] com RAM[0] salvando em RAM[3]

leaw $3, %A
movw $0, (%A)

loop:

  leaw $0, %A
  movw (%A), %D

  ; subtrai RAM[0] = RAM[0] - 1

end:


