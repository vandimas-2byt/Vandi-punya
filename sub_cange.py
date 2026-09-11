import re

class SubCange:
    def __init__(self, env):
        self.env = env

    def eksekusi(self, daftar_instruksi, daftar_imports):
        """Memproses instruksi dari blok include{%.cange}"""
        # 1. Menghubungkan modul/library yang di-import dari blok pie agar bisa diakses di cange
        lokal_vars = self.env.dapatkan_semua().copy()
        for lib in daftar_imports:
            try:
                exec(f"import {lib}", globals())
            except Exception as e:
                pass

        # 2. Penggabungan kode berdasarkan aturan /jan
        kode_siap_eksekusi = []
        baris_sementara = []

        for item in daftar_instruksi:
            if item["type"] == "code":
                baris = item["value"].strip()
                # Mengabaikan komentar C
                if baris.startswith("//") or baris.startswith("/*"):
                    continue
                
                # Penerjemah sederhana perintah printf khas C ke fungsi cetak
                baris_terjemahan = self._terjemahkan_sintaks_c(baris)
                baris_sementara.append(baris_terjemahan)

            elif item["type"] == "jan":
                kode_siap_eksekusi.append(" ".join(baris_sementara))
                baris_sementara = []

        if baris_sementara:
            kode_siap_eksekusi.append(" ".join(baris_sementara))

        script_cange = "\n".join(kode_siap_eksekusi)

        # 3. Eksekusi kode matematika / fungsi C
        try:
            exec(script_cange, globals(), lokal_vars)
            self.env.perbarui_dari_dict(lokal_vars)
        except Exception as e:
            print(f"[Error Runtime Cange]: {e}")

    def _terjemahkan_sintaks_c(self, baris):
        """Menerjemahkan sintaks C sederhana (seperti printf dan deklarasi tipe data)"""
        # Hapus titik koma di akhir baris khas C jika ada
        if baris.endswith(";"):
            baris = baris[:-1].strip()

        # Konversi printf("%d", hasil) -> print(hasil)
        pola_printf = r'printf\s*\(\s*"[^"]*"\s*,\s*(.+)\)'
        match_printf = re.match(pola_printf, baris)
        if match_printf:
            argumen = match_printf.group(1).strip()
            return f"print({argumen})"

        # Hapus tipe data khas C (int, float, double, char) saat deklarasi variabel
        baris = re.sub(r'^(int|float|double|char)\s+', '', baris)

        return baris
