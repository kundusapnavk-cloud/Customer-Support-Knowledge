# Why: this is where retrieval becomes RAG. The LLM is instructed to answer from retrieved knowledge instead of relying freely on its own knowledge.
from groq import Groq

client = Groq()


def generate_answer(query: str, context: str) -> str:
    prompt = f"""
You are a customer support assistant.

Answer the customer's question using ONLY the provided context.

Rules:
- If the context contains enough information to answer, answer directly.
- Combine information from multiple context sections when needed.
- Do not invent information.
- Only say "I could not find this information in the support knowledge base."
  when the context truly does not contain the answer.

Context:
{context}

Customer question:
{query}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content