from dino_ai.game import obstaculo
from dino_ai.game.obstaculo import TIPO_ESPINHO, LARGURA_ESPINHO, ALTURA_ESPINHO, Y_ESPINHO
from dino_ai.game.dino import Dino, VOANDO, PULANDO, CHAO
from dino_ai.game.mundo import Mundo


def teste_constants_espinhos():
    assert LARGURA_ESPINHO == 810
    assert ALTURA_ESPINHO == 31
    assert Y_ESPINHO == 10
    assert obstaculo.TIPO_ESPINHO == TIPO_ESPINHO

def teste_contador_espinhos():
    mundo = Mundo()
    for i in range(10):
        mundo.obstaculo.x = -1000
        mundo.passo()
    assert mundo.contador_espinhos == 10


def teste_decimo_primeiro_obstaculo():
    mundo = Mundo()
    for i in range(11):
        mundo.obstaculo.x = -1000
        mundo.passo()
    assert mundo.obstaculo.tipo == TIPO_ESPINHO


teste_constants_espinhos()
teste_contador_espinhos()
teste_decimo_primeiro_obstaculo()

print("Teste espinhos ok")