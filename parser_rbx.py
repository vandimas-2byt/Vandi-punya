from tokens import (
    TT_INCLUDE_JAS, TT_INCLUDE_PIE, TT_INCLUDE_CANGE,
    TT_IMPORT_PIE, TT_JAN, TT_CODE_BLOCK, TT_EOF
)

class ParserRBX:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posisi = 0
        self.token_sekarang = self.tokens[0] if len(self.tokens) > 0 else None

    def maju(self):
        self.posisi += 1
        if self.posisi < len(self.tokens):
            self.token_sekarang = self.tokens[self.posisi]

    def parse(self):
        struktur_ast = {
            "imports": [],
            "jas": [],
            "pie": [],
            "cange": [],
            "urutan_blok": []  # Mencatat urutan kemunculan modul
        }

        modul_aktif = None

        while self.token_sekarang and self.token_sekarang.type != TT_EOF:
            token = self.token_sekarang

            if token.type == TT_IMPORT_PIE:
                struktur_ast["imports"].append(token.value)

            elif token.type == TT_INCLUDE_JAS:
                modul_aktif = "jas"
                if "jas" not in struktur_ast["urutan_blok"]:
                    struktur_ast["urutan_blok"].append("jas")

            elif token.type == TT_INCLUDE_PIE:
                modul_aktif = "pie"
                if "pie" not in struktur_ast["urutan_blok"]:
                    struktur_ast["urutan_blok"].append("pie")

            elif token.type == TT_INCLUDE_CANGE:
                modul_aktif = "cange"
                if "cange" not in struktur_ast["urutan_blok"]:
                    struktur_ast["urutan_blok"].append("cange")

            elif token.type == TT_CODE_BLOCK:
                if modul_aktif:
                    struktur_ast[modul_aktif].append({"type": "code", "value": token.value})

            elif token.type == TT_JAN:
                if modul_aktif:
                    struktur_ast[modul_aktif].append({"type": "jan"})

            self.maju()

        return struktur_ast
