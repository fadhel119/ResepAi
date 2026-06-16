import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

load_dotenv()

def build_recipe_chain() -> LLMChain:
    llm = ChatOpenAI(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        base_url="https://api.groq.com/openai/v1",
        api_key=str(os.getenv("GROQ_API_KEY"))
    )

    prompt = PromptTemplate(
        input_variables=["bahan", "preferensi"],
        template="""
Kamu adalah chef profesional.

Bahan tersedia:
{bahan}

Preferensi:
{preferensi}

Berikan tepat 3 rekomendasi resep.

Output HARUS JSON:

{{
  "resep": [
    {{
      "nama": "nama resep",
      "tingkat_kesulitan": "mudah",
      "waktu_masak": "15 menit",
      "bahan_utama_dipakai": ["bahan1","bahan2"]
    }}
  ]
}}
"""
    )

    return LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )