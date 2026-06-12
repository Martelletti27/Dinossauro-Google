# importações
from dino_ai.neural_network import relu


# testes
assert relu(-5) == 0
assert relu(0) == 0
assert relu(3.7) == 3.7
assert relu(-0.001) == 0

print("Todos os testes de ReLU passaram")

