class Knn:

    """Executa o algoritmo de classificação k-nearest neighbors algorithm (KNN)
    """
    
    def __init__(self, k_class, data_trein, data_test):
        
        """Construtor para a classe Knn
  
        Parâmetros:
           k_class (int): Número que representa os K vizinhos mais próximos
           data_trein (list): Lista com os dados de treinamento que seguem o seguinte padrão 
           [CPF: INT, Perfil Do Investidor: STRING, Carteira de Investimento: TUPLA]           
           data_test (list): Lista com os dados de teste que seguem o seguinte padrão 
           [CPF: INT, Perfil Do Investidor: STRING, Carteira de Investimento: TUPLA]
        """
            
        self.k_class = k_class
        self.data_trein = data_trein
        self.data_test = data_test
        # O dicionário abaixo armazena o resultado
        self.dict_result = {}
        
    def euclidean_distance(self, vetor1, vetor2):
        
        """Calcula a distância euclidiana entre dois vetores passados como parâmetro
  
        Parâmetros:
           vetor1 (list): Vetor que representa um elemento de teste
           vetor2 (list): Vetor que representa um elemento de treinamento
        """

        return ( sum( [ (v1-v2)**2 for v1,v2 in zip(vetor1,vetor2) ])**(1/2) )
    
    def calculate_distances(self):
        
        """Calcula a distância euclidiana de cada elemento de teste para todos os elementos de treinamento
        """
        
        # Calculando as distâncias de cada elemento de teste para todos os elementos de treinamento
        for teste in self.data_test:   
            cpf = teste[0]
            # O dicionário abaixo é a estrutura que armazena o resultado de todos os cálculos de interesse do KNN
            self.dict_result[cpf] = {
                # Armazena a distância de cada elemento de teste para todos os elementos de treinamento
                'classes_e_distancias' : [], 
                # Armazena as K menor distância entre o elemento de teste e todos de treinamento
                'classes_e_distancias_k_menores' : [], 
                # Armazena a frequência das classes mais próximas
                'frequencia_por_classe' : [], 
                # Armazena a informação da classe mais próxima
                'classe_mais_proxima' : '' 
            }        
            # Calcula a distância do elemento de teste para todos os elementos de treinamento
            for trein in self.data_trein:        
                distancia = self.euclidean_distance( teste[2],trein[2] )
                self.dict_result[cpf]['classes_e_distancias'].append( (trein[1] , distancia) )        
                
   
    def order_distances(self, cpf):
        
        """Ordena as distâncias do cpf de teste passado como parâmetro para cada elemento de treinamento

        Parameters:
            cpf (int): CPF de teste
        """
        
        # captura a distância euclidiana do cpf de teste passado como parâmetro para cada elemento de treinamento
        tuplas_cpf = self.dict_result[cpf]['classes_e_distancias']
        # Ordena as distâncias em ordem crescente
        self.dict_result[cpf]['classes_e_distancias'] = sorted( tuplas_cpf , key=lambda tup: tup[1])
    
    def calculate_nearest_class(self, cpf):

        """Identifica dentre as K classes mais próximas do CPF de teste passado como parâmetro aquela que 
        tem a maior frequência e classifica esse CPF de teste com esse rótulo de maior frequência

        Parameters:
            cpf (int): CPF de teste
        """
        
        # Capturando as K vizinhos mais próximos
        self.dict_result[cpf]['classes_e_distancias_k_menores'] = self.dict_result[cpf]['classes_e_distancias'][0:self.k_class]  
        # Frequência das classes dos K elementos mais próximos 
        listaClass = [item[0] for item in self.dict_result[cpf]['classes_e_distancias_k_menores']]
        self.dict_result[cpf]['frequencia_por_classe'] = [ ( item, listaClass.count(item)) for item in set(listaClass) ]
        # Cálculo da MODA das classes dos k vizinhos mais próximos.
        self.dict_result[cpf]['classe_mais_proxima'] = max( self.dict_result[cpf]['frequencia_por_classe'] ,key=lambda item:item[1])[0]
    
    def print_result(self, detalhamento = False):
        
        """Imprime a classificação de cada CPF de teste
        
        Parameters:
             detalhamento (bool): informa de deve mostrar a frequência das K classes mais próximas. True indica que sim , e False indica que não. Por padrão o detalhamento não é mostrado.
        """

        # Visualizando as classificações obtidas com os elementos de teste
        # Se quiser mostrar a frequência das K classes mais próximas, basta mudar a  
        # variável 'mostrar_frequencia_classes_proximas' para True
        mostrar_frequencia_classes_proximas = detalhamento 
        todas_linhas = []
        
        if mostrar_frequencia_classes_proximas:
            column_names = ['CPF de Teste','Classificação (Rótulo)','Frequência das Classes mais próximas (K={})'.format(self.k_class)]
            print(column_names)
            for res in self.data_test:
                print(  [ res[0] , self.dict_result[res[0]]['classe_mais_proxima'] , self.dict_result[res[0]]['frequencia_por_classe'] ] )
        else:
            column_names = ['CPF de Teste','Classificação (Rótulo)']
            print(column_names)
            for res in self.data_test:
                print(  [ res[0] , self.dict_result[res[0]]['classe_mais_proxima'] ] )
        
    def run(self):
        
        """Executa o algoritmo principal do KNN
        """        
        # Calcula a distância de cada CPF de teste para todos CPF's de treinamento
        self.calculate_distances()
        # Iterando sobre cada CPF de teste para ordenar as distâncias para os elementos de treinamento
        # identificando os K vizinhos mais próximos
        for cpf in self.dict_result.keys():       
            # Ordenar distâncias
            self.order_distances(cpf)
            # Calcular clase mais próxima
            self.calculate_nearest_class(cpf)        
                
    def __repr__(self):
        
        """Mètodo mágico que imprime a configuração do algoritmo KNN
        """
                
        algoritmo = '\nAlgoritmo: k-nearest neighbors algorithm (KNN)'
        classe = '\nParâmetro K: ' + str(self.k_class)
        qtd_trein = '\nQuantidade de dados de treinamento: {}'.format(len(self.data_trein))
        qtd_test = '\nQuantidade de dados de teste: {}'.format(len(self.data_test))
        lista_classes = [item[1] for item in self.data_trein]
        set_classes = set(lista_classes)
        classes_rotulos = '\nClasses/Rótulos identificados no conjunto de treinamento: {}'.format(set_classes)
        return  algoritmo + classe + qtd_trein + qtd_test + classes_rotulos +'\n'