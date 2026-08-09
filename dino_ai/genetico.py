from dino_ai.config import PESO_MAX, PESO_MIN
import random


teto_mutacao = 70

# acha qual o melhor dino em uma lista pelo maior fitness

def melhor_individuo(lista_de_dinos):
    melhor = lista_de_dinos[0]
    for dino in lista_de_dinos:
        if dino.fitness > melhor.fitness:
            melhor = dino
    return melhor

def mutar_dna(dna) -> list:
    novo = dna.copy()
    mutacao = random.randint(1,int(teto_mutacao))
    for x in range(mutacao):
        posicao = random.randint(0,len(dna)-1)
        novo[posicao] = random.randint(PESO_MIN, PESO_MAX)

    return novo

def proxima_geracao(dna_campeao, tamanho_populacao) -> list:
    global teto_mutacao
    nova_pop = []
    nova_pop.append(dna_campeao.copy())
    while len(nova_pop) < tamanho_populacao:
        filho = mutar_dna(dna_campeao)
        nova_pop.append(filho)
    teto_mutacao = teto_mutacao * 0.99
    if teto_mutacao < 20:
        teto_mutacao = 20
    return nova_pop