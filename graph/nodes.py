import json
import re
from chains.extract_chain import build_extract_chain
from chains.recipe_chain import build_recipe_chain
from chains.steps_chain import build_steps_chain

# Inisialisasi semua chain satu kali saja saat module di-import
extract_chain = build_extract_chain()
recipe_chain = build_recipe_chain()
steps_chain = build_steps_chain()


import urllib.parse

def _parse_json_safe(json_str: str):
    """Parse JSON string safely, removing markdown code blocks if present"""
    try:
        # Remove markdown code blocks if present
        cleaned = re.sub(r'```(?:json)?\s*\n?', '', json_str).strip()
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        raise

def _buat_link_sumber(nama_resep: str) -> str:
    """Buat link Google Search berdasarkan nama resep sebagai referensi sumber"""
    query = f"resep {nama_resep}"
    query_encoded = urllib.parse.quote_plus(query)
    return f"https://www.google.com/search?q={query_encoded}"


def node_ekstrak_bahan(state: dict) -> dict:
    """
    Node 1 — Ekstrak bahan makanan dari input pengguna.
    Input state: user_input (str)
    Output state: bahan (list[str])
    """
    print("\n[NODE 1] Mengekstrak bahan dari input...")

    hasil = extract_chain.run(user_input=state["user_input"])

    try:
        bahan_list = _parse_json_safe(hasil)
        if not isinstance(bahan_list, list):
            bahan_list = []
    except (json.JSONDecodeError, ValueError):
        # Fallback: split manual jika JSON gagal
        bahan_list = [b.strip() for b in state["user_input"].split(",")]

    state["bahan"] = bahan_list
    print(f"[NODE 1] Bahan terdeteksi: {bahan_list}")
    return state


def node_cek_preferensi(state: dict) -> dict:
    """
    Node 2 — Ambil preferensi pengguna dari memory.
    Input state: memory (UserMemory)
    Output state: preferensi (str)
    """
    print("\n[NODE 2] Mengambil preferensi dari memory...")

    user_memory = state["memory"]
    preferensi = user_memory.get_preference_summary()

    state["preferensi"] = preferensi
    print(f"[NODE 2] Preferensi: {preferensi}")
    return state


def node_cari_resep(state: dict) -> dict:
    """
    Node 3 — Cari 3 resep berdasarkan bahan dan preferensi.
    Input state: bahan (list), preferensi (str)
    Output state: resep_list (list[dict])
    """
    print("\n[NODE 3] Mencari resep yang cocok...")

    bahan_str = ", ".join(state["bahan"])
    hasil = recipe_chain.run(
        bahan=bahan_str,
        preferensi=state["preferensi"]
    )

    try:
        resep_data = _parse_json_safe(hasil)
        resep_list = resep_data.get("resep", [])
    except (json.JSONDecodeError, ValueError, AttributeError):
        resep_list = []

    # Tambahkan link sumber ke setiap resep
    for resep in resep_list:
        nama = resep.get("nama", "")
        resep["sumber"] = _buat_link_sumber(nama)

    state["resep_list"] = resep_list
    nama_resep = [r.get("nama", "-") for r in resep_list]
    print(f"[NODE 3] Resep ditemukan: {nama_resep}")
    return state

def node_generate_langkah(state: dict) -> dict:
    """
    Node 4 — Generate langkah memasak lengkap untuk resep pilihan pertama.
    Input state: resep_list (list), bahan (list), preferensi (str)
    Output state: output (str)
    """
    print("\n[NODE 4] Membuat langkah memasak lengkap...")

    if not state["resep_list"]:
        state["output"] = "Maaf, tidak ditemukan resep yang cocok dengan bahan yang tersedia."
        return state

    resep_pilihan = state["resep_list"][0]["nama"]
    bahan_str = ", ".join(state["bahan"])

    hasil = steps_chain.run(
        nama_resep=resep_pilihan,
        bahan=bahan_str,
        preferensi=state["preferensi"]
    )

    state["output"] = hasil
    print(f"[NODE 4] Langkah masak untuk '{resep_pilihan}' berhasil dibuat.")
    return state