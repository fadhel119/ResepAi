from langgraph.graph import StateGraph, END
from graph.nodes import (
    node_ekstrak_bahan,
    node_cek_preferensi,
    node_cari_resep,
    node_generate_langkah
)


def build_graph():
    """
    Bangun dan compile graph LangGraph dengan 4 node berurutan.

    Alur:
    ekstrak_bahan → cek_preferensi → cari_resep → generate_langkah → END
    """
    graph = StateGraph(dict)

    # Daftarkan semua node
    graph.add_node("ekstrak_bahan",    node_ekstrak_bahan)
    graph.add_node("cek_preferensi",   node_cek_preferensi)
    graph.add_node("cari_resep",       node_cari_resep)
    graph.add_node("generate_langkah", node_generate_langkah)

    # Tentukan node pertama yang dijalankan
    graph.set_entry_point("ekstrak_bahan")

    # Sambungkan node satu per satu
    graph.add_edge("ekstrak_bahan",    "cek_preferensi")
    graph.add_edge("cek_preferensi",   "cari_resep")
    graph.add_edge("cari_resep",       "generate_langkah")
    graph.add_edge("generate_langkah", END)

    return graph.compile()