# Asistente de RRHH TechFlow - Sistema RAG de Consultas Internas

## Descripción del Proyecto
Este proyecto consiste en el desarrollo de un chatbot de preguntas frecuentes (FAQ) para la empresa TechFlow, diseñado para resolver dudas de los empleados sobre políticas internas, beneficios y cultura organizacional. La solución utiliza una arquitectura de Generación Aumentada por Recuperación (RAG) para conectar un modelo de lenguaje avanzado (GPT-4o-mini) con una base de conocimientos específica y actualizada. El sistema permite que el personal obtenga respuestas precisas fundamentadas en documentos oficiales, reduciendo la carga de trabajo del equipo de RRHH y garantizando la consistencia en la información proporcionada.



## Beneficios de la Arquitectura RAG
La implementación de RAG en este chatbot ofrece tres ventajas críticas:
1. **Conocimiento Actualizable**: Permite integrar nuevas políticas simplemente indexando nuevos documentos, sin necesidad de reentrenar el modelo.
2. **Reducción de Alucinaciones**: Al restringir al LLM a responder únicamente basándose en los fragmentos recuperados, se minimiza la generación de información falsa.
3. **Atribución de Fuentes**: El sistema identifica y devuelve los fragmentos exactos utilizados para generar la respuesta, permitiendo la auditoría y verificación de la información.

## Estructura del Repositorio
* **src/**: Módulos de lógica (build_index.py, query.py, evaluator.py).
* **data/**: Documento fuente (faq_document.txt) e índices generados (faq_index.bin).
* **outputs/**: Resultados de pruebas con evaluación (sample_queries.json).

## Configuración e Instalación

1. **Entorno Virtual**:
   python -m venv .venv
   source .venv/Scripts/activate # En Windows: .venv\Scripts\activate

2. **Instalación de Dependencias**:
   pip install -r requirements.txt

3. **Variables de Entorno**:
   Crear un archivo .env en la raíz y configurar la clave de OpenAI:
   OPENAI_API_KEY=tu_api_key_aqui

## Instrucciones de Uso

1. **Etapa de Indexación**: Procesa el documento y genera los vectores.
   python src/build_index.py

2. **Etapa de Consulta y Evaluación**: Ejecuta el pipeline de RAG y audita las respuestas.
   python src/query.py

## Decisiones Técnicas
* **Estrategia de Chunking**: Se utilizó un método de tamaño fijo con un chunk_size de 300 caracteres y un overlap de 50. Esta configuración asegura que cada fragmento mantenga suficiente contexto semántico para ser comprendido por el modelo sin exceder los límites de tokens.
* **Búsqueda Vectorial**: Se implementó la técnica de k-Nearest Neighbors (k-NN) mediante la librería FAISS, utilizando la Distancia Euclidiana (L2) para calcular la similitud. Se eligió este método por su alta velocidad de respuesta y precisión en la recuperación de embeddings de alta dimensionalidad.

## Formato de Salida (JSON)
El sistema genera un objeto estructurado para cada consulta con el siguiente formato:
- user_question: La pregunta original.
- system_answer: La respuesta generada por el LLM.
- chunks_related: Lista de fragmentos recuperados de la base vectorial.
- evaluation: Objeto con score (0-10) y justificativo generado por el Agente Evaluador.