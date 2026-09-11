import sys

class RubixError:
    """Kelas dasar untuk menangani semua error di bahasa Rubix"""
    
    @staticmethod
    def tampilkan(jenis_error, pesan, baris=None):
        print("\n========================================")
        print(f"[RUBIX ERROR]: {jenis_error}")
        if baris:
            print(f"Lokasi Baris : Baris {baris}")
        print(f"Pesan Error  : {pesan}")
        print("========================================\n")
        sys.exit(1)

class SyntaxErrorRBX:
    """Error jika penulisan sintaksis .rbx salah (misal: tag include salah ketik)"""
    @staticmethod
    def lempar(pesan, baris=None):
        RubixError.tampilkan("Syntax Error (Kesalahan Tata Bahasa)", pesan, baris)

class RuntimeErrorRBX:
    """Error saat kode sedang dijalankan (misal: variabel tidak ditemukan / gagal import)"""
    @staticmethod
    def lempar(pesan, baris=None):
        RubixError.tampilkan("Runtime Error (Kesalahan Eksekusi)", pesan, baris)

class ModulErrorRBX:
    """Error khusus jika ada masalah dalam pemrosesan blok jas, pie, atau cange"""
    @staticmethod
    def lempar(nama_modul, pesan):
        RubixError.tampilkan(f"Modul Error [{nama_modul}]", pesan)
