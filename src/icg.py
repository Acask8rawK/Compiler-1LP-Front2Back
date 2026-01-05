from colors import Colors
class Quadruple:
    def __init__(self, op, arg1, arg2, result):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __repr__(self):
        # Format: result = arg1 op arg2
        if self.op == 'ASSIGN':
            return f"{self.result} = {self.arg1}"
        elif self.op == 'PRINT':
            return f"PRINT {self.arg1}"
        else:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"

class ICG:
    def __init__(self):
        self.code = []      # List instruksi TAC (Three-Address Code)
        self.temp_count = 0 # Counter untuk variabel temporary (t1, t2, ...)

    def new_temp(self):
        """Membuat variabel temporary baru (t1, t2, t3...)"""
        self.temp_count += 1
        return f"t{self.temp_count}"

    def emit(self, op, arg1, arg2, result):
        instr = Quadruple(op, arg1, arg2, result)
        self.code.append(instr)
        # Gunakan warna hijau tipis untuk log generate
        print(f"   {Colors.GREEN}>> [GEN]{Colors.ENDC} {instr}")

    def get_code(self):
        return self.code