import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

load_dotenv()

print("DEBUG GROQ:", os.getenv("GROQ_API_KEY"))

def build_extract_chain() -> LLMChain:
    llm = ChatOpenAI(
        model="llama-3.3-70b-versatile",
        temperature=0,
        base_url="https://api.groq.com/openai/v1",
        api_key=str(os.getenv("GROQ_API_KEY"))
    )

    prompt = PromptTemplate(
        input_variables=["user_input"],
        template="""
Kamu adalah asisten dapur yang ahli mengenali bahan makanan.

Tugasmu: Ekstrak semua bahan makanan yang disebutkan dari kalimat pengguna.
Abaikan kata yang bukan bahan makanan.

Kembalikan HANYA JSON array.

Input:
{user_input}

Contoh:
["telur","tomat","garam"]

Output JSON:
"""
    )

    return LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True
    )