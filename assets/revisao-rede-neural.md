# Revisão: rede neural + algoritmo genético

Documento de estudo baseado nas perguntas e respostas do port Python do Dinossauro Google.  
Planilha de simulação do cálculo: [`Simulacao Rede Neural.xlsx`](./Simulacao%20Rede%20Neural.xlsx)

---

## O que já está pronto no código

- Rede neural em `dino_ai/neural_network.py` + constantes em `dino_ai/config.py`
- Arquitetura: **6+1 → 6+1 → 3** (70 pesos)
- Funções: ReLU, criar rede, forward pass, DNA ida/volta
- Testes: `test_relu`, `test_criar_rede`, `test_dna`
- Ainda **não** existe: simulador do jogo, genético, Pygame

---

## Arquitetura da rede

| Camada | Quantidade | Papel |
|--------|------------|--------|
| Entrada | 6 sensores + 1 bias | Recebe dados do jogo |
| Oculta (hidden) | 6 neurônios + 1 bias | Processa |
| Saída | 3 neurônios | Decide ações |

- Ativação: **ReLU** (negativo → 0; senão mantém o valor)
- Pesos aleatórios iniciais: **-1000 a 999**
- DNA = lista com os **70 pesos** (oculta + saída; entrada não tem pesos)

### Contagem dos 70 pesos

- Oculta: 7 neurônios × 7 pesos = **49**
- Saída: 3 neurônios × 7 pesos = **21**
- Total = **70**

---

## Os 6 inputs (sensores)

Vêm do **estado do jogo** a cada frame (~0,005 s no original), não de um arquivo externo.

| Índice | Sensor | Significado simples |
|--------|--------|---------------------|
| 0 | Distância até o próximo obstáculo | Quão longe está o perigo |
| 1 | Largura do obstáculo | Quão “gordo” ele é |
| 2 | Altura (Y) do obstáculo | Em que altura ele está |
| 3 | Comprimento (altura do sprite) | Quão alto é o desenho |
| 4 | Velocidade (`\|VELOCIDADE\|`) | Quão rápido o mundo está |
| 5 | Altura Y do dinossauro | Em que altura o dino está |

- O **7º** valor da entrada é o **bias = 1,0** (fixo; não é sensor).
- No jogo real, esses sensores tendem a ser **≥ 0**. Quem pode ser negativo são os **pesos**.

---

## As 3 saídas

| Índice | Ação |
|--------|------|
| 0 | Pular |
| 1 | Abaixar |
| 2 | Avião |

Regra no original: valor **0** → não faz; valor **≠ 0** → faz a ação.

### E se duas saídas forem positivas ao mesmo tempo?

A rede **não escolhe só uma**. O código do jogo aplica as ações na ordem dele.

- No **chão**, se pular e abaixar vêm juntos: o **pulo tende a ganhar** (sobrescreve).
- No **ar**, pular de novo é ignorado; abaixar pode cortar a subida.
- Não é “só o maior vence” (argmax).

---

## Bias: quem liga em quem

- **Bias da entrada** → liga nos **6** neurônios da oculta que calculam.
- **Nada** (no forward pass) liga **no** bias da oculta; ele só fica em **1,0**.
- **Bias da oculta** → liga nas **3** saídas.

Os pesos ficam no neurônio que **recebe** (oculta/saída). Entrada só guarda o valor do sensor.

---

## O cálculo (forward pass)

### 1) Preencher a entrada

Coloca os 6 sensores + bias. O neurônio de distância **só guarda** o número; o cérebro só “pensa” quando o formulário está completo.

### 2) Cada neurônio da oculta (os 6 que calculam)

```text
somatorio = e0*p0 + e1*p1 + e2*p2 + e3*p3 + e4*p4 + e5*p5 + bias*p6
saida = relu(somatorio)
```

### 3) Cada neurônio de saída

Mesma ideia, usando as **7 saídas da oculta** (6 calculadas + bias = 1) × pesos daquele neurônio de saída → ReLU.

Fluxo:

```text
sensores (6) + bias
        ↓
   oculta (6) + bias     ← ReLU
        ↓
   saídas (3)            ← ReLU  → pular / abaixar / avião
```

A planilha Excel simula exatamente essa conta com números de exemplo.

---

## Frequência: de quanto em quanto tempo?

A cada **passo do jogo** (frame). No original, `Periodo ≈ 0,005 s` → cerca de **200 vezes por segundo**.

Ordem típica no frame: mover mundo → gravidade/colisões → ler sensores → `calcular_saida` → aplicar ação.

---

## Lógica do treino (algoritmo genético)

1. Cria **população** de redes com DNA aleatório (6+1 → 6+1 → 3).
2. Todas jogam (em paralelo no original).
3. A cada frame: jogo gera sensores → rede decide → dino age.
4. Fitness sobe enquanto o dino está vivo (no original: pontos por frame, não “metros” literais — mas correlaciona com ir longe).
5. Quando todos morrem:
   - ordena por fitness;
   - o **melhor fica intacto** (elite = exploitation);
   - os outros **recebem cópia** do DNA do melhor;
   - os clones sofrem **mutação** (exploration): trocar peso, multiplicar ou somar um pouco.
6. Nova geração → repete.

### Exploitation vs exploration

| Conceito | No projeto |
|----------|-------------|
| Exploitation | Manter o melhor sem mudar |
| Exploration | Mutar os clones |

No original, a quantidade de mutações tende a **diminuir** com as gerações (explora menos depois).

### “Pesos ideais e joga pra sempre?”

Não. Chega em pesos **bons o bastante**, sem garantia matemática de perfeição eterna. Pode falhar em situações novas.

---

## Fluxo mental (quando o jogo existir)

1. Jogo gera sensores → `copiar_para_entrada`
2. `calcular_saida`
3. `copiar_da_saida` → decide ação
4. Ao morrer → `extrair_vetor_das_camadas` (DNA)
5. Genético muta DNA → `copiar_vetor_para_camadas` na próxima geração

Hoje os passos 2–5 (cérebro + DNA) já existem no Python; falta o mundo do jogo em volta.

---

## Próximo passo do port

Simulador headless em etapas (aluno digita; agente orienta e revisa):

1. Dino (posição, pulo, gravidade)
2. Obstáculos + colisão
3. Sensores (6 inputs)
4. Loop do mundo + testes
5. Depois: genético e Pygame
