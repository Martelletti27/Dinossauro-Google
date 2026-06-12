# importações
from dino_ai.config import BIAS, PESO_MIN, PESO_MAX
import random

# ReLU
def relu(x: float) -> float:
    if x < 0:
        return 0
    else:
        return x


# Classes
class Neuronio:
    def __init__(self, qtd_ligacoes: int):
        self.pesos = [random.randint(PESO_MIN, PESO_MAX) for x in range(qtd_ligacoes)]
        self.saida = 1.0

class Camada:
    def __init__(self, qtd_neuronios: int, qtd_ligacoes_por_neuronio: int):
        self.neuronios = [Neuronio(qtd_ligacoes_por_neuronio) for x in range(qtd_neuronios)]

class NeuronioEntrada:
    def __init__(self):
        self.saida = 1.0

class RedeNeural:
    def __init__(self, qtd_escondidas:int , qtd_input:int, qtd_hide:int, qtd_output:int):
        qtd_entrada_total = qtd_input + BIAS
        qtd_hide_total = qtd_hide + BIAS
        
        # entrada
        self.camada_entrada = [NeuronioEntrada() for x in range(qtd_entrada_total)]

        # escondidas
        self.camadas_escondidas = []
        for x in range(qtd_escondidas):
            if x == 0:
                ligacoes = qtd_entrada_total
            else:
                ligacoes = qtd_hide_total
            
            self.camadas_escondidas.append(
                Camada(qtd_hide_total, ligacoes)
            )
        
        self.camada_saida = Camada(qtd_output, qtd_hide_total)

def criar_rede(qtd_escondidas, qtd_input, qtd_hide, qtd_output):
    return RedeNeural(qtd_escondidas, qtd_input, qtd_hide, qtd_output)

def quantidade_pesos(rede: RedeNeural) -> int:
    total = 0

    for camada in rede.camadas_escondidas:
        for neuronio in camada.neuronios:
            total += len(neuronio.pesos)

    for neuronio in rede.camada_saida.neuronios:
        total += len(neuronio.pesos)

    return total

def copiar_para_entrada(rede: RedeNeural, sensores: list) -> None:
    for x in range(len(sensores)):
        rede.camada_entrada[x].saida = sensores[x]

def copiar_da_saida(rede: RedeNeural) -> list:
    saida = []
    for neuronio in rede.camada_saida.neuronios:
        saida.append(neuronio.saida)
    return saida

def calcular_saida(rede: RedeNeural) -> None:
    
    #parte A = Camada de Entrada para Primeira Camada Oculta
    camada_escondida = rede.camadas_escondidas[0]
    for i in range(len(camada_escondida.neuronios) - BIAS):
        somatorio = 0
        for j in range(len(rede.camada_entrada)):
            somatorio += rede.camada_entrada[j].saida * camada_escondida.neuronios[i].pesos[j]
        camada_escondida.neuronios[i].saida = relu(somatorio)

    #parte B = Camada oculta para Camada oculta quando for > 1 camada oculta
    for k in range(1, len(rede.camadas_escondidas)):
        camada_anterior = rede.camadas_escondidas[k - 1]
        camada_atual = rede.camadas_escondidas[k]
        for i in range(len(camada_atual.neuronios) - BIAS):
            somatorio = 0
            for j in range(len(camada_anterior.neuronios)):
                somatorio += camada_anterior.neuronios[j].saida * camada_atual.neuronios[i].pesos[j]
            camada_atual.neuronios[i].saida = relu(somatorio)


    #parte C = Ultima Camada Oculta para a Camada de Saida
    ultima_escondida  = rede.camadas_escondidas[-1]
    for i in range(len(rede.camada_saida.neuronios)):
        somatorio = 0
        for j in range(len(ultima_escondida.neuronios)):
            somatorio += ultima_escondida.neuronios[j].saida * rede.camada_saida.neuronios[i].pesos[j]
        rede.camada_saida.neuronios[i].saida = relu(somatorio)


def copiar_vetor_para_camadas(rede: RedeNeural, dna: list) -> None:
    j = 0
    
    # camadas escondidas
    for camada in rede.camadas_escondidas:
        for neuronio in camada.neuronios:
            for i in range(len(neuronio.pesos)):
                neuronio.pesos[i]=dna[j]
                j += 1
    
    #camada saida
    for neuronio in rede.camada_saida.neuronios:
        for i in range(len(neuronio.pesos)):
            neuronio.pesos[i]=dna[j]
            j += 1

def extrair_vetor_das_camadas(rede: RedeNeural) -> list:
    dna = []

    # camadas escondidas
    for camada in rede.camadas_escondidas:
        for neuronio in camada.neuronios:
            for i in range(len(neuronio.pesos)):
                dna.append(neuronio.pesos[i])

    # camada saida
    for neuronio in rede.camada_saida.neuronios:
        for i in range(len(neuronio.pesos)):
            dna.append(neuronio.pesos[i])

    return dna
