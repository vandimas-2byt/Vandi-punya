import sys
import os
import json
import config
from lexer import Lexer
from parser_rbx import ParserRBX
from evaluators import Evaluator

REGISTRY_FILE = "registry.json"

def muat_registry():
    if os.path.exists(REGISTRY_FILE):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)
    return {}

def simpan_registry(data):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def jalankan_kode_rbx(kode_sumber, nama_program):
    lexer = Lexer(kode_sumber)
    tokens = lexer.buat_tokens()

    parser = ParserRBX(tokens)
    pohon_ast = parser.parse()

    evaluator = Evaluator()
    evaluator.eksekusi(pohon_ast)

def main():
    args = sys.argv[1:]
    
    if not args:
        print("Aturan Pakai:")
        print("  1. Daftar modul  : rubix -m -d \"nama_panggilan\" <file.rbx>")
        print("  2. Panggil modul : rubix <nama_panggilan>")
        sys.exit(1)

    registry = muat_registry()

    # Fitur 1: Opsi Registrasi Modul -> rubix -m -d "nama_panggilan" file.rbx
    if len(args) >= 3 and args[0] == "-m" and args[1] == "-d":
        nama_alias = args[2]
        # Jika ada argumen ke-4 (nama file), daftarkan file tersebut
        file_target = args[3] if len(args) > 3 else f"{nama_alias}.rbx"

        if not os.path.exists(file_target):
            print(f"[Error Rubix]: File '{file_target}' tidak ditemukan untuk didaftarkan!")
            sys.exit(1)

        registry[nama_alias] = os.path.abspath(file_target)
        simpan_registry(registry)
        print(f"[Rubix Registry]: Modul '{nama_alias}' berhasil didaftarkan -> {file_target}")
        return

    # Fitur 2: Memanggil Nama Alias -> rubix nama_panggilan
    nama_panggilan = args[0]
    
    if nama_panggilan in registry:
        path_file = registry[nama_panggilan]
        if not os.path.exists(path_file):
            print(f"[Error Rubix]: File terdaftar '{path_file}' sudah tidak ada!")
            sys.exit(1)

        with open(path_file, 'r', encoding='utf-8') as f:
            kode_sumber = f.read()

        jalankan_kode_rbx(kode_sumber, nama_panggilan)

    # Fallback: Jika pengguna langsung memasukkan file .rbx (misal: rubix program.rbx)
    elif nama_panggilan.endswith(config.EXTENSION) and os.path.exists(nama_panggilan):
        with open(nama_panggilan, 'r', encoding='utf-8') as f:
            kode_sumber = f.read()
        jalankan_kode_rbx(kode_sumber, nama_panggilan)

    else:
        print(f"[Error Rubix]: Modul atau file '{nama_panggilan}' tidak ditemukan!")
        sys.exit(1)

if __name__ == "__main__":
    main()
