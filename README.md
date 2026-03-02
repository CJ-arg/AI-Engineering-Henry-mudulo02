# Asistente de RRHH TechFlow - Proyecto AI Engineering (RAG)

Este proyecto es una utilidad de procesamiento de lenguaje natural diseñada para actuar como un asistente inteligente de consultas internas para empleados.

El sistema implementa una arquitectura de Generación Aumentada por Recuperación (RAG) que permite responder preguntas sobre políticas, beneficios y procedimientos de la empresa TechFlow, extrayendo información directamente de manuales de texto no estructurados.

## Objetivos del Proyecto
- **Recuperación Semántica**: Implementación de búsqueda vectorial para localizar fragmentos de información relevantes en documentos extensos.
- **Salida Estructurada**: Generación de respuestas en JSON válido que incluyen la respuesta del sistema, los fragmentos recuperados y una auditoría de calidad.
- **Evaluación Automatizada**: Incorporación de un agente crítico que califica la precisión y completitud de cada respuesta generada.
- **Escalabilidad**: Uso de índices vectoriales eficientes para permitir el crecimiento de la base de conocimientos sin degradar la latencia.

## Estructura del Repositorio
- **src/**: Contiene la lógica de indexación (build_index.py), el motor de consulta (query.py) y el módulo de auditoría (evaluator.py).
- **data/**: Almacena el documento fuente (faq_document.txt), el índice vectorial binario (faq_index.bin) y los fragmentos de texto procesados (faq_chunks.txt).
- **outputs/**: Registros JSON con el historial de consultas, respuestas y sus respectivas evaluaciones de calidad (sample_queries.json).

## Configuración e Instalación

1. **Requisitos previos**: Se recomienda el uso de un entorno virtual para la gestión de dependencias.
2. **Entorno Virtual**: Crea y activa tu entorno para mantener las dependencias aisladas.
   - Ejecutar: python -m venv .venv
   - Activar (Windows): source .venv/Scripts/activate
   - Activar (Unix/Mac): source .venv/bin/activate
3. **Instalación de dependencias**:
   - Ejecutar: pip install -r requirements.txt
4. **Variables de Entorno**: Crea un archivo .env en la raíz del proyecto y añade tu API Key:
   - OPENAI_API_KEY=tu_clave_aqui

## Ejecución

Para procesar el documento fuente y construir la base de datos vectorial:
python src/build_index.py

Para ejecutar el pipeline de consultas (RAG) y generar los ejemplos de auditoría:
python src/query.py

## Arquitectura RAG y Búsqueda Vectorial
El sistema implementa una estrategia de recuperación de información optimizada dividida en tres capas:

* **Ingesta y Segmentación (Chunking):** El documento original se divide en fragmentos de 300 caracteres con un solapamiento del 20% (50 caracteres) para asegurar que no se pierda el contexto semántico en los puntos de corte.
* **Indexación de Alta Performance (FAISS):** Se utiliza la librería FAISS (Facebook AI Similarity Search) para realizar búsquedas de vecinos más cercanos (k-NN) sobre los embeddings generados por el modelo text-embedding-3-small.
* **Aumentación y Generación:** El contexto recuperado se inyecta en un prompt sistémico que restringe al modelo gpt-4o-mini a responder exclusivamente con la información proporcionada, minimizando alucinaciones.

## Agente Evaluador de Calidad
A diferencia de los chatbots estándar, este sistema implementa un Agente de Auditoría independiente que valida cada interacción:

* **Análisis en tiempo real:** Evalúa la respuesta del sistema contrastándola con los fragmentos recuperados.
* **Métricas de Precisión:** El agente asigna un puntaje de 0 a 10 basado en tres ejes: relevancia, veracidad y completitud.
* **Justificación Técnica:** Cada evaluación incluye una explicación detallada del puntaje, permitiendo identificar brechas en la documentación o áreas de mejora en el prompt de generación.
* **Persistencia de Auditoría:** Los resultados de la evaluación se integran en el JSON final, cumpliendo con los estándares de observabilidad necesarios para entornos de producción.