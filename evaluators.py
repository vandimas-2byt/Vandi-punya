from environment import Environment
from sub_jas import SubJas
from sub_pie import SubPie
from sub_cange import SubCange

class Evaluator:
    def __init__(self):
        # Membuka memori variabel terpusat
        self.env = Environment()
        self.sub_jas = SubJas(self.env)
        self.sub_pie = SubPie(self.env)
        self.sub_cange = SubCange(self.env)

    def eksekusi(self, struktur_ast):
        """
        Menjalankan alur program berdasarkan urutan blok di file .rbx
        """
        daftar_imports = struktur_ast.get("imports", [])
        urutan_blok = struktur_ast.get("urutan_blok", [])

        # Jika parser belum menyediakan urutan_blok, gunakan urutan berbasis deteksi
        if not urutan_blok:
            urutan_blok = self._deteksi_urutan(struktur_ast)

        # Melacak urutan blok jas dan pie
        posisi_jas = urutan_blok.index("jas") if "jas" in urutan_blok else -1
        posisi_pie = urutan_blok.index("pie") if "pie" in urutan_blok else -1

        for modul in urutan_blok:
            if modul == "jas":
                # Jika JAS ditulis SEBELUM PIE -> JAS jadi penampung variabel
                # Jika JAS ditulis SETELAH PIE -> JAS jadi mesin utama (logika, loop, override var PIE)
                if posisi_pie != -1 and posisi_jas > posisi_pie:
                    self.sub_jas.eksekusi(struktur_ast["jas"], mode="mesin_utama")
                else:
                    self.sub_jas.eksekusi(struktur_ast["jas"], mode="penampung")

            elif modul == "pie":
                self.sub_pie.eksekusi(struktur_ast["pie"], daftar_imports)

            elif modul == "cange":
                # CANGE menelan import yang sama dari PIE
                self.sub_cange.eksekusi(struktur_ast["cange"], daftar_imports)

    def _deteksi_urutan(self, struktur_ast):
        """Mengatur urutan fallback jika tidak ditentukan dari AST"""
        urutan = []
        for k in ["jas", "pie", "cange"]:
            if struktur_ast.get(k):
                urutan.append(k)
        return urutan
