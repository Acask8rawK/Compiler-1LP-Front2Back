.data
    ; Variable declarations would go here
.text
global _start
_start:
    ; a = 10
    MOV EAX, 10
    MOV [a], EAX
    ; b = 5
    MOV EAX, 5
    MOV [b], EAX
    ; PRINT a
    PUSH a
    CALL print_int
    ADD ESP, 4
    ; d = 100
    MOV EAX, 100
    MOV [d], EAX
    ; PRINT b
    PUSH b
    CALL print_int
    ADD ESP, 4
    ; Exit program
    MOV EAX, 1
    INT 0x80