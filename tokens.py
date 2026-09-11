# ==========================================
# DEFINISI TOKEN UNTUK BAHASA RUBIX (.rbx)
# ==========================================

# 1. Kategori Jenis Token (Token Types)
TT_INCLUDE_JAS   = "INCLUDE_JAS"    # include{%.jas}
TT_INCLUDE_PIE   = "INCLUDE_PIE"    # include{%.pie}
TT_INCLUDE_CANGE = "INCLUDE_CANGE"  # include{%.cange}
TT_IMPORT_PIE    = "IMPORT_PIE"     # include{%.pie.import ...}

TT_JAN           = "JAN"            # Perintah /jan (pindah baris)
TT_CODE_BLOCK    = "CODE_BLOCK"     # Teks kode di dalam blok modul
TT_EOF           = "EOF"            # End of File (tanda akhir program)

# 2. Kelas Token untuk Menyimpan Data
class Token:
    def __init__(self, type_, value=None):
        self.type = type_    # Jenis token (misal: TT_INCLUDE_JAS)
        self.value = value  # Isi teksnya (misal: "skor = 100")

    def __repr__(self):
        # Mengubah bentuk token jadi teks agar mudah di-debug/dibaca
        if self.value:
            return f"Token({self.type}, {repr(self.value)})"
        return f"Token({self.type})"
