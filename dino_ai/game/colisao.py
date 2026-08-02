
#funcao de colisao
def colisao(dino, obstaculo) -> bool:
    dino_largura = 40
    dino_altura = 40

    if (dino.x + dino_largura) <= obstaculo.x:           # dino esta totalmente a esquerda do obstaculo?
        return False
    if dino.x >= (obstaculo.x + obstaculo.largura):      # dino esta totalmente a direita do obstaculo?
        return False
    if (dino.y + dino_altura) <= obstaculo.y:            # dino esta totalmente abaixo do obstaculo?
        return False    
    if dino.y >= (obstaculo.y + obstaculo.altura):       # dino esta totalmente a acima do obstaculo?
        return False
    return True