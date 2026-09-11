import re

class SubJas:
    def __init__(self, env):
        self.env = env

    def eksekusi(self, daftar_instruksi, mode="penampung"):
        """
        Memproses instruksi dari blok include{%.jas}
        mode = "penampung" (JS hanya untuk buat variabel)
        mode = "mesin_utama" (JS untuk logika, perulangan, matematika, & override variabel)
        """
        if mode == "penampung":
            self._proses_penampung(daftar_instruksi)
        else:
            self._proses_mesin_utama(daftar_instruksi)

    def _proses_penampung(self, daftar_instruksi):
        """Mode Standar: Hanya mengekstrak variabel let/const/var"""
        for item in daftar_instruksi:
            if item["type"] == "code":
                baris = item["value"].strip()
                if baris.startswith("//") or baris.startswith("/*"):
                    continue

                pola = r'^(?:let|const|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*(.+?);?$'
                match = re.match(pola, baris)
                if match:
                    nama_var = match.group(1)
                    nilai_raw = match.group(2).strip()
                    nilai_terproses = self._evaluasi_nilai(nilai_raw)
                    self.env.simpan_variabel(nama_var, nilai_terproses)

    def _proses_mesin_utama(self, daftar_instruksi):
        """Mode Mesin Utama: Menjalankan Logika, Perulangan, & Matematika JS"""
        lokal_vars = self.env.dapatkan_semua().copy()

        # Gabungkan instruksi JS berdasarkan aturan /jan
        kode_siap_eksekusi = []
        baris_sementara = []

        for item in daftar_instruksi:
            if item["type"] == "code":
                baris = item["value"].strip()
                if baris.startswith("//") or baris.startswith("/*"):
                    continue
                # Terjemahkan perintah khas JS ke format eksekusi (seperti console.log -> print)
                baris_terjemahan = self._terjemahkan_js_ke_python(baris)
                baris_sementara.append(baris_terjemahan)
            elif item["type"] == "jan":
                kode_siap_eksekusi.append(" ".join(baris_sementara))
                baris_sementara = []

        if baris_sementara:
            kode_siap_eksekusi.append(" ".join(baris_sementara))

        script_js = "\n".join(kode_siap_eksekusi)

        try:
            # Eksekusi logika JS yang sudah disesuaikan dan timpa variabel di Environment
            exec(script_js, globals(), lokal_vars)
            self.env.perbarui_dari_dict(lokal_vars)
        except Exception as e:
            print(f"[Error Runtime Jas (Mesin Utama)]: {e}")

    def _terjemahkan_js_ke_python(self, baris):
        """Menerjemahkan sintaks JS sederhana agar bisa berjalan sebagai logika utama"""
        if baris.endswith(";"):
            baris = baris[:-1].strip()

        # console.log("...") -> print("...")
        baris = re.sub(r'console\.log\s*\((.*)\)', r'print(\1)', baris)

        # Hapus let/const/var jika ada di tengah logika
        baris = re.sub(r'^(let|const|var)\s+', '', baris)
        return baris

    def _evaluasi_nilai(self, nilai_str):
        if (nilai_str.startswith('"') and nilai_str.endswith('"')) or \
           (nilai_str.startswith("'") and nilai_str.endswith("'")):
            return nilai_str[1:-1]
        try:
            if '.' in nilai_str:
                return float(nilai_str)
            return int(nilai_str)
        except ValueError:
            pass
        if nilai_str == "true": return True
        if nilai_str == "false": return False
        return nilai_str
