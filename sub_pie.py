import sys
from json_bridge import JSONBridge

class SubPie:
    def __init__(self, env):
        self.env = env

    def eksekusi(self, daftar_instruksi, daftar_imports):
        """Memproses instruksi dari blok include{%.pie}"""
        # 1. Eksekusi Import Library
        for lib in daftar_imports:
            try:
                exec(f"import {lib}", globals())
            except Exception as e:
                print(f"[Error Import Pie]: Gagal meng-import '{lib}' - {e}")

        # 2. Ambil variabel saat ini dari Environment
        lokal_vars = self.env.dapatkan_semua().copy()

        # 3. Gabungkan kode berdasarkan aturan /jan
        kode_siap_eksekusi = []
        baris_sementara = []

        for item in daftar_instruksi:
            if item["type"] == "code":
                baris_sementara.append(item["value"])
            elif item["type"] == "jan":
                # Jika ada /jan, gabungkan baris_sementara dan buat baris baru
                kode_siap_eksekusi.append(" ".join(baris_sementara))
                baris_sementara = []

        if baris_sementara:
            kode_siap_eksekusi.append(" ".join(baris_sementara))

        script_python = "\n".join(kode_siap_eksekusi)

        # 4. Eksekusi kode Python dan update variabel di Environment (Override)
        try:
            exec(script_python, globals(), lokal_vars)
            # Perbarui Environment dengan variabel yang mungkin ditimpa/ditambah oleh Python
            self.env.perbarui_dari_dict(lokal_vars)
        except Exception as e:
            print(f"[Error Runtime Pie]: {e}")
