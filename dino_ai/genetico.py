from dino_ai.config import PESO_MAX, PESO_MIN
import random

# acha qual o melhor dino em uma lista pelo maior fitness

def melhor_individuo(lista_de_dinos):
    melhor = lista_de_dinos[0]
    for dino in lista_de_dinos:
        if dino.fitness > melhor.fitness:
            melhor = dino
    return melhor

def mutar_dna(dna) -> list:
    novo = dna.copy()
    for x in range(5):
        posicao = random.randint(0,len(dna)-1)
        novo[posicao] = random.randint(PESO_MIN, PESO_MAX)

    return novo

def proxima_geracao(dna_campeao, tamanho_populacao) -> list:
    nova_pop = []
    nova_pop.append(dna_campeao.copy())
    while len(nova_pop) < tamanho_populacao:
        filho = mutar_dna(dna_campeao)
        nova_pop.append(filho)
    return nova_pop