from dino_ai.genetico import proxima_geracao

dna = list(range(70))
pop = proxima_geracao(dna, 10)

assert len(pop) == 10
assert pop[0] == dna
assert pop[1] != dna

print("Teste genetico ok")