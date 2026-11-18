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
original/             Código C/C++ original (gabarito do port)
assets/               Sprites, redes treinadas do original, material de estudo
.cursor/              Regras e subagentes do modo ensino e da auditoria contra o C
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

O simulador ainda é **mais simples** que o jogo completo do Chrome:

- No respawn, sorteia **três obstáculos**: cacto baixo (20×40), cacto alto (30×70) ou **pássaro** (30×25, a 30 acima do chão), com `x` entre 350 e 550.
- O dino usa **pular** e **abaixar**; a terceira saída (avião) existe no DNA mas ainda não é lida.
- Fitness por frame (vivo): **+2** no chão (em pé/abaixado), **+1** pulando.
- Velocidade do mundo começa em **-3** e acelera **0,0005 por frame** até o teto de **8** (igual ao original).

Os experimentos 1–3 usavam **um único tamanho** de cacto; o 4 introduziu o segundo tamanho; o 5 introduziu o pássaro e o abaixar; o 6 aplicou quatro ajustes no simulador após o colapso do 174.

Fitness alto = “sobreviveu muito tempo neste loop de obstáculos”, **não** domínio do jogo completo.

### Roteiro de experimentos (um de cada vez)

1. ~~População / gerações~~ (feito)
2. ~~`MAX_PASSOS`~~ (feito)
3. ~~Respawn com distância aleatória~~ (feito)
4. ~~Dois tamanhos de cacto no chão~~ (feito)
5. ~~Pássaro / obstáculos no ar + abaixar~~ (feito — colapso em 174; causa era divergência do C)
6. ~~Ajustes pós-174 (ordem, queda, colisão, aceleração, mutação variável + decaimento)~~ (feito)
7. Terceira saída (avião) e, depois, interface (Pygame)

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

#### 5) Pássaro no ar + ação de abaixar

Setup: pop 30 × 20 gerações, `MAX_PASSOS = 3000`, respawn `x` 350–550.  
Mudança: no respawn entra um terceiro sorteio, o **pássaro** (30×25 a `CHAO + 30`), a saída 2 da rede passa a acionar `abaixar`, e a caixa de colisão do dino encolhe de 40 para 20 de altura quando ele está abaixado.

| Cenário | Melhor ger. 0 | Final (ger. 19) |
|---------|---------------|-----------------|
| 2 cactos, só pulo | ~4100 | ~4192 |
| + pássaro e abaixar | **174** | **174** |

**Leitura:** colapso total, e o valor `174` denunciou a causa. Ele não é aleatório: o dino nasce em `x = 100` com 40 de largura, o obstáculo começa em `x = 400` e anda 3 por frame, então o encontro acontece em `(400 - 140) / 3 ≈ 87` frames; parado no chão são `87 × 2 = 174` pontos. Ou seja, **a população inteira estava morrendo no primeiro cacto sem sair do chão**. Medindo a frequência das saídas, o abaixar ficava ativo em ~62% dos frames — e isso, somado à ordem errada das ações, anulava todo pulo. O próximo passo não foi mexer em hiperparâmetro: foram ajustes no simulador e no genético.

#### 6) Ajustes após o colapso do 174

Ajustes feitos **um de cada vez**. Medição: 8 treinos com sementes fixas (0 a 7), pop 30 × 20 gerações, `MAX_PASSOS = 3000`.

| # | Ajuste | Melhor fitness | Sementes que completam o episódio | Presos em 174 |
|---|--------|----------------|-----------------------------------|---------------|
| — | (antes dos ajustes; estado do exp. 5) | 174 | 0 de 8 | 8 de 8 |
| 1 | Ordem das ações no frame: `abaixar` antes de `pular` | 5135 | 6 de 8 | ~2 de 8 |
| 2 | Abaixar no ar também empurra o dino 2 para baixo | 5283 | 7 de 8 | ~1 de 8 |
| 3 | Colisão avaliada **antes** da decisão da rede | 4782 | 6 de 8 | ~2 de 8 |
| 4 | Velocidade do mundo acelera 0,0005/frame até 8 | 4622 | 4 de 8 | ~3 de 8 |
| 5 | Mutação com quantidade variável (1 até tamanho do DNA) | 4402 | 4 de 8 | 0 de 8 |
| 6 | Teto de mutação decai ×0,99 por geração (piso 20) | **4992** | **6 de 8** | **0 de 8** |

**Leitura:**

1. **Ordem das ações** — bug fatal. Com `pular` antes de `abaixar`, o impulso era criado e apagado no mesmo frame. Invertendo a ordem, o pulo volta a funcionar. Fitness saltou de 174 para a casa dos 4000–5000.
2. **Queda rápida** — além de frear a subida, abaixar no ar agora também empurra o dino 2 para baixo. Permite abortar um pulo mal calculado. Ganho pequeno e consistente.
3. **Momento da colisão** — a colisão passa a ser checada antes da decisão da rede, então a agachada só vale a partir do frame seguinte. **O fitness caiu de propósito** (5283 → 4782): o jogo ficou mais exigente, não pior.
4. **Aceleração do mundo** — a velocidade deixa de ser fixa em -3: aos 3000 passos chega a **-4,5** (ainda longe do teto 8). O quinto sensor passa a variar. Melhor fitness 4782 → 4622, sementes que completam 6/8 → 4/8. Queda esperada — o cenário aperta com o tempo.
5. **Mutação variável** — em vez de trocar sempre 5 pesos, cada filho muda um número sorteado entre 1 e o tamanho do DNA (~70). Isso ataca a armadilha do 174: mesmo quando a geração 0 só tem dino parado, as mutações maiores conseguem achar um pulador. **Presos em 174: 3/8 → 0/8.**
6. **Decaimento do teto** — o máximo de mutações começa em 70 e cai 1% por geração (piso 20). Em 20 gerações o teto vai a ~57: ainda alto, mas a tendência é explorar mais no começo e afinar depois. Completam o episódio 4/8 → **6/8**; melhor fitness **4992**; presos em 174 continuam **0/8**.

**Pendências que sobraram depois deste passo:**

- **Terceira saída sem uso.** `QTD_OUTPUT = 3`, mas o mundo só lê pular e abaixar. São genes que não afetam nada e diluem a mutação. Ou implementar o avião, ou reduzir para 2 saídas.
- **Divergências ainda abertas no genético (opcional):** população do original é 2000 (aqui 30); o C tem 3 tipos de operador de mutação (substituir / multiplicar / somar). Aqui só substituímos.
- **Divergências aceitas de propósito:** um único obstáculo reciclado; dino em `x` fixo (100); caixa de colisão com medidas fixas.

#### 7) Espinho + avião (saidas[2])

Setup: pop 30 × 20 gerações, `MAX_PASSOS = 3000` (igual aos experimentos 3–6).  
Mudança de cenário: gerador de espinhos a cada 10 obstáculos (`tipo` 6, 810×31, Y=10; commit `2b57133`), terceira saída da rede aciona o **avião** (`saidas[2]`), e testes novos em `dino_ai/tests/test_espinho_aviao.py` (constantes, contador a cada 10, 11º obstáculo = espinho).

| Momento | Melhor fitness |
|---------|----------------|
| Geração 0 | 811 |
| Pico no treino | **2080** (geração 10) |
| Final (geração 19) | 1827 |

**Leitura:**

- Não houve colapso em **174**: o melhor de cada geração ficou bem acima disso (o elite não ficou parado no primeiro cacto). Ainda aparecem indivíduos com 174/90 na população, mas o campeão evolui.
- O platô (~1800–2100) ficou **abaixo** do pós-174 do experimento 6 (~4000–5000): o espinho (faixa larga) e o cenário com avião apertam o episódio; sobreviver 3000 passos fica mais raro.
- Pico **2080** na geração 10; o final (1827) oscila em torno dessa faixa — típico de mutação em torno do elite sem “encher o cronômetro” como nos cactos simples.
- Tempo total de parede: **não registrado** no log do terminal (só saídas de fitness por indivíduo e `Geracao: … Melhor: …`).

## Progresso do port Python

- [x] Rede neural (`neural_network.py`) — forward pass completo
- [x] Carregar/extrair DNA (70 pesos)
- [x] Simulador headless (física, colisão, obstáculo em loop)
- [x] Sensores + decisão da rede no mundo
- [x] Algoritmo genético + loop de treino
- [x] Respawn com distância aleatória
- [x] Dois tamanhos de cacto no chão
- [x] Pássaro / obstáculos no ar + abaixar
- [x] Ordem das ações, queda rápida, momento da colisão e aceleração do mundo
- [x] Mutação com quantidade variável + decaimento do teto (armadilha do 174)
- [x] Avião (`saidas[2]`) + espinhos a cada 10 obstáculos
- [ ] Salvar/carregar o melhor DNA em arquivo
- [ ] Interface gráfica (Pygame)

## Créditos

- Projeto original: [JVictorDias/Dinossauro-Google](https://github.com/JVictorDias/Dinossauro-Google)
- [Vídeo demonstrativo do autor](https://www.youtube.com/watch?v=NZlIYr1slAk)

## Licença

Consulte o repositório original para informações de licenciamento.