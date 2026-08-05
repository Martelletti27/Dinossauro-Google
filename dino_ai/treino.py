import random
from dino_ai.config import PESO_MAX, PESO_MIN
from dino_ai.game.mundo import Mundo
from dino_ai.game.dino import MORTO
from dino_ai.genetico import proxima_geracao



TAMANHO_POP = 30
MAX_PASSOS = 3000
GERACOES = 20    
populacao = []


for x in range(TAMANHO_POP):
    dna = []
    for y in range(70):
        dna.append(random.randint(PESO_MIN, PESO_MAX))
    populacao.append(dna)

print(len(populacao))
print(len(populacao[0]))


for geracao in range(GERACOES):
    melhor_fitness = -1
    melhor_dna = None

    for dna in populacao:
        mundo = Mundo(dna=dna)
        for passo in range(MAX_PASSOS):
            if mundo.dino.estado == MORTO:
                break
            mundo.passo()
        print(mundo.dino.fitness)

        if mundo.dino.fitness > melhor_fitness:
            melhor_fitness = mundo.dino.fitness
            melhor_dna = dna

    print("Geracao:", geracao, "Melhor:", melhor_fitness)

    populacao = proxima_geracao(melhor_dna, TAMANHO_POP)
    