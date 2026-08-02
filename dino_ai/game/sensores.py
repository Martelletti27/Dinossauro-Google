

def ler_sensores(dino, obstaculo, velocidade) -> list:
    return [
        obstaculo.x - dino.x,
        obstaculo.largura,
        obstaculo.y,
        obstaculo.altura,
        abs(velocidade),
        dino.y
    ]