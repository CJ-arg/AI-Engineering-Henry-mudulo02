import os
import numpy as np
import faiss
from openai import OpenAI
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  


def create_chunks(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0 
    while start <len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def get_embeddings(text_list):
    embeddings = []
    for text in tqdm(text_list, desc="Generando embeddings"):
        response = client.embeddings.create(
            input=text, 
            model="text-embedding-3-small"
        )
        embeddings.append(response.data[0].embedding)
    return np.array(embeddings).astype("float32")

def main():
   print("leyendo archivo de texto")
   with open("data/faq_document.txt", "r", encoding="utf-8") as f:
       text = f.read()
   print("creando fragmentos de texto")
   chunks = create_chunks(text, chunk_size=300, overlap=50)
   print(f"Listo, se crearon {len(chunks)} fragmentos de texto")

   embeddings = get_embeddings(chunks)

   dimension = embeddings.shape[1]
   index = faiss.IndexFlatL2(dimension)
   index.add(embeddings)

   print("Guardando base de conocimientos...")
   faiss.write_index(index, "data/faq_index.bin")
   
   with open("data/faq_chunks.txt", "w", encoding="utf-8") as f:
       for chunk in chunks:
           f.write(chunk.replace("\n", " ") + "\n")
   
   print("¡Indexación exitosa! Archivos guardados en la carpeta data/.")

if __name__ == "__main__":
    main()

  
   







