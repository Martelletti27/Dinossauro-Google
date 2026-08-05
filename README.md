# Dinossauro Google — Port Python

Fork e reimplementação em **Python** do projeto [Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google) de [Victor Dias](https://github.com/JVictorDias), onde redes neurais evoluem para aprender a jogar o jogo do dinossauro do Chrome.

Preview

## Sobre o projeto

Várias redes neurais competem em paralelo. As que sobrevivem mais tempo passam seus pesos (DNA) para a próxima geração, com mutações aleatórias — **algoritmo genético**, não backpropagation.

### Rede neural (MLP)


| Camada  | Tamanho              | Função                                                                  |
| ------- | -------------------- | ----------------------------------------------------------------------- |
| Entrada | 6 sensores + 1 bias  | distância, largura, Y e altura do obstáculo, velocidade, altura do dino |
| Oculta  | 6 neurônios + 1 bias | processamento intermediário                                             |
| Saída   | 3 neurônios          | pular, abaixar, avião                                                   |


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


| Parâmetro     | Valor |
| ------------- | ----- |
| `TAMANHO_POP` | 30    |
| `GERACOES`    | 20    |
| `MAX_PASSOS`  | 3000  |


### Setup atual do cenário (importante para ler os números)

O simulador ainda é **bem simples** frente ao jogo completo do Chrome:

- Obstáculos só no **chão** (sem pássaros ainda).
- No respawn, sorteia **dois tamanhos de cacto**: 20×40 ou 30×70, com `x` entre 350 e 550.
- O dino só usa de fato a saída de **pular** (abaixar/avião ainda não entram no jogo).
- Fitness por frame (vivo): **+2** no chão (em pé/abaixado), **+1** pulando.

Os experimentos 1–3 usavam **um único tamanho** de cacto; o experimento 4 introduziu o segundo tamanho.

Fitness alto = “sobreviveu muito tempo neste loop de cactos”, **não** domínio do jogo completo.

### Roteiro de experimentos (um de cada vez)

1. ~~População / gerações~~ (feito)
2. ~~`MAX_PASSOS`~~ (feito)
3. ~~Respawn com distância aleatória~~ (feito)
4. ~~Dois tamanhos de cacto no chão~~ (feito)
5. **Pássaro / obstáculos no ar** (próximo) — aí abaixar passa a importar
6. Mais variedade + ações (avião) e, depois, interface (Pygame)

### Experimentos e análise (hiperparâmetros)

Mudanças feitas **uma de cada vez** para isolar o efeito.

#### 1) População e gerações

Setup: **1 cacto**, respawn fixo `x = 400`, `MAX_PASSOS = 500`, só pulo.

| Setup | Melhor fitness típico |
|-------|------------------------|
| Pop 5 × 3 gerações | ~174 |
| Pop 30 × 20 gerações | ~698 (já na geração 0; estável depois) |

**Leitura:** mais candidatos ajudam a achar um DNA que passa vários ciclos do mesmo cacto. Depois o elite se mantém e as mutações raramente o superam.

#### 2) Limite de passos do episódio

Setup: **1 cacto**, respawn fixo `x = 400`, pop 30 × 20 gerações, só pulo.

| `MAX_PASSOS` | Melhor estável | Teto teórico (sempre no chão, +2/frame) | Melhor ÷ passos |
|--------------|----------------|----------------------------------------|-----------------|
| 500 | ~698 | 1000 | ~1,40 |
| 1500 | ~1985 | 3000 | ~1,32 |
| 3000 | **~3900** | 6000 | **~1,30** |

**Leitura:**

- Subir `MAX_PASSOS` aumenta o fitness na mesma proporção aproximada: o bom DNA **enche o cronômetro**.
- Fica abaixo do teto teórico por causa dos frames de pulo (+1).
- O genético acha o patamar cedo (geração 0–2) e estabiliza.
- Só alongar o episódio traz pouca informação nova sobre generalização.

#### 3) Respawn com distância aleatória

Setup: **1 cacto**, pop 30 × 20 gerações, `MAX_PASSOS = 3000`, só pulo.  
Única mudança: ao sair da tela, `x = random(350..550)` em vez de `400` fixo.

| Respawn | Melhor ger. 0 | Pico no treino | Comportamento |
|---------|---------------|----------------|---------------|
| Fixo `x = 400` | ~3900 | ~3900 | Platô duro; muitos indivíduos iguais |
| Aleatório 350–550 | ~4155 | **~4300** (ger. 18) | Oscila ~4100–4300; sobe um pouco ao longo das gerações |

**Leitura:**

- A rede **não quebrou** com espaçamento variável: ainda encontra DNAs que sobrevivem o episódio inteiro.
- Fitness pode ficar **acima** de 3900 porque gaps maiores (até 550) dão mais tempo no chão (+2) e menos pressão de pulo.
- Há **mais variação** entre indivíduos (menos “todo mundo 3900”) e um pouco mais de evolução geracional.
- Continua sendo só **1 tipo de cacto**; o próximo passo foi variar o **tamanho** (experimento 4).

#### 4) Dois tamanhos de cacto no chão

Setup: pop 30 × 20 gerações, `MAX_PASSOS = 3000`, respawn `x` 350–550, só pulo.  
Única mudança: no respawn, sorteia cacto **baixo** (20×40) ou **alto** (30×70).

| Cenário | Melhor ger. 0 | Pico | Final (ger. 19) |
|---------|---------------|------|-----------------|
| 1 tamanho + x aleatório | ~4155 | ~4300 | ~4177 |
| 2 tamanhos + x aleatório | ~4100 | **~4276** | ~4192 |

**Leitura:**

- A rede **ainda** encontra DNAs que enchem o episódio (~4200); o segundo tamanho não derrubou o treino.
- Impacto no platô dos campeões foi **leve** (faixa parecida com o experimento 3).
- Aparecem mais fitness intermediários na população (falha no cacto alto ou no timing) — cenário um pouco mais exigente sem mudar o teto dos melhores.
- Próximo salto de dificuldade útil: **pássaro** (Y no ar), onde abaixar passa a importar.

## Progresso do port Python

- [x] Rede neural (`neural_network.py`) — forward pass completo
- [x] Carregar/extrair DNA (70 pesos)
- [x] Simulador headless (física, colisão, obstáculo em loop)
- [x] Sensores + decisão da rede no mundo
- [x] Algoritmo genético + loop de treino
- [x] Respawn com distância aleatória
- [x] Dois tamanhos de cacto no chão
- [ ] Pássaro / obstáculos no ar + abaixar
- [ ] Interface gráfica (Pygame)

## Créditos

- Projeto original: [JVictorDias/Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google)
- [Vídeo demonstrativo do autor](https://www.youtube.com/watch?v=NZlIYr1slAk)

## Licença

Consulte o repositório original para informações de licenciamento.