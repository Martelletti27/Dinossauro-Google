from dino_ai.game.dino import CHAO
TIPO_ESPINHO = 6
LARGURA_ESPINHO = 810
ALTURA_ESPINHO = 31
Y_ESPINHO = 10

# Classe Obstaculo
class Obstaculo:
    def __init__(self, x:int, largura:int, altura:int, tipo:int):
        self.x = x
        self.y = CHAO
        self.largura = largura
        self.altura = altura
        self.tipo = tipo
    
    def mover(self, velocidade:int):
        self.x = self.x + velocidade
