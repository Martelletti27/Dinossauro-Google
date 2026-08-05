# Dinossauro Google — Port Python

Fork e reimplementação em **Python** do projeto [Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google) de [Victor Dias](https://github.com/JVictorDias), onde redes neurais evoluem para aprender a jogar o jogo do dinossauro do Chrome.

![Preview](original/preview.gif)

## Sobre o projeto

Várias redes neurais competem em paralelo. As que sobrevivem mais tempo passam seus pesos (DNA) para a próxima geração, com mutações aleatórias — **algoritmo genético**, não backpropagation.

### Rede neural (MLP)

| Camada | Tamanho | Função |
|--------|---------|--------|
| Entrada | 6 sensores + 1 bias | distância, largura, Y e altura do obstáculo, velocidade, altura do dino |
| Oculta | 6 neurônios + 1 bias | processamento intermediário |
| Saída | 3 neurônios | pular, abaixar, avião |

- Ativação: **ReLU**
- DNA: **70 pesos** por indivíduo

## Estrutura do repositório

```text
dino_ai/
  neural_network.py   Rede MLP + DNA
  genetico.py         Seleção, mutação, próxima geração
  treino.py           Loop de evolução
  game/               Simulador headless (dino, obstáculo, colisão, mundo, sensores)
  tests/              Testes da rede, mundo e genético
original/             Código C/C++ original (referência)
assets/               Sprites, redes treinadas do original, material de estudo
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
python -m dino_ai.tests.test_mundo
python -m dino_ai.tests.test_genetico
```

## Treino

```bash
python -m dino_ai.treino
```

Configuração atual em `dino_ai/treino.py`:

| Parâmetro | Valor |
|-----------|-------|
| `TAMANHO_POP` | 30 |
| `GERACOES` | 20 |
| `MAX_PASSOS` | 3000 |

### Setup atual do cenário (importante para ler os números)

Os experimentos abaixo usam um cenário **ainda bem simples**:

- **Um único tipo de obstáculo** — o equivalente a um **cacto** no chão (mesma largura/altura; sem pássaros, sem grupos de cactos).
- Esse obstáculo **reaparece** quando sai pela esquerda (esteira), mas sempre com **a mesma distância de respawn** (`x = 400` fixo).
- O dino só usa de fato a saída de **pular** (abaixar/avião ainda não entram no jogo).
- Fitness por frame (vivo): **+2** no chão (em pé/abaixado), **+1** pulando.

Ou seja: os fitness altos mostram “sobreviveu muito tempo neste cacto em loop com espaçamento fixo”, **não** ainda domínio do jogo completo do Chrome.

### Roteiro de experimentos (um de cada vez)

Ordem pensada para medir impacto limpo:

1. ~~População / gerações~~ (feito)
2. ~~`MAX_PASSOS`~~ (feito)
3. **Respawn com distância aleatória** (próximo) — evita decorar o timing de `x = 400`
4. **Outros obstáculos** — alturas/larguras diferentes, pássaros, etc.
5. Ações que faltam (abaixar, avião) e, depois, interface (Pygame)

### Experimentos e análise (hiperparâmetros)

Mudanças feitas **uma de cada vez** para isolar o efeito.  
Setup de cenário comum a estes testes: **1 cacto em loop**, respawn fixo, só pulo.

#### 1) População e gerações (com `MAX_PASSOS = 500`)

| Setup | Melhor fitness típico |
|-------|------------------------|
| Pop 5 × 3 gerações | ~174 |
| Pop 30 × 20 gerações | ~698 (já na geração 0; estável depois) |

**Leitura:** mais candidatos ajudam a achar um DNA que passa vários “ciclos” do mesmo cacto. Depois disso o elite se mantém e as mutações raramente o superam.

#### 2) Limite de passos do episódio (pop 30 × 20 gerações)

| `MAX_PASSOS` | Melhor estável | Teto teórico (sempre no chão, +2/frame) | Melhor ÷ passos |
|--------------|----------------|----------------------------------------|-----------------|
| 500 | ~698 | 1000 | ~1,40 |
| 1500 | ~1985 | 3000 | ~1,32 |
| 3000 | **~3900** | 6000 | **~1,30** |

**Leitura:**

- Subir `MAX_PASSOS` **aumenta** o fitness na mesma proporção aproximada: o bom DNA **enche o cronômetro** (sobrevive até o fim do episódio neste cenário de 1 cacto).
- O valor fica abaixo do teto teórico porque há frames de pulo (fitness +1 em vez de +2).
- O genético encontra esse patamar cedo (muitas vezes na geração 0–2) e estabiliza.
- Continuar só aumentando `MAX_PASSOS` alonga a mesma prova; o próximo experimento útil é **respawn aleatório**, depois **outros tipos de obstáculo**.

## Progresso do port Python

- [x] Rede neural (`neural_network.py`) — forward pass completo
- [x] Carregar/extrair DNA (70 pesos)
- [x] Simulador headless (física, colisão, obstáculo em loop)
- [x] Sensores + decisão da rede no mundo
- [x] Algoritmo genético + loop de treino
- [ ] Distância de respawn aleatória / cenários mais ricos
- [ ] Interface gráfica (Pygame)

## Créditos

- Projeto original: [JVictorDias/Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google)
- [Vídeo demonstrativo do autor](https://www.youtube.com/watch?v=NZlIYr1slAk)

## Licença

Consulte o repositório original para informações de licenciamento.
