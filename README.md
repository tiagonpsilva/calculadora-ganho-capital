# Calculadora de Imposto sobre Ganho de Capital

## Descrição

Este programa implementa uma calculadora de impostos sobre ganhos de capital para operações no mercado financeiro de ações. A aplicação recebe operações de compra e venda através da entrada padrão (stdin) em formato JSON e calcula o imposto a ser pago para cada operação, seguindo as regras estabelecidas.

## Regras de Cálculo de Imposto

- O imposto é de 20% sobre o lucro obtido em operações de venda
- O preço médio ponderado de compra é recalculado a cada nova operação de compra
- Prejuízos são deduzidos de lucros futuros antes do cálculo do imposto
- Não há imposto quando o valor total da operação (preço × quantidade) for ≤ R$ 20.000,00
- Operações de compra não geram impostos
- Cada linha de entrada é processada independentemente

## Requisitos

- Python 3.6 ou superior
- Não há dependências externas

## Instalação

Clone o repositório:

```bash
git clone https://[url-do-repositorio]/capital-gains.git
cd capital-gains
```

## Uso

Execute o programa através da linha de comando:

```bash
python main.py
```

Você pode fornecer operações diretamente pela entrada padrão ou redirecionar um arquivo:

```bash
python main.py < input.txt
```

### Formato de Entrada

Cada linha da entrada deve conter uma lista de operações em formato JSON:

```json
[{"operation":"buy", "unit-cost":10.00, "quantity": 100}, {"operation":"sell", "unit-cost":15.00, "quantity": 50}]
```

Onde:
- `operation`: Tipo de operação (`"buy"` ou `"sell"`)
- `unit-cost`: Preço unitário da ação
- `quantity`: Quantidade de ações negociadas

### Formato de Saída

Para cada linha processada, o programa retorna uma lista JSON contendo o imposto calculado para cada operação:

```json
[{"tax": 0.0}, {"tax": 0.0}]
```

## Estrutura do Projeto

```
capital-gains/
├── main.py         # Implementação principal da calculadora
├── tests/          # Testes unitários e de integração
│   ├── test_calculator.py
│   └── test_integration.py
└── README.md       # Este arquivo
```

## Arquitetura

O projeto utiliza uma arquitetura simples e direta:

1. `CapitalGainCalculator`: Classe principal que:
   - Mantém o estado atual (preço médio, quantidade de ações, prejuízos acumulados)
   - Implementa a lógica de processamento de operações de compra e venda
   - Calcula o imposto de acordo com as regras de negócio

2. Função principal (`main`):
   - Lê as operações da entrada padrão
   - Instancia o calculador para cada linha de entrada
   - Formata e imprime os resultados

## Testes

O projeto inclui testes unitários e de integração que cobrem todos os casos de uso especificados. Para executar os testes:

```bash
python -m unittest discover tests
```

## Decisões Técnicas

- **Uso da biblioteca padrão**: Optei por utilizar apenas a biblioteca padrão do Python para garantir portabilidade e simplicidade.
- **Uso do módulo `decimal`**: Para garantir precisão nos cálculos financeiros, evitando problemas de arredondamento com pontos flutuantes.
- **Separação de responsabilidades**: A lógica de cálculo foi isolada em uma classe dedicada, facilitando testes e manutenção.
- **Imutabilidade do estado entre simulações**: Cada linha de entrada cria uma nova instância do calculador, garantindo que as simulações sejam independentes.

## Tratamento de Casos Especiais

- **Operações de valor zero**: Tratadas corretamente sem gerar exceções
- **Arredondamento**: Todos os valores são arredondados para 2 casas decimais conforme especificado
- **Validação de entrada**: O programa valida o formato e consistência das operações recebidas