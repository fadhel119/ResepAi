import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

load_dotenv()

def build_steps_chain() -> LLMChain:
    llm = ChatOpenAI(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        base_url="https://api.groq.com/openai/v1",
        api_key=str(os.getenv("GROQ_API_KEY"))
    )

    prompt = PromptTemplate(
        input_variables=["nama_resep", "bahan", "preferensi"],
        template="""
Kamu adalah chef profesional.

Nama resep:
{nama_resep}

Bahan:
{bahan}

Preferensi:
{preferensi}

Buat resep lengkap dengan format:

=====================================
🍽️ {nama_resep}
=====================================

📋 BAHAN-BAHAN:
- ...

👨‍🍳 LANGKAH MEMASAK:
1. ...
2. ...
3. ...
4. ...
5. ...

⏱️ Estimasi waktu: ... menit
👥 Porsi: ... orang

💡 TIPS CHEF:
- ...

=====================================
"""
    )

    return LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )