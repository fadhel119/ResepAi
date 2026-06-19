from langchain_classic.memory import ConversationBufferMemory

class UserMemory:
    def __init__(self):
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.preferences = {
            "vegetarian": False,
            "alergi": [],
            "masakan_favorit": []
        }
        self.riwayat_judul = []  # daftar judul resep yang pernah dicari

    def update_preference(self, key, value):
        """Update satu preferensi pengguna"""
        self.preferences[key] = value

    def add_alergi(self, bahan: str):
        """Tambahkan satu item alergi"""
        if bahan not in self.preferences["alergi"]:
            self.preferences["alergi"].append(bahan)

    def get_preference_summary(self) -> str:
        """Ubah preferensi menjadi kalimat untuk dimasukkan ke prompt"""
        prefs = self.preferences
        summary = []

        if prefs["vegetarian"]:
            summary.append("pengguna adalah vegetarian, jangan gunakan daging")

        if prefs["alergi"]:
            alergi_str = ", ".join(prefs["alergi"])
            summary.append(f"pengguna alergi terhadap: {alergi_str}")

        if prefs["masakan_favorit"]:
            favorit_str = ", ".join(prefs["masakan_favorit"])
            summary.append(f"pengguna menyukai masakan: {favorit_str}")

        if not summary:
            return "tidak ada preferensi khusus"

        return ". ".join(summary) + "."

    def save_to_memory(self, human_msg: str, ai_msg: str):
        """Simpan satu giliran percakapan ke memory"""
        self.memory.save_context(
            {"input": human_msg},
            {"output": ai_msg}
        )

    def get_history(self) -> dict:
        """Ambil seluruh riwayat percakapan"""
        return self.memory.load_memory_variables({})

    def get_history_string(self) -> str:
        """Ambil riwayat percakapan dalam format string"""
        history = self.get_history()
        messages = history.get("chat_history", [])
        if not messages:
            return "Belum ada riwayat percakapan."
        result = []
        for msg in messages:
            role = "Kamu" if msg.type == "human" else "Asisten"
            result.append(f"{role}: {msg.content}")
        return "\n".join(result)

    def add_riwayat_judul(self, nama_resep: str):
        """Tambahkan judul resep ke riwayat singkat"""
        if nama_resep:
            self.riwayat_judul.append(nama_resep)

    def get_riwayat_judul(self) -> list:
        """Ambil daftar judul resep yang pernah dicari"""
        return self.riwayat_judul