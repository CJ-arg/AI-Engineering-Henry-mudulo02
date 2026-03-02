import subprocess
import sys

def main():
    print("Iniciando Proceso RAG TechFlow")
    
    print("Ejecutando: build_index.py")
    subprocess.run([sys.executable, "src/build_index.py"])
    
    print("Ejecutando: query.py")
    subprocess.run([sys.executable, "src/query.py"])

    print("Proceso finalizado.")

if __name__ == "__main__":
    main()