from dotenv import load_dotenv

load_dotenv()

import config

from graph.workflow import build_graph
from memory.user_memory import UserMemory

def print_banner():
    print("=" * 50)
    print("       🍳  ASISTEN RESEP AI  🍳")
    print("  Powered by LangChain + LangGraph + LangSmith")
    print("=" * 50)
    print("Ketik bahan yang kamu punya, contoh:")
    print("  > telur, tomat, bawang, garam")
    print()
    print("Perintah khusus:")
    print("  vegetarian       → aktifkan mode vegetarian")
    print("  alergi <bahan>   → contoh: alergi kacang")
    print("  riwayat          → lihat riwayat percakapan")
    print("  preferensi       → lihat preferensi tersimpan")
    print("  keluar           → keluar dari program")
    print("=" * 50)
    print()


def handle_special_command(user_input: str, user_memory: UserMemory) -> bool:
    """
    Tangani perintah khusus pengguna.
    Return True jika perintah ditangani, False jika bukan perintah khusus.
    """
    lower = user_input.lower().strip()

    # Perintah: keluar
    if lower == "keluar":
        print("Sampai jumpa! Selamat memasak! 👨‍🍳")
        return "exit"

    # Perintah: aktifkan vegetarian
    if lower == "vegetarian":
        user_memory.update_preference("vegetarian", True)
        print("✅ Mode vegetarian aktif! Resep selanjutnya tidak akan menggunakan daging.\n")
        return True

    # Perintah: tambah alergi
    if lower.startswith("alergi "):
        bahan_alergi = lower.replace("alergi ", "").strip()
        user_memory.add_alergi(bahan_alergi)
        print(f"✅ Alergi '{bahan_alergi}' tersimpan!\n")
        return True

    # Perintah: lihat riwayat
    if lower == "riwayat":
        print("\n📜 RIWAYAT PERCAKAPAN:")
        print("-" * 40)
        print(user_memory.get_history_string())
        print("-" * 40 + "\n")
        return True

    # Perintah: lihat preferensi
    if lower == "preferensi":
        prefs = user_memory.preferences
        print("\n⚙️  PREFERENSI TERSIMPAN:")
        print(f"  Vegetarian   : {'Ya' if prefs['vegetarian'] else 'Tidak'}")
        print(f"  Alergi       : {', '.join(prefs['alergi']) if prefs['alergi'] else 'Tidak ada'}")
        print(f"  Masakan suka : {', '.join(prefs['masakan_favorit']) if prefs['masakan_favorit'] else 'Belum disetel'}")
        print()
        return True

    return False


def main():
    print_banner()

    # Inisialisasi graph dan memory
    graph = build_graph()
    user_memory = UserMemory()

    while True:
        try:
            user_input = input("Kamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSampai jumpa!")
            break

        if not user_input:
            continue

        # Cek perintah khusus dulu
        result = handle_special_command(user_input, user_memory)
        if result == "exit":
            break
        if result is True:
            continue

        # Jalankan graph LangGraph
        print("\n⏳ Sedang memproses...\n")

        state = {
            "user_input": user_input,
            "memory": user_memory,
            "bahan": [],
            "preferensi": "",
            "resep_list": [],
            "output": ""
        }

        try:
            hasil = graph.invoke(state)
        except Exception as e:
            print(f"❌ Terjadi error: {e}\n")
            continue

        # Tampilkan output resep utama
        print("\n" + "=" * 50)
        print(hasil["output"])
        print("=" * 50)

        # Tampilkan 2 resep alternatif lainnya
        resep_list = hasil.get("resep_list", [])
        if len(resep_list) > 1:
            print("\n📌 RESEP ALTERNATIF LAINNYA:")
            for i, resep in enumerate(resep_list[1:], start=2):
                print(f"  {i}. {resep.get('nama', '-')} "
                      f"({resep.get('tingkat_kesulitan', '-')}, "
                      f"{resep.get('waktu_masak', '-')})")
            print()

        print("💬 Ingin resep alternatif? Ketik nama resepnya langsung!\n")

        # Simpan ke memory
        user_memory.save_to_memory(user_input, hasil["output"])


if __name__ == "__main__":
    main()