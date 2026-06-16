import streamlit as st
from graph.workflow import build_graph
from memory.user_memory import UserMemory

st.set_page_config(
    page_title="Asisten Resep AI",
    page_icon="🍳",
    layout="wide"
)

# Session State
if "memory" not in st.session_state:
    st.session_state.memory = UserMemory()

if "graph" not in st.session_state:
    st.session_state.graph = build_graph()

# Header
st.title("🍳 Asisten Resep AI")
st.markdown(
    "Temukan resep berdasarkan bahan yang tersedia di dapur Anda."
)

# Sidebar
with st.sidebar:
    st.header("⚙️ Preferensi")

    vegetarian = st.checkbox(
        "Vegetarian",
        value=st.session_state.memory.preferences["vegetarian"]
    )

    st.session_state.memory.preferences["vegetarian"] = vegetarian

    alergi = st.text_input(
        "Alergi Bahan",
        placeholder="contoh: kacang"
    )

    if st.button("➕ Simpan Alergi"):
        if alergi:
            st.session_state.memory.add_alergi(alergi)
            st.success(f"Alergi '{alergi}' disimpan")

    st.divider()

    st.subheader("📖 Riwayat")

    history = st.session_state.memory.get_history_string()

    if history:
        st.text_area(
            "",
            history,
            height=300
        )
    else:
        st.info("Belum ada riwayat")

# Input Utama
bahan_input = st.text_area(
    "🥬 Masukkan bahan yang tersedia",
    placeholder="telur, tomat, bawang, garam",
    height=120
)

if st.button("🔍 Cari Resep", use_container_width=True):

    if not bahan_input.strip():
        st.warning("Masukkan bahan terlebih dahulu")
        st.stop()

    with st.spinner("Sedang mencari resep terbaik..."):

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

            st.success("Resep berhasil ditemukan!")

            # Resep Utama
            st.subheader("🍽️ Resep Utama")

            st.markdown(
                f"""
<div style="padding:20px;border-radius:10px;border:1px solid #ddd;">
<pre>{hasil["output"]}</pre>
</div>
""",
                unsafe_allow_html=True
            )

            # Alternatif
            resep_list = hasil.get("resep_list", [])

            if len(resep_list) > 1:

                st.subheader("📌 Resep Alternatif")

                cols = st.columns(len(resep_list)-1)

                for idx, resep in enumerate(resep_list[1:]):

                    with cols[idx]:
                        st.card = st.container()

                        with st.card:
                            st.markdown(
                                f"""
### {resep.get("nama","-")}

**Kesulitan:** {resep.get("tingkat_kesulitan","-")}

**Waktu:** {resep.get("waktu_masak","-")}
"""
                            )

            st.session_state.memory.save_to_memory(
                bahan_input,
                hasil["output"]
            )

        except Exception as e:
            st.error(f"Error: {e}")