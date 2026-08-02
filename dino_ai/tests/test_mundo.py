from dino_ai.game.mundo import Mundo
from dino_ai.game.dino import MORTO

mundo = Mundo()

for x in range(200):
    mundo.passo()

assert mundo.dino.estado == MORTO
print("Teste mundo OK")





