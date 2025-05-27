import json
class CalculadoraGanhoCapital:
    """Classe para cálculo de imposto sobre ganho de capital em operações financeiras."""
    
    def __init__(self):
        """Inicializa o calculador de impostos."""
        self.preco_medio_ponderado = 0
        self.total_acoes = 0
        self.erros = 0
    
    def processar_compra(self, custo_unitario, quantidade, logger=None):
        """
            Processa uma operação de compra e retorna o imposto (sempre zero).
        Args:
            self: instância da classe
            custo_unitario (float): preço unitário de compra
            quantidade (int): quantidade de ações compradas
        Returns:    
            float: valor do imposto a ser pago (0.00 se não houver imposto)
        """
        if logger:
            logger.debug(f"Processando compra: unit-cost={custo_unitario}, quantity={quantidade}")
        custo_total = self.preco_medio_ponderado * self.total_acoes + custo_unitario * quantidade
        self.total_acoes += quantidade
        
        if self.total_acoes > 0:
            self.preco_medio_ponderado = custo_total / self.total_acoes
        else:
            self.preco_medio_ponderado = 0
            
        # Não há imposto em operações de compra
        return 0.00
    
    def processar_venda(self, custo_unitario, quantidade, logger=None):
        """
            Processa uma operação de venda e retorna o imposto calculado.
            Args:  
                self: instância da classe
                custo_unitario (float): preço unitário de venda
                quantidade (int): quantidade de ações vendidas
            Returns:
                float: valor do imposto a ser pago (0.00 se não houver imposto)
        """
        if logger:
            logger.debug(f"Processando venda: unit-cost={custo_unitario}, quantity={quantidade}")
        # Calcula lucro/prejuízo
        lucro = (custo_unitario - self.preco_medio_ponderado) * quantidade
        
        # Calcula imposto (20% sobre o lucro, apenas se valor total da operação > 20000)
        valor_operacao = custo_unitario * quantidade
        imposto = 0.0
        
        if valor_operacao > 20000 and lucro > 0:
            imposto = lucro * 0.2
        
        # Atualiza o total de ações
        self.total_acoes -= quantidade
        
        return round(imposto, 2)
    
    def processar_operacao(self, operacao, logger=None):
        """
            Processa uma única operação e retorna o imposto calculado.
            Args:
                self: instância da classe
                operacao (dict): dicionário com informações da operação
            Returns:    
                float: valor do imposto a ser pago
        """
        tipo_op = operacao["operation"]
        custo_unitario = operacao["unit-cost"]
        quantidade = operacao["quantity"]
        if logger:
            logger.info(f"Operação: {tipo_op}, unit-cost={custo_unitario}, quantity={quantidade}")
       # print(f"Operação: {tipo_op}, Custo Unitário: {custo_unitario}, Quantidade: {quantidade}")
      
    
        if tipo_op == "buy":
            return self.processar_compra(custo_unitario, quantidade, logger=logger)
              
        elif tipo_op == "sell":
             if(quantidade <=self.total_acoes):
                return self.processar_venda(custo_unitario, quantidade, logger=logger)
             else:
                if logger:
                    logger.error(f"Tentativa de venda de {quantidade} ações, mas apenas {self.total_acoes} disponíveis.")
                raise ValueError("Can't sell more stocks than you have")
        else:
            if logger:
                logger.error(f"Tipo de operação desconhecido: {tipo_op}")
            raise ValueError(f"Tipo de operação desconhecido: {tipo_op}")
    
    def calcular_impostos(self, operations, logger=None):
        """
            Calcula impostos para uma lista de operações de compra/venda.
            Args:
                self: instância da classe
                operations (list): lista de dicionários com operações
            Returns:
                list: lista de dicionários com os impostos calculados
        """
        resultados = [] 
        
        for operacao in operations:
            try:
                imposto = self.processar_operacao(operacao, logger=logger)
                resultados.append({"tax": imposto})
            except Exception as e:
                if logger:
                    logger.error(f"Erro ao processar operação: {operacao} | Erro: {str(e)}")
                self.erros += 1
                resultados.append({"error": str(e)})
        return resultados


    def processar_arquivo(self,file_path, logger=None):
        """
            Processa um único arquivo JSON de operações.
            Args:
                file_path (str): caminho do arquivo JSON
            Returns:
                list: lista de dicionários com os impostos calculados
        """
        if logger:
            logger.info(f"Lendo arquivo: {file_path}")
        try:
            with open(file_path, 'r') as f:
                operations = json.load(f)
            if logger:
                logger.info(f"Arquivo lido com sucesso. Total de operações: {len(operations)}")
            
            resultados = self.calcular_impostos(operations, logger=logger)
            return resultados
        except FileNotFoundError:
            if logger:
                logger.error(f"Arquivo '{file_path}' não encontrado.")
            return None
        except Exception as e:
            if logger:
                logger.error(f"Erro ao processar arquivo '{file_path}': {str(e)}")
            return None
