import os
import faiss
import numpy as np
import json
from openai import OpenAI
from dotenv import load_dotenv
from evaluator import evaluate_rag_response

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))    

try:
    index = faiss.read_index("data/faq_index.bin")
    with open("data/faq_chunks.txt", "r", encoding="utf-8") as f:
        chunks = [line.strip() for line in f.readlines()]
except Exception as e:
    print(f"Error cargando la base de datos: {e}")
    exit()

def search_top_chunks(query,index,k=3):
    response = client.embeddings.create(
        input=query, 
        model="text-embedding-3-small"
    )
    query_vec = np.array([response.data[0].embedding]).astype("float32")

    distances, indices = index.search(query_vec, k)
    return [chunks[i] for i in indices[0]]
            
def generate_answer(question, context_chunks):
    context_text = "\n\n".join(context_chunks)
    system_prompt = f"""
    Eres un asistente de RRHH de TechFlow. 
    Responde la pregunta basándote ÚNICAMENTE en este contexto:
    
    {context_text}
    
    Si la respuesta no está, di: 'No tengo esa información en mis registros'.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ],
        temperature=0 
    )
    return response.choices[0].message.content

def main():
   
    queries = [
        "¿Cómo funcionan las vacaciones y qué son los días de bienestar?",
        "¿Qué equipamiento me dan para trabajar desde casa?",
        "¿Cuál es el proceso de desvinculación y propiedad intelectual?"
    ]
    
    all_results = []
        
    for q in queries:
        try:
            relevant_chunks = search_top_chunks(q, index, k=3)
            answer = generate_answer(q, relevant_chunks)
            evaluation = evaluate_rag_response(q, answer, relevant_chunks)
            
            result = {
                "user_question": q,
                "system_answer": answer,
                "chunks_related": relevant_chunks,
                "evaluation": evaluation
            }
          
            all_results.append(result)
            print(f"--- Procesado: {q} ---")

        except Exception as e:
            print(f"Error procesando la pregunta '{q}': {e}")

    output_path = "outputs/sample_queries.json"
    os.makedirs("outputs", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=4, ensure_ascii=False)
    
    print(f"\nProceso finalizado. Archivo guardado en: {output_path}")
 

if __name__ == "__main__":
    main()