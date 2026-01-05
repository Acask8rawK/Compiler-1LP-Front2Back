🚀 1LP Programming Language Compiler (Front-to-Back)

Proyek Akhir Mata Kuliah Teknik Kompilasi

Dosen: Sulistyo Puspitodjati



📝 Deskripsi Proyek

Proyek ini merupakan implementasi Compiler Lengkap (Front-to-Back) untuk bahasa pemrograman kustom bernama "1LP".

Berbeda dengan versi sebelumnya yang hanya sebatas interpreter, versi final ini adalah True Compiler yang menerjemahkan kode sumber tingkat tinggi menjadi Kode Rakitan (Assembly x86) yang siap dijalankan oleh mesin.

Proyek ini dibangun menggunakan bahasa Python dari nol (from scratch) tanpa ketergantungan pada library parser eksternal seperti PLY, Yacc, atau ANTLR.



✨ Fitur Unggulan:

Full Pipeline: Lexer $\rightarrow$ Parser $\rightarrow$ Semantic $\rightarrow$ ICG $\rightarrow$ Backend.

Code Generation: Menghasilkan file output .asm dengan sintaks Assembly x86 (Intel).

Intermediate Code (TAC): Menggunakan representasi Three-Address Code (Quadruples) untuk standarisasi logika.

Robust Error Recovery: Implementasi Panic Mode yang mampu memulihkan diri dari kesalahan sintaks (misal: kurang titik koma) dan melanjutkan kompilasi baris berikutnya.

Strict Semantics: Validasi ketat untuk variabel yang belum dideklarasikan (Undeclared Variable Check).

Rich UI: Tampilan terminal interaktif dengan pewarnaan (Syntax Highlighting) untuk membedakan log sukses, warning, dan error.


👥 Informasi Kelompok

Kelas: 4IA04

Nama Anggota:

* Miskah Nurzakwan W (5042283)
* Dio Adeliya Putra (50422434)
* Pasya Shafaa Aaqila (51422281)
* Muhammad Alfian Rizki R (50422934)
* Muhammad Muhsin Azzam (51422095)


📂 Struktur Folder

Plaintext



Compiler_Front2Back/

│

├── src/                      <-- Source Code Utama

│   ├── lexer.py              # Scanner: Mengubah teks menjadi Token stream

│   ├── parser_icg.py         # Parser: Analisis Sintaks, Semantik & Panic Mode

│   ├── icg.py                # ICG: Generator Three-Address Code (TAC)

│   ├── backend.py            # Backend: Penerjemah TAC ke Assembly x86

│   ├── colors.py             # UI: Modul pewarnaan output terminal

│   └── main_full.py          # Driver: Program utama yang menjalankan semua fase

│

├── tests/                    <-- File Uji Coba (Test Cases)

│   ├── valid_code.txt        # Kode valid (Math, Nested Expression, Print)

│   ├── error_syntax.txt      # Uji fitur Panic Mode (Lupa titik koma)

│   ├── error_semantic.txt    # Uji validasi variabel (Typo nama variabel)

│   └── error_lexical.txt     # Uji karakter ilegal

│

├── output.asm                # Hasil Output Assembly (Generated File)

└── README.txt                # Dokumentasi proyek


🛠️ Spesifikasi Teknis

1. Frontend (Analisa)

Lexer: Menggunakan Regex untuk mengenali token ID, NUM, ASSIGN, PRINT, Operator Matematika, dan (Stm, Exp).

Parser: Menggunakan metode Recursive Descent Parsing (Top-Down LL(1)).

Semantic: Menggunakan Symbol Table (Set) untuk memastikan setiap variabel yang digunakan sudah di-assign sebelumnya.

2. Intermediate Code (Tengah)

Parser mengubah ekspresi matematika kompleks menjadi urutan instruksi sederhana.

Menggunakan variabel temporer (t1, t2, t3...) secara otomatis.

Format: Result = Operand1 Operator Operand2

3. Backend (Sintesis)

Menerjemahkan instruksi perantara menjadi instruksi CPU nyata.

Target: Assembly x86 (Intel Syntax).

Register: Menggunakan EAX untuk akumulator, EBX untuk pembagi, dan EDX untuk sisa bagi.

Stack: Mengelola PUSH/POP untuk pemanggilan fungsi print.


🚀 Cara Menjalankan Program

Pastikan Python 3 sudah terinstall. Jalankan perintah melalui terminal dari folder root proyek.

A. Kompilasi Kode Valid (Normal)

Perintah ini akan menghasilkan file output.asm.

Bash



python src/main_full.py tests/valid_code.txt

Output: Tampilan fase Lexing, Parsing, tabel TAC, dan preview Assembly berwarna hijau (Sukses).

B. Uji Error Recovery (Panic Mode)

Mendemokan kemampuan compiler untuk tidak crash saat ada error sintaks.

Bash



python src/main_full.py tests/error_syntax.txt

Output: Pesan error berwarna MERAH, diikuti pesan Recovery berwarna KUNING. Compiler tetap lanjut memproses baris yang benar.

C. Uji Validasi Semantik

Mendemokan deteksi variabel yang belum didefinisikan.

Bash



python src/main_full.py tests/error_semantic.txt

Output: Pesan error [Semantic Error] Variabel '...' belum didefinisikan.


📊 Contoh Hasil Output (TAC vs Assembly)

Berikut adalah transformasi data yang terjadi di dalam compiler ini:

1. Source Code (Input):

Plaintext



c := a + b * 2;

2. Intermediate Code / TAC (Internal):

Plaintext



t1 = b * 2

c = a + t1

3. Assembly x86 (Output):

Cuplikan kode



; t1 = b * 2

MOV EAX, b

IMUL EAX, 2

MOV [t1], EAX



; c = a + t1

MOV EAX, a

ADD EAX, t1

MOV [c], EAX
