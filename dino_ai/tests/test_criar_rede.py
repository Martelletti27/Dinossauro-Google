from dino_ai.neural_network import criar_rede, quantidade_pesos

rede = criar_rede(1, 6, 6, 3)

# 1. DNA tem 70 pesos
assert quantidade_pesos(rede) == 70

# 2. Entrada tem 7 neurônios (6 + bias)
assert len(rede.camada_entrada) == 7

# 3. Escondida tem 7 neurônios
assert len(rede.camadas_escondidas[0].neuronios) == 7

# 4. Saída tem 3 neurônios
assert len(rede.camada_saida.neuronios) == 3

# 5. Cada neurônio da escondida tem 7 pesos
for neuronio in rede.camadas_escondidas[0].neuronios:
    assert len(neuronio.pesos) == 7

# 6. Cada neurônio de saída tem 7 pesos
for neuronio in rede.camada_saida.neuronios:
    assert len(neuronio.pesos) == 7

print("Todos os testes de criar_rede passaram!")