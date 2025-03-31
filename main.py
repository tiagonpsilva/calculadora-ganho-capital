import json
import sys
import os 
from CalculadoraGanhoCapital import CalculadoraGanhoCapital


def main():
    """Função principal para processar um arquivo de operações informado pelo usuário."""
    if len(sys.argv) != 2:
        print("Uso: python main.py <caminho_do_arquivo_json>")
        print("Exemplo: python main.py operations-samples/case1.json")
        return
    
    file_path = sys.argv[1]
    calculadora = CalculadoraGanhoCapital()
    resultados = calculadora.processar_arquivo(file_path)
    
    if resultados:
        print(json.dumps(resultados, indent=2))


if __name__ == "__main__":
    main()