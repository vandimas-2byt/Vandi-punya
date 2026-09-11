# ==========================================
# PENGELOLA MEMORI VARIABEL (ENVIRONMENT)
# ==========================================

class Environment:
    def __init__(self):
        # Tempat menyimpan variabel (nama_variabel: nilai_variabel)
        self.variabel = {}

    def simpan_variabel(self, nama, nilai):
        """Menyimpan atau menimpa nilai variabel"""
        self.variabel[nama] = nilai

    def ambil_variabel(self, nama):
        """Mengambil nilai variabel berdasarkan nama"""
        return self.variabel.get(nama, None)

    def ada_variabel(self, nama):
        """Mengecek apakah variabel sudah pernah dideklarasikan"""
        return nama in self.variabel

    def dapatkan_semua(self):
        """Mengembalikan seluruh dictionary variabel"""
        return self.variabel

    def perbarui_dari_dict(self, data_dict):
        """Menimpa atau menambah variabel secara masal dari dictionary"""
        self.variabel.update(data_dict)
