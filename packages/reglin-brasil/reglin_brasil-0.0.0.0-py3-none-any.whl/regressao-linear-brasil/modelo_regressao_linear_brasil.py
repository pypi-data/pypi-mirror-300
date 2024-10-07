import numpy as np

class RegressaoLinearBRC:
    
    def __init__(self):
        
        """
        Inicializa os atributos da classe RegressaoLinearBRC
        
        """
        
        self.coeficientes = None # Coeficientes da regressão linear
        self.y_predito = None # Vetor predito com o modelo ajustado
        self.preditores = None # Número de variáveis preditoras do modelo
        self.num_observacoes = None # Número de observações de predição

    def ajuste(self, X_treino, y_treino):
        
        """
        Ajusta o modelo aos dados de treinamento.
        
        Parâmetros:
        
        X_treino (numpy.ndarray): Matriz das variáveis preditoras de treinamento.
        y_treino (numpy.ndarray): Vetor da variável resposta (verdadeira) de treinamento.
        
        O ajuste retorna os coeficientes (betas) do modelo ajustado.
        
        """
        # ---------- Análise de possível erro ---------- #
        
        # Verificar se os dados de entrada não estão vazios
        if X_treino is None or y_treino is None:
            raise ValueError("Os dados de treino não podem ser vazios.")

        # Verificar se as dimensões de X_treino e y_treino são compatíveis
        if X_treino.shape[0] != len(y_treino):
            raise ValueError("O número de observações em X_treino e y_treino deve ser o mesmo.")
        
        
        # ---------- Ajustar o modelo ---------- #

        # Adicionando coluna com valores 1 para definição do intecepto
        X_bias = np.c_[np.ones(X_treino.shape[0]), X_treino]

        # Calculando os coeficientes beta (incluindo o intercepto)
        try:
            self.coeficientes = np.linalg.inv(X_bias.T.dot(X_bias)).dot(X_bias.T).dot(y_treino)
        
        except np.linalg.LinAlgError:
            raise ValueError("Não foi possível calcular a inversa da matriz. Os dados podem ser linearmente dependentes.")

        return self.coeficientes


    def predizer(self, X_predizer):
        
        """
        Faz previsões com base nas variáveis preditoras fornecidas.
        
        Parâmetros:
        
        X_predizer (numpy.ndarray): Matriz das variáveis preditoras.
        
        Retorna o vetor de previsão.
        """
        
        # ---------- Verificação de possível erro de uso antecipado da predição ---------- #
        
        if self.coeficientes is None:
            raise ValueError("O modelo precisa ser ajustado antes de fazer predições.")
            
        # ---------- Cálculos de predição ---------- #

        # Adicionar termo referente ao intercepto
        X_predizer_bias = np.c_[np.ones(len(X_predizer)), X_predizer]  # Adicionar termo bias
        
        # Realiza a previsão criando o vetor de previsão
        self.y_predito = X_predizer_bias.dot(self.coeficientes)

        return self.y_predito

    
    def equacao(self):
        
        """
        Retorna a equação da regressão linear.
        
        """
        # Armazenamento dos termos para serem retornados em formato da equação da regressão linear
        termos = [f"{self.coeficientes[i]} * X{i}" for i in range(1, len(self.coeficientes))]
        
        return f"{self.coeficientes[0]} + " + " + ".join(termos)
    
    def erro_absoluto_medio(self, y_real):
        
        """
        Calcula o erro absoluto médio (MAE).
        
        Parâmetros:
        
        y_real (numpy.ndarray): Vetor dos valores reais.
        
        """

        # ---------- Verificação de possível passagem de vetor vazio ---------- #
        
        if y_real is None:
            raise ValueError("Os dados reais não podem ser um vetor vazio.")
            
        # ---------- Cálculo ---------- #
        
        # Calcula o erro absoluto médio
        EAM = np.mean(np.abs(y_real - self.y_predito))
        
        return EAM
    
    def erro_quadrado_medio(self, y_real):
        
        """
        Calcula o erro quadrado médio (MSE).
        
        Parâmetros:
        
        y_real (numpy.ndarray): Vetor dos valores reais.
        
        """
        
        # ---------- Verificação de possível passagem de vetor vazio ---------- #
        
        if y_real is None:
            raise ValueError("Os dados reais não podem ser um vetor vazio.")
        
        # ---------- Cálculo ----------#
        
        # Retorna o erro quadrado médio
        MSE = np.mean(((y_real - self.y_predito) ** 2))
                               
        return MSE
      
    def raiz_quadrada_erro_quadrado_medio(self, y_real):
        
        """
        Calcula a raiz do erro quadrado médio (RMSE).
        
        Parâmetros:
        
        y_real (numpy.ndarray): Vetor dos valores reais.
        
        """

        # ---------- Verificação de possível passagem de vetor vazio ---------- #
        
        if y_real is None:
            raise ValueError("Os dados reais não podem ser um vetor vazio.")
        
        # ---------- Cálculo ----------#
        
        # Retorna a raiz do erro quadrado médio
        RMSE = np.sqrt(np.mean(((y_real - self.y_predito) ** 2)))
        
        return RMSE
                        
    def r_quadrado(self, y_real):
        
        """
        Calcula o coeficiente de determinação (R²).
        
        Parâmetros:
        
        y_real (numpy.ndarray): Vetor dos valores reais.
        
        """
        
        # ---------- Verificação de possível passagem de vetor vazio ---------- #
        
        if y_real is None:
            raise ValueError("Os dados reais não podem ser um vetor vazio.")
        
        # ---------- Cálculo ---------- #
        
        # Calcula o R quadrado
        R2 = 1 - (np.sum((y_real - self.y_predito)**2) / np.sum((y_real - np.mean(y_real))**2))
        
        return R2
    
    def r_quadrado_ajustado(self, y_real, num_preditores):
        
        """
        Calcula o coeficiente de determinação ajustado (R² ajustado).
        
        Parâmetros:
        
        y_real (numpy.ndarray): Vetor dos valores reais.
        num_preditores (int): O número de variáveis preditoras
        
        """

        # ---------- Verificação de possível passagem de vetor vazio ---------- #
        
        if y_real is None:
            raise ValueError("Os dados reais não podem ser um vetor vazio.")
            
        if num_preditores is None:
            raise ValueError("É preciso informar o número de variáveis preditoras passadas para o modelo.")
        
        # ---------- Cálculo ----------#
        
        # Determinando o número de preditores
        self.preditores = num_preditores
        
        # Determinando o tamanho do vetor de valores reais
        self.num_observacoes = len(y_real)
        
        # Calculando o R quadrado
        R2 = self.r_quadrado(y_real)
        
        # Calculando o R quadrado ajustado
        R2_ajustado = 1 - (((1 - R2) * (self.num_observacoes - 1))/(self.num_observacoes - self.preditores - 1))
        
        return R2_ajustado
