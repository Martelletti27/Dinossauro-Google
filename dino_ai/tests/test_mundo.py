from dino_ai.game.mundo import Mundo
from dino_ai.game.dino import MORTO

mundo = Mundo()

for x in range(2000):
    mundo.passo()

assert (mundo.dino.estado == MORTO) or (mundo.dino.fitness > 400)

print("Teste mundo OK")





