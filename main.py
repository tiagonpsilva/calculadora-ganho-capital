import json
import sys
import os 
from CalculadoraGanhoCapital import CalculadoraGanhoCapital
import logging
import argparse
import time

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "level": record.levelname,
            "message": record.getMessage(),
            "time": self.formatTime(record, self.datefmt),
            "module": record.module,
            "function": record.funcName,
        }
        return json.dumps(log_record)

def main():
    """Função principal para processar um arquivo de operações informado pelo usuário."""
    parser = argparse.ArgumentParser(description="Calculadora de Imposto sobre Ganho de Capital")
    parser.add_argument("file_path", help="Caminho do arquivo JSON de operações")
    parser.add_argument("--log-level", default="INFO", help="Nível de log: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    args = parser.parse_args()

    # Configuração do logger
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO), handlers=[handler])
    logger = logging.getLogger("calculadora")

    start_time = time.time()
    logger.info(f"Iniciando processamento do arquivo: {args.file_path}")
    calculadora = CalculadoraGanhoCapital()
    resultados = calculadora.processar_arquivo(args.file_path, logger=logger)
    end_time = time.time()

    if resultados:
        print(json.dumps(resultados, indent=2))
        logger.info(f"Processamento concluído. Operações: {len(resultados)} | Tempo: {end_time - start_time:.3f}s | Erros: {sum(1 for r in resultados if 'error' in r)}")
    else:
        logger.error("Nenhum resultado processado.")


if __name__ == "__main__":
    main()