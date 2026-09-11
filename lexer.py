import config
from tokens import Token, TT_INCLUDE_JAS, TT_INCLUDE_PIE, TT_INCLUDE_CANGE, TT_IMPORT_PIE, TT_JAN, TT_CODE_BLOCK, TT_EOF

class Lexer:
    def __init__(self, teks_sumber):
        self.teks = teks_sumber
        self.posisi = 0
        self.karakter_sekarang = self.teks[0] if len(self.teks) > 0 else None

    def maju(self):
        """Maju satu karakter ke depan"""
        self.posisi += 1
        if self.posisi < len(self.teks):
            self.karakter_sekarang = self.teks[self.posisi]
        else:
            self.karakter_sekarang = None

    def buat_tokens(self):
        """Memproses seluruh teks menjadi daftar Token"""
        tokens = []

        # Memecah teks per baris untuk mempermudah deteksi tag include dan /jan
        baris_baris = self.teks.splitlines()

        for baris in baris_baris:
            baris_bersih = baris.strip()
            if not baris_bersih:
                continue

            # 1. Cek Blok Import Library Python
            if baris_bersih.startswith(config.TAG_PIE_IMPORT):
                # Mengambil nama library, contoh: include{%.pie.import flask} -> flask
                nama_lib = baris_bersih.replace(config.TAG_PIE_IMPORT, "").replace("}", "").strip()
                tokens.append(Token(TT_IMPORT_PIE, nama_lib))

            # 2. Cek Header Modul Utama
            elif baris_bersih == config.TAG_JAS:
                tokens.append(Token(TT_INCLUDE_JAS))
            elif baris_bersih == config.TAG_PIE:
                tokens.append(Token(TT_INCLUDE_PIE))
            elif baris_bersih == config.TAG_CANGE:
                tokens.append(Token(TT_INCLUDE_CANGE))

            # 3. Cek Isi Kode / Operasi /jan
            else:
                # Cek apakah di akhir baris ada perintah /jan
                ada_jan = False
                if baris_bersih.endswith(config.NEWLINE_OPERATOR):
                    ada_jan = True
                    # Hapus kata /jan dari isi kode
                    baris_bersih = baris_bersih[:-len(config.NEWLINE_OPERATOR)].strip()

                if baris_bersih:
                    tokens.append(Token(TT_CODE_BLOCK, baris_bersih))
                
                if ada_jan:
                    tokens.append(Token(TT_JAN))

        # Tanda akhir file
        tokens.append(Token(TT_EOF))
        return tokens
