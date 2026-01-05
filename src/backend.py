class CodeGenerator:
    def __init__(self, ir_code):
        self.ir_code = ir_code
        self.target_code = []

    def generate(self):
        print(f"{'='*10} FASE 4: CODE GENERATION (BACKEND) {'='*10}")
        
        self.target_code.append(".data")
        self.target_code.append("    ; Variable declarations would go here")
        self.target_code.append(".text")
        self.target_code.append("global _start")
        self.target_code.append("_start:")

        for instr in self.ir_code:
            self.translate(instr)

        self.target_code.append("    ; Exit program")
        self.target_code.append("    MOV EAX, 1")
        self.target_code.append("    INT 0x80")
        
        return "\n".join(self.target_code)

    def translate(self, instr):
        # Menerjemahkan Quadruple ke Assembly
        op = instr.op
        arg1 = instr.arg1
        arg2 = instr.arg2
        res = instr.result

        self.target_code.append(f"    ; {instr}") # Komentar kode asli

        if op == 'ASSIGN':
            # a = b  -> MOV EAX, b; MOV a, EAX
            self.target_code.append(f"    MOV EAX, {arg1}")
            self.target_code.append(f"    MOV [{res}], EAX")
            
        elif op in ['+', '-', '*', '/']:
            # t1 = a + b
            self.target_code.append(f"    MOV EAX, {arg1}")
            
            if op == '+':
                self.target_code.append(f"    ADD EAX, {arg2}")
            elif op == '-':
                self.target_code.append(f"    SUB EAX, {arg2}")
            elif op == '*':
                self.target_code.append(f"    IMUL EAX, {arg2}")
            elif op == '/':
                self.target_code.append(f"    MOV EDX, 0") # Clear EDX for div
                self.target_code.append(f"    MOV EBX, {arg2}")
                self.target_code.append(f"    DIV EBX")

            self.target_code.append(f"    MOV [{res}], EAX")

        elif op == 'PRINT':
            # Print (Fiktif, memanggil interrupt print)
            self.target_code.append(f"    PUSH {arg1}")
            self.target_code.append(f"    CALL print_int")
            self.target_code.append(f"    ADD ESP, 4")