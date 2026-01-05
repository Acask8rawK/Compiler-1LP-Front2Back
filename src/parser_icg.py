import sys
from icg import ICG
from colors import Colors # Kita pakai warna agar error terlihat jelas

class ParserICG:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos]
        self.symbol_table = set() 
        self.icg = ICG()
        self.error_count = 0 # Menghitung jumlah error

    def error(self, message):
        self.error_count += 1
        # Raise exception agar bisa ditangkap oleh mekanisme SYNC
        raise Exception(f"{message} pada token {self.current_token}")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            self.error(f"Mengharapkan {token_type}, mendapat {self.current_token.type}")

    # --- ERROR RECOVERY (PANIC MODE) ---
    def sync(self):
        """
        Melompati token sampai menemukan titik koma (SEMI) atau EOF.
        """
        Colors.print_warning("🔄 [PANIC MODE] Mencari token penyelaras (SEMI)...")
        
        # Loop terus sampai ketemu SEMI atau EOF
        while self.current_token.type != 'SEMI' and self.current_token.type != 'EOF':
            # Skip token
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        
        # Jika ketemu SEMI, makan tokennya agar parser siap di statement baru
        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
            Colors.print_info("👌 [RECOVERY] Berhasil sinkronisasi. Lanjut ke baris berikutnya.")

    # --- ATURAN PRODUKSI ---

    def parse(self):
        print(f"{'='*10} FASE 2 & 3: PARSING & ICG {'='*10}")
        self.stm()
        
        if self.current_token.type != 'EOF':
            self.error("Sisa input deteksi.")
            
        print(f"\n[INFO] Parsing & ICG Selesai. Total Error: {self.error_count}")
        return self.icg.get_code()

    def stm(self):
        # Kita bungkus LOGIKA UTAMA dengan Try-Except
        try:
            self.stm_prime()
            # Pindahkan si_stm ke DALAM try
            # Artinya: Kalau stm_prime sukses, baru cari titik koma
            self.si_stm() 
            
        except Exception as e:
            # Jika ada error syntax di statement ini:
            Colors.print_error(f"Syntax Error: {e}")
            
            # Lakukan sinkronisasi (skip sampai ;)
            self.sync()
            
            # --- LOGIKA RECOVERY BARU ---
            # Setelah sync, token saat ini adalah awal dari statement berikutnya (misal: PRINT).
            # Kita tidak butuh si_stm (karena titik koma sudah dimakan sync).
            # Kita langsung panggil stm() untuk memproses baris berikutnya.
            if self.current_token.type != 'EOF':
                # Panggil diri sendiri untuk lanjut parsing baris next
                self.stm()

    def si_stm(self):
        if self.current_token.type == 'SEMI':
            self.eat('SEMI')
            if self.current_token.type in ('ID', 'PRINT'):
                self.stm()
        
        elif self.current_token.type in ('ID', 'PRINT'):
            # Kasus lupa titik koma
            self.error("Kurang titik koma (SEMI) antar statement")
            self.stm()
            
        elif self.current_token.type == 'EOF':
            pass # Benar-benar selesai
            
        elif self.current_token.type == 'RPAREN':
            pass # Selesai karena tutup kurung (nested statement)
            
        else:
            # Jika ketemu token aneh (misal angka '200' nganggur), anggap error
            self.error(f"Token tidak diharapkan '{self.current_token.value}' setelah statement")

    def stm_prime(self):
        # Stm' -> id := Exp | print ( ExpList )
        if self.current_token.type == 'ID':
            var_name = self.current_token.value
            self.eat('ID')
            self.eat('ASSIGN')
            
            # Jika exp() error, dia akan throw exception, 
            # ICG emit di bawah ini TIDAK AKAN dijalankan (Aman!)
            exp_addr = self.exp()
            
            self.icg.emit('ASSIGN', exp_addr, None, var_name)
            self.symbol_table.add(var_name)

        elif self.current_token.type == 'PRINT':
            self.eat('PRINT')
            self.eat('LPAREN')
            self.exp_list() 
            self.eat('RPAREN')
        else:
            self.error("Statement harus id atau print")

    def exp(self):
        term_addr = self.exp_prime()
        return self.si_exp(term_addr)

    def si_exp(self, inherited_addr):
        if self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.type
            self.eat(op)
            term_addr = self.exp_prime()
            
            new_temp = self.icg.new_temp()
            op_symbol = '+' if op == 'PLUS' else '-'
            self.icg.emit(op_symbol, inherited_addr, term_addr, new_temp)
            
            return self.si_exp(new_temp)
        return inherited_addr

    def exp_prime(self):
        factor_addr = self.exp_double_prime()
        return self.si_exp_prime(factor_addr)

    def si_exp_prime(self, inherited_addr):
        if self.current_token.type in ('TIMES', 'DIVIDE'):
            op = self.current_token.type
            self.eat(op)
            factor_addr = self.exp_double_prime()
            
            new_temp = self.icg.new_temp()
            op_symbol = '*' if op == 'TIMES' else '/'
            self.icg.emit(op_symbol, inherited_addr, factor_addr, new_temp)
            
            return self.si_exp_prime(new_temp)
        return inherited_addr

    def exp_double_prime(self):
        if self.current_token.type == 'NUM':
            val = str(self.current_token.value)
            self.eat('NUM')
            return val
        elif self.current_token.type == 'ID':
            name = self.current_token.value
            self.eat('ID')
            return name
        elif self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            # Nested statement juga harus diproteksi
            try:
                self.stm() 
            except Exception:
                self.sync() # Synch lokal dalam kurung
            
            self.eat('COMMA')
            val_addr = self.exp()
            self.eat('RPAREN')
            return val_addr
        else:
            self.error("Ekspresi harus dimulai id, num, atau '('")
            return "0" # Return dummy value biar gak crash pythonnya

    def exp_list(self):
        val_addr = self.exp()
        self.icg.emit('PRINT', val_addr, None, None)
        self.exp_list_prime()

    def exp_list_prime(self):
        if self.current_token.type == 'COMMA':
            self.eat('COMMA')
            self.exp_list()