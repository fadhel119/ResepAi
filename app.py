import streamlit as st
from graph.workflow import build_graph
from memory.user_memory import UserMemory

st.set_page_config(
    page_title="Asisten Resep AI",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================
# CUSTOM CSS
# ============================
st.markdown("""
<style>
    /* Hilangkan padding atas default */
    .block-container {
        padding-top: 2rem;
    }

    /* Header gradient */
    .main-header {
        background: linear-gradient(135deg, #FF6B6B 0%, #FFA94D 100%);
        padding: 2rem 2.5rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
        box-shadow: 0 8px 24px rgba(255, 107, 107, 0.25);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.1rem;
        font-weight: 800;
    }
    .main-header p {
        color: rgba(255,255,255,0.92);
        margin: 0.4rem 0 0 0;
        font-size: 1.02rem;
    }

    /* Input card */
    .input-card {
        background: #ffffff;
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        border: 1px solid #f0f0f0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.04);
        margin-bottom: 1.5rem;
    }

    /* Resep utama box */
    .resep-utama-box {
        background: #ffffff;
        padding: 1.8rem 2rem;
        border-radius: 18px;
        border: 1px solid #f0e6d8;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        border-left: 6px solid #FF6B6B;
    }
    .resep-utama-box pre {
        white-space: pre-wrap;
        font-family: 'Source Code Pro', monospace;
        font-size: 0.92rem;
        line-height: 1.6;
        background: transparent;
        border: none;
        color: #333;
    }

    /* Link sumber resep utama */
    .sumber-utama {
        margin-top: 0.7rem;
        padding-left: 0.2rem;
    }
    .sumber-utama a {
        font-size: 0.88rem;
        color: #FF6B6B;
        font-weight: 600;
        text-decoration: none;
    }
    .sumber-utama a:hover {
        text-decoration: underline;
    }

    /* Resep alternatif card */
    .alt-card {
        background: #fff;
        border-radius: 14px;
        padding: 1.2rem 1.3rem;
        border: 1px solid #eee;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        height: 100%;
        transition: transform 0.15s ease;
    }
    .alt-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }
    .alt-card h4 {
        margin: 0 0 0.6rem 0;
        color: #FF6B6B;
        font-size: 1.05rem;
    }
    .alt-card a {
        font-size: 0.85rem;
        color: #FF6B6B;
        font-weight: 600;
        text-decoration: none;
    }
    .alt-card a:hover {
        text-decoration: underline;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 0.4rem;
        margin-bottom: 0.3rem;
    }
    .badge-time {
        background: #FFF3E0;
        color: #E8862E;
    }
    .badge-level {
        background: #E8F5E9;
        color: #2E7D32;
    }

    /* Sidebar styling */
    .sidebar-pref-badge {
        background: #FFF0EB;
        color: #FF6B6B;
        padding: 0.3rem 0.8rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }

    /* Riwayat judul resep */
    .riwayat-item {
        background: #fff;
        border: 1px solid #f0f0f0;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        margin-bottom: 0.5rem;
        font-size: 0.88rem;
        color: #444;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }
    .riwayat-item b {
        color: #FF6B6B;
    }

    section[data-testid="stSidebar"] {
        background: #FAFAFA;
    }

    /* Button styling */
    .stButton button {
        border-radius: 12px;
        font-weight: 700;
        height: 3rem;
        background: linear-gradient(135deg, #FF6B6B 0%, #FFA94D 100%);
        color: white;
        border: none;
        transition: opacity 0.15s ease;
    }
    .stButton button:hover {
        opacity: 0.88;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============================
# SESSION STATE
# ============================
if "memory" not in st.session_state:
    st.session_state.memory = UserMemory()

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

if "hasil_terakhir" not in st.session_state:
    st.session_state.hasil_terakhir = None

# ============================
# HEADER
# ============================
st.markdown("""
<div class="main-header">
    <h1>🍳 Asisten Resep AI</h1>
    <p>Temukan resep terbaik berdasarkan bahan yang tersedia di dapur Anda — didukung oleh AI.</p>
</div>
""", unsafe_allow_html=True)

# ============================
# SIDEBAR
# ============================
with st.sidebar:
    st.markdown("### ⚙️ Preferensi")

    vegetarian = st.checkbox(
        "🌱 Mode Vegetarian",
        value=st.session_state.memory.preferences["vegetarian"]
    )
    st.session_state.memory.preferences["vegetarian"] = vegetarian

    if vegetarian:
        st.markdown('<span class="sidebar-pref-badge">🌱 Vegetarian Aktif</span>', unsafe_allow_html=True)

    st.markdown("---")

    alergi = st.text_input(
        "🚫 Tambah Alergi Bahan",
        placeholder="contoh: kacang"
    )

    if st.button("➕ Simpan Alergi", use_container_width=True):
        if alergi:
            st.session_state.memory.add_alergi(alergi)
            st.success(f"Alergi '{alergi}' disimpan")

    daftar_alergi = st.session_state.memory.preferences.get("alergi", [])
    if daftar_alergi:
        st.markdown("**Alergi tersimpan:**")
        badges = " ".join(
            f'<span class="sidebar-pref-badge">🚫 {a}</span>' for a in daftar_alergi
        )
        st.markdown(badges, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📖 Riwayat Resep")

    riwayat_judul = st.session_state.memory.get_riwayat_judul()

    if riwayat_judul:
        for i, judul in enumerate(reversed(riwayat_judul), start=1):
            st.markdown(
                f'<div class="riwayat-item"><b>{i}.</b> {judul}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info("Belum ada riwayat resep.")

# ============================
# INPUT UTAMA
# ============================
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown("#### 🥬 Bahan yang tersedia")

bahan_input = st.text_area(
    "Bahan yang tersedia",
    placeholder="contoh: telur, tomat, bawang, garam",
    height=110,
    label_visibility="collapsed"
)

cari_clicked = st.button("🔍 Cari Resep", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# ============================
# PROSES PENCARIAN
# ============================
if cari_clicked:

    if not bahan_input.strip():
        st.warning("⚠️ Masukkan bahan terlebih dahulu")
        st.stop()

    with st.spinner("🤖 Sedang mencari resep terbaik untuk Anda..."):

        state = {
            "user_input": bahan_input,
            "memory": st.session_state.memory,
            "bahan": [],
            "preferensi": "",
            "resep_list": [],
            "output": ""
        }

        try:
            hasil = st.session_state.graph.invoke(state)

            # Simpan ke memory riwayat percakapan
            st.session_state.memory.save_to_memory(
                bahan_input,
                hasil["output"]
            )

            # Simpan judul resep utama ke riwayat singkat
            resep_list_sementara = hasil.get("resep_list", [])
            if resep_list_sementara:
                nama_resep_utama = resep_list_sementara[0].get("nama", "Resep tanpa nama")
                st.session_state.memory.add_riwayat_judul(nama_resep_utama)

            # Simpan hasil ke session_state supaya tidak hilang saat rerun
            st.session_state.hasil_terakhir = hasil

            # Rerun supaya sidebar (riwayat) ikut update
            st.rerun()

        except Exception as e:
            st.error(f"❌ Terjadi error: {e}")

# ============================
# TAMPILKAN HASIL TERAKHIR
# ============================
if st.session_state.hasil_terakhir:

    hasil = st.session_state.hasil_terakhir

    st.success("✅ Resep berhasil ditemukan!")

    # ---- Ambil daftar resep ----
    resep_list = hasil.get("resep_list", [])
    resep_utama = resep_list[0] if resep_list else {}
    sumber_utama = resep_utama.get("sumber", "#")

    # ---- Resep Utama ----
    st.markdown("### 🍽️ Resep Utama")
    st.markdown(
        f"""
        <div class="resep-utama-box">
            <pre>{hasil["output"]}</pre>
            <div class="sumber-utama">
                <a href="{sumber_utama}" target="_blank">
                    🔗 Lihat referensi resep serupa di internet
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---- Resep Alternatif ----
    if len(resep_list) > 1:
        st.markdown("### 📌 Resep Alternatif")
        st.write("")

        cols = st.columns(len(resep_list) - 1)

        for idx, resep in enumerate(resep_list[1:]):
            with cols[idx]:
                nama = resep.get("nama", "-")
                kesulitan = resep.get("tingkat_kesulitan", "-")
                waktu = resep.get("waktu_masak", "-")
                sumber = resep.get("sumber", "#")

                st.markdown(
                    f"""
                    <div class="alt-card">
                        <h4>🍲 {nama}</h4>
                        <span class="badge badge-level">📊 {kesulitan}</span>
                        <span class="badge badge-time">⏱️ {waktu}</span>
                        <div style="margin-top:0.6rem;">
                            <a href="{sumber}" target="_blank">
                                🔗 Cari referensi resep
                            </a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )