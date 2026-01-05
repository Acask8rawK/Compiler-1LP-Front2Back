🚀 1LP Programming Language Compiler (Front-to-Back)
Proyek Akhir Mata Kuliah Teknik Kompilasi Dosen: Sulistyo Puspitodjati

📝 Deskripsi Proyek
Proyek ini merupakan implementasi Compiler Lengkap (Front-to-Back) untuk bahasa pemrograman kustom bernama "1LP". Berbeda dengan versi interpreter sebelumnya, versi ini tidak hanya menghitung hasil, tetapi menerjemahkan kode sumber menjadi Intermediate Code (TAC) dan Target Code (Assembly x86).

Compiler ini dibangun menggunakan bahasa Python dari nol (from scratch) tanpa menggunakan library parser eksternal seperti PLY atau Yacc.

Fitur Utama:
Lexical Analysis (Scanner): Tokenisasi menggunakan Regular Expression.

Syntax Analysis (Parser): Menggunakan metode Recursive Descent (LL(1)).

Semantic Analysis: Validasi variabel dan manajemen Symbol Table.

Intermediate Code Generation (ICG): Menghasilkan Three-Address Code (TAC/Quadruples).

Code Generation (Backend): Menerjemahkan TAC menjadi kode Assembly x86 (Intel Syntax) yang siap dijalankan.

Robust Error Handling: Implementasi Panic Mode Recovery untuk mendeteksi multiple error tanpa crash.

User Interface: Tampilan terminal yang rapi dan berwarna (Syntax Highlighting).

👥 Informasi Kelompok
Kelas: 4IA04 Nama Anggota:

Muhammad Muhsin Azzam (51422095)

Pasya Shafaa Aaqila (51422781)

Dio Adeliya Putra (50422434)

Miskah Nurzakwan W (50922783)

Muhammad Alfian Ricki R (50422734)

📂 Struktur Folder
Plaintext

Compiler_Front2Back/
│
├── src/                      <-- Source Code Utama
│   ├── lexer.py              # Scanner (Membaca karakter jadi Token)
│   ├── parser_icg.py         # Parser modifikasi untuk generate ICG & Error Recovery
│   ├── icg.py                # Modul Intermediate Code (Quadruples)
│   ├── backend.py            # Modul Sintesis (Translator ke Assembly x86)
│   ├── colors.py             # Helper untuk pewarnaan output terminal
│   └── main_full.py          # Entry point utama (Driver Front-to-Back)
│
├── tests/                    <-- Kumpulan Test Case
│   ├── valid_code.txt        # Kode valid (Assignment, Math, Print, Nested)
│   ├── error_syntax.txt      # Tes Error Recovery (Kurang titik koma, dll)
│   └── error_lexical.txt     # Tes Karakter Ilegal
│
├── output.asm                # Hasil Output Assembly (Generated)
└── README.txt                # Dokumentasi proyek
🛠️ Spesifikasi Teknis (Alur Kompilasi)
1. Frontend (Analisa)
Grammar: LL(1) modifikasi. Mendukung prioritas operator (P1OP/P2OP) dan nested expression.

Panic Mode: Jika parser menemukan error, ia akan melakukan sinkronisasi (skip token) hingga menemukan delimiter (;) agar bisa melanjutkan pemeriksaan baris berikutnya.

2. Intermediate Code (Tengah)
Parser tidak langsung menghitung nilai, melainkan memanggil fungsi emit().

Menghasilkan instruksi atomik dalam format: Result = Arg1 Op Arg2.

Variabel sementara (t1, t2, dst) dibuat otomatis untuk menampung hasil perhitungan bertingkat.

3. Backend (Sintesis)
Membaca instruksi ICG.

Memetakan instruksi ke Register CPU x86 (EAX, EBX, EDX).

Mengelola Stack Pointer (ESP) untuk operasi fungsi print.

Output berupa file .asm standar Linux (Global _start).

🚀 Cara Menjalankan Program
Prasyarat: Python 3.x terinstall.

Langkah-langkah:
Buka Terminal / CMD.

Masuk ke direktori root proyek.

Jalankan perintah berikut:

A. Menjalankan Kompilasi Penuh (Valid Code):

Bash

python src/main_full.py tests/valid_code.txt
Ekspektasi: Tampil visualisasi Fase 1-4 di terminal dan file output.asm terbentuk.

B. Menguji Ketahanan Error (Panic Mode):

Bash

python src/main_full.py tests/error_syntax.txt
Ekspektasi: Compiler menampilkan pesan error merah, melakukan recovery (kuning), dan tetap berhasil men-generate Assembly untuk bagian kode yang valid.

📊 Contoh Hasil Output Terminal
Saat menjalankan valid_code.txt, output akan menampilkan tahapan fase:

Plaintext

==================================================
 RUNNING COMPILER: tests/valid_code.txt
==================================================

[PHASE 1] Lexical Analysis...
   Token Stream: [Token(ID, a), Token(ASSIGN, :=), ...]

[PHASE 2 & 3] Parsing & Intermediate Code Generation...
   [INTERMEDIATE CODE - TAC]
   01: a = 10
   02: t1 = b * 4
   03: t2 = t1 / 2
   04: t3 = a + t2
   ...

[PHASE 4] Backend Code Generation...

[TARGET CODE - ASSEMBLY PREVIEW]
.data
.text
global _start
_start:
    ; a = 10
    MOV EAX, 10
    MOV [a], EAX
    ; t1 = b * 4
    MOV EAX, b
    IMUL EAX, 4
    MOV [t1], EAX
    ...

--------------------------------------------------
✅ [SUCCESS] Kompilasi Selesai! Output disimpan di 'output.asm'