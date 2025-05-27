import unittest
import json
import os
import sys
from CalculadoraGanhoCapital import CalculadoraGanhoCapital

# Adicionado para permitir importar o módulo principal
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestCalculadoraGanhoCapital(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para cada teste."""
        self.calculadora = CalculadoraGanhoCapital()
    
    def test_operacao_compra(self):
        """Testa se operações de compra sempre retornam imposto zero."""
        imposto = self.calculadora.processar_compra(10.00, 100)
        self.assertEqual(imposto, 0.00)
        self.assertEqual(self.calculadora.total_acoes, 100)
        self.assertEqual(self.calculadora.preco_medio_ponderado, 10.00)
    
    def test_preco_medio_ponderado(self):
        """Testa se o preço médio ponderado é calculado corretamente após múltiplas compras."""
        self.calculadora.processar_compra(10.00, 100)  # Total: 1000, Ações: 100, PM: 10
        self.calculadora.processar_compra(20.00, 100)  # Total: 3000, Ações: 200, PM: 15
        self.assertEqual(self.calculadora.preco_medio_ponderado, 15.00)
    
    def test_venda_sem_imposto_valor_baixo(self):
        """Testa venda com valor total abaixo de 20.000."""
        self.calculadora.processar_compra(10.00, 100)
        imposto = self.calculadora.processar_venda(15.00, 50)
        self.assertEqual(imposto, 0.00)  # Valor da operação: 750 (< 20.000)
    
    def test_venda_com_imposto(self):
        """Testa venda com lucro e valor acima de 20.000."""
        self.calculadora.processar_compra(10.00, 10000)  # PM: 10, Total: 10.000 ações
        imposto = self.calculadora.processar_venda(20.00, 5000)  # Lucro: 50.000, Valor: 100.000
        self.assertEqual(imposto, 10000.00)  # 20% de 50.000 = 10.000
    
    def test_venda_sem_imposto_prejuizo(self):
        """Testa venda com prejuízo (não deve gerar imposto mesmo acima de 20.000)."""
        self.calculadora.processar_compra(30.00, 1000)
        imposto = self.calculadora.processar_venda(20.00, 1000)  # Prejuízo: -10.000, Valor: 20.000
        self.assertEqual(imposto, 0.00)

    def test_quantidade_para_venda(self):
        """Testa se tenho ações suficientes para vender."""
        self.calculadora.processar_operacao({"operation": "buy", "unit-cost": 10.00, "quantity": 100})
        with self.assertRaises(Exception):
            self.calculadora.processar_operacao({"operation": "sell", "unit-cost": 10.00, "quantity": 200})
            # Comentário 01
            
     
    def test_operacoes_sequenciais(self):
        """Testa uma sequência completa de operações."""
        operacoes = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 5.00, "quantity": 5000}
        ]
        resultados_esperados = [
            {"tax": 0.00},
            {"tax": 10000.00},
            {"tax": 0.00}
        ]
        
        resultados = self.calculadora.calcular_impostos(operacoes)
        self.assertEqual(resultados, resultados_esperados)
    
    def test_arquivo_json(self):
        """Testa o processamento de um arquivo JSON de exemplo."""
        # Cria um arquivo temporário para teste
        dados_teste = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 5.00, "quantity": 5000}
        ]
        
        # Certifica-se de que o diretório operations-samples existe
        os.makedirs('operations-samples', exist_ok=True)
        
        # Cria o arquivo de teste
        with open('operations-samples/test_case.json', 'w') as f:
            json.dump(dados_teste, f)
        
        try:
            resultados = self.calculadora.processar_arquivo('operations-samples/test_case.json')
            resultados_esperados = [
                {"tax": 0.00},
                {"tax": 10000.00},
                {"tax": 0.00}
            ]
            self.assertEqual(resultados, resultados_esperados)
        finally:
            # Limpa o arquivo de teste
            if os.path.exists('operations-samples/test_case.json'):
                os.remove('operations-samples/test_case.json')


if __name__ == '__main__':
    unittest.main()