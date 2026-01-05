import sys

from lexer import Lexer
from parser_icg import ParserICG
from backend import CodeGenerator
from colors import Colors # Import modul warna kita

def run_full_compiler(filepath):
    Colors.print_header(f"RUNNING COMPILER: {filepath}")
    
    try:
        # --- PHASE 0: READ FILE ---
        try:
            with open(filepath, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            Colors.print_error(f"File '{filepath}' tidak ditemukan!")
            return

        # --- PHASE 1: LEXER ---
        print(f"\n{Colors.BLUE}[PHASE 1] Lexical Analysis...{Colors.ENDC}")
        lexer = Lexer(code)
        # Tampilkan token dengan rapi (dipotong jika terlalu panjang)
        token_preview = str(lexer.tokens)[:100] + "..." if len(str(lexer.tokens)) > 100 else str(lexer.tokens)
        print(f"   Token Stream: {Colors.CYAN}{token_preview}{Colors.ENDC}")

        # --- PHASE 2 & 3: PARSING & ICG ---
        print(f"\n{Colors.BLUE}[PHASE 2 & 3] Parsing & Intermediate Code Generation...{Colors.ENDC}")
        try:
            parser = ParserICG(lexer.tokens)
            ir_code = parser.parse()
        except Exception as e:
            # Tangkap error parser disini
            Colors.print_error(f"Parsing Gagal: {e}")
            return # Berhenti jika parsing gagal

        print(f"\n{Colors.BOLD}[INTERMEDIATE CODE - TAC]{Colors.ENDC}")
        for i, instr in enumerate(ir_code):
            # Mewarnai instruksi agar mudah dibaca
            print(f"   {Colors.WARNING}{i+1:02d}:{Colors.ENDC} {instr}")

        # --- PHASE 4: BACKEND ---
        print(f"\n{Colors.BLUE}[PHASE 4] Backend Code Generation...{Colors.ENDC}")
        backend = CodeGenerator(ir_code)
        assembly = backend.generate()

        print(f"\n{Colors.BOLD}[TARGET CODE - ASSEMBLY PREVIEW]{Colors.ENDC}")
        print(Colors.CYAN + "\n".join(assembly.split('\n')[:15]) + Colors.ENDC) # Tampilkan 15 baris pertama saja
        if len(assembly.split('\n')) > 15:
            print(f"{Colors.CYAN}... (sisa kode di output file) ...{Colors.ENDC}")
        
        # Output File
        output_file = "output.asm"
        with open(output_file, "w") as f:
            f.write(assembly)
        
        print("-" * 50)
        Colors.print_success(f"Kompilasi Selesai! Output disimpan di '{output_file}'")

    except Exception as e:
        Colors.print_error(f"Critical System Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        Colors.print_warning("Usage: python src/main_full.py <filepath>")
    else:
        run_full_compiler(sys.argv[1])