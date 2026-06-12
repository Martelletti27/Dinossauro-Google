# Dinossauro Google — Port Python

Fork e reimplementação em **Python** do projeto [Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google) de [Victor Dias](https://github.com/JVictorDias), onde redes neurais evoluem para aprender a jogar o jogo do dinossauro do Chrome.

![Preview](original/preview.gif)

## Sobre o projeto

Várias redes neurais competem em paralelo. As que sobrevivem mais tempo passam seus pesos (DNA) para a próxima geração, com mutações aleatórias — **algoritmo genético**, não backpropagation.

### Rede neural (MLP)

| Camada | Tamanho | Função |
|--------|---------|--------|
| Entrada | 6 sensores + 1 bias | distância, largura, altura e tipo do obstáculo, velocidade, altura do dino |
| Oculta | 6 neurônios + 1 bias | processamento intermediário |
| Saída | 3 neurônios | pular, abaixar, avião |

- Ativação: **ReLU**
- DNA: **70 pesos** por indivíduo

## Estrutura do repositório

```text
dino_ai/          Port Python — rede neural e testes
original/         Código C/C++ original (referência)
assets/           Sprites, fontes, obstáculos e redes treinadas do projeto original
```

## Requisitos

- Python **3.10+**
- Por enquanto, apenas biblioteca padrão (sem dependências externas)
- Pygame será adicionado na etapa do simulador gráfico

## Instalação

```bash
git clone https://github.com/Martelletti27/Dinossauro-Google.git
cd Dinossauro-Google
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

## Testes

Execute na **raiz do repositório**:

```bash
python -m dino_ai.tests.test_relu
python -m dino_ai.tests.test_criar_rede
python -m dino_ai.tests.test_dna
```

## Progresso do port Python

- [x] Rede neural (`neural_network.py`) — forward pass completo
- [x] Carregar/extrair DNA (70 pesos)
- [ ] Simulador do jogo (física, colisão, obstáculos)
- [ ] Algoritmo genético (população e mutações)
- [ ] Interface gráfica (Pygame)

## Créditos

- Projeto original: [JVictorDias/Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google)
- [Vídeo demonstrativo do autor](https://www.youtube.com/watch?v=NZlIYr1slAk)

## Licença

Consulte o repositório original para informações de licenciamento.
