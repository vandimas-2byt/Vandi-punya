import json

class JSONBridge:
    @staticmethod
    def export_ke_json(data_dict):
        """Mengubah dictionary variabel menjadi string JSON"""
        try:
            return json.dumps(data_dict)
        except Exception as e:
            print(f"[Error JSON Bridge]: Gagal mengkonversi data ke JSON - {e}")
            return "{}"

    @staticmethod
    def import_dari_json(json_str):
        """Mengubah string JSON kembali menjadi dictionary Python"""
        try:
            return json.loads(json_str)
        except Exception as e:
            print(f"[Error JSON Bridge]: Gagal membaca data dari JSON - {e}")
            return {}
