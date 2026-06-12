from dino_ai.neural_network import criar_rede, quantidade_pesos, copiar_vetor_para_camadas, extrair_vetor_das_camadas

rede = criar_rede(1, 6, 6, 3)

# DNA de teste com 70 números
dna = list(range(70))

copiar_vetor_para_camadas(rede, dna)
extraido = extrair_vetor_das_camadas(rede)

assert len(dna) == 70
assert len(extraido) == 70
assert extraido == dna
print("Teste DNA OK")