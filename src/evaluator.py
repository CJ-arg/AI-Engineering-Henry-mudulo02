import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))        


def evaluate_rag_response(user_question, system_answer, chunks_related):
    """
    Agente evaluador que analiza la calidad de la respuesta generada.
    """
    context_text = "\n---\n".join(chunks_related)
    
    prompt = f"""
    Eres un Auditor de Calidad especializado en Sistemas RAG. 
    Tu tarea es evaluar la respuesta de un chatbot de RRHH basándote en los fragmentos recuperados.

    PREGUNTA DEL USUARIO: {user_question}
    RESPUESTA DEL SISTEMA: {system_answer}
    CONTEXTO RECUPERADO (CHUNKS): 
    {context_text}

    Evalúa de 0 a 10 los siguientes puntos:
    1. Relevancia: ¿La respuesta usa la información de los chunks?
    2. Precisión: ¿Es veraz según el contexto? (Sin inventar nada).
    3. Completitud: ¿Responde todos los puntos de la pregunta?

    Responde ESTRICTAMENTE en formato JSON con estas claves:
    - score: (número del 0 al 10)
    - justification: (explicación técnica de por qué ese puntaje)
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        response_format={ "type": "json_object" },
        temperature=0
    )
    
    return json.loads(response.choices[0].message.content)

if __name__ == "__main__":
    
    sample_query = "¿Qué beneficios tengo para mi oficina?"
    sample_answer = "Tienes un bono de USD 500 para silla y monitor renovable cada 24 meses."
    sample_chunks = ["Bono de USD 500 para setup de home office renovable cada 2 años."]

    print("--- Iniciando Evaluación de Calidad ---")
    result = evaluate_rag_response(sample_query, sample_answer, sample_chunks)
    print(json.dumps(result, indent=4, ensure_ascii=False))