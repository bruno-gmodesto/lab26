# Documentação Teórica — Perceptron e MLP

> Material complementar ao notebook `perceptron_pytorch.ipynb`.
> Cobre os **Tópicos 1 a 4** (Sinapses, Soma Ponderada, Ativação e Predição) e
> os conceitos necessários para compreender o **Tópico 11** (MLP: Sigmoid vs Tanh).

---

## Avaliação dos Tópicos 1 a 4 do Notebook

Os quatro primeiros tópicos do notebook formam a *anatomia* de um neurônio artificial.
Eles são apresentados na ordem pedagógica correta: **estrutura → operação linear → operação não-linear → saída composta**. A avaliação de cada um:

| Tópico | O que o notebook apresenta | Avaliação |
|---|---|---|
| **1. Sinapses** | Mapeamento entrada/peso/bias como analogia biológica. | Correto. A analogia com "rodinha de volume" é fiel ao papel dos pesos. A observação de que o bias pode ser visto como um peso com entrada fixa em 1 é tecnicamente precisa. |
| **2. Soma Ponderada** | Produto escalar `z = wᵀx + b`. | Correto. A menção ao hiperplano separador está matematicamente correta: a equação `wᵀx + b = 0` define de fato um hiperplano no espaço de entrada. |
| **3. Ativação** | Step, Sigmoid, ReLU, Tanh com justificativa da não-linearidade. | Correto e completo para o escopo. A frase "sem ela, qualquer rede se reduziria a uma única transformação linear" é rigorosamente verdadeira. |
| **4. Predição** | Forward pass `ŷ = f(wᵀx + b)` e `nn.Linear` no PyTorch. | Correto. **Observação menor**: na fórmula LaTeX do tópico 4 há um somatório sem o termo `b` explícito (`∑ wᵢxᵢ +`) — a versão vetorial logo ao lado está certa. |

A transição tópicos 1→4 é coesa: cada um acrescenta exatamente uma peça do cálculo
`ŷ = f(wᵀx + b)`.

---

## 1. Sinapses — A Conexão Ponderada

### Origem biológica
Um neurônio biológico recebe estímulos de outros neurônios por meio de **sinapses**,
cuja força modula a contribuição de cada estímulo no potencial de ação pós-sináptico.
Essa abstração foi formalizada pela primeira vez por **McCulloch & Pitts (1943)**, que
propuseram o "neurônio lógico": uma unidade que integra entradas binárias ponderadas e
dispara quando a soma ultrapassa um limiar.

### Formalização matemática
Em um Perceptron com `n` entradas:

- Vetor de entradas: `x = (x₁, x₂, …, xₙ) ∈ ℝⁿ`
- Vetor de pesos: `w = (w₁, w₂, …, wₙ) ∈ ℝⁿ`
- Bias (intercepto): `b ∈ ℝ`

Cada componente `wᵢ` representa a **força sináptica** da conexão `i`. Pesos positivos são
excitatórios; pesos negativos são inibitórios — exatamente a distinção entre sinapses
glutamatérgicas e gabaérgicas no cérebro.

### O bias como peso auxiliar
É comum estender o vetor de entrada com uma componente fixa `x₀ = 1` para que o bias
apareça como mais um peso `w₀ = b`. Isso simplifica a notação:

```
ỹ = f(w̃ᵀx̃),  onde x̃ = [1, x₁, …, xₙ]ᵀ,  w̃ = [b, w₁, …, wₙ]ᵀ
```

### Fonte acadêmica
- McCulloch, W. S., & Pitts, W. (1943). *A logical calculus of the ideas immanent in nervous activity*. **Bulletin of Mathematical Biophysics**, 5(4), 115–133. https://doi.org/10.1007/BF02478259

---

## 2. Soma Ponderada — A Operação Linear

### Interpretação algébrica
A soma ponderada é o **produto interno** entre os vetores `w` e `x`, deslocado por `b`:

```
z = w · x + b = Σᵢ wᵢ xᵢ + b
```

### Interpretação geométrica
O conjunto de pontos que satisfaz `wᵀx + b = 0` é um **hiperplano** em `ℝⁿ`:
- Em 2D, uma reta.
- Em 3D, um plano.
- Em dimensão `n`, uma superfície `(n-1)`-dimensional.

`w` é o **vetor normal** ao hiperplano e `b / ||w||` é a distância (sinalizada) entre o
hiperplano e a origem. Para qualquer ponto `x`, o valor de `z` é proporcional à distância
assinada de `x` ao hiperplano, na direção de `w`. Isso explica por que o Perceptron é
um **classificador linear**: a decisão depende apenas de qual lado do hiperplano o ponto se encontra.

### Limitação fundamental
Como a soma ponderada é linear, um único Perceptron só pode separar classes que sejam
**linearmente separáveis**. Esse foi o resultado demonstrado por **Minsky & Papert (1969)**,
que provaram formalmente a impossibilidade de um Perceptron simples resolver o
XOR — motivação histórica para o surgimento das redes multicamadas.

### Fontes acadêmicas
- Rosenblatt, F. (1958). *The perceptron: A probabilistic model for information storage and organization in the brain*. **Psychological Review**, 65(6), 386–408. https://doi.org/10.1037/h0042519
- Minsky, M., & Papert, S. (1969). *Perceptrons: An Introduction to Computational Geometry*. MIT Press.

---

## 3. Função de Ativação — A Não-Linearidade

### Papel conceitual
A soma ponderada `z` é um escalar real contínuo. A função de ativação `f: ℝ → ℝ`
transforma esse valor em uma saída interpretável (probabilidade, classe, intensidade).
Mais importante, **f introduz não-linearidade** — sem ela, a composição de camadas se
colapsa em uma única transformação linear equivalente:

```
f(x) = Wx        ⇒    f₂(f₁(x)) = W₂ W₁ x = W' x   (continua linear)
```

### Funções clássicas (como no notebook)

| Função | Fórmula | Faixa | Diferenciável? | Característica |
|---|---|---|---|---|
| Degrau (Heaviside) | `1 se z ≥ 0, senão 0` | `{0, 1}` | Não (em z=0) | Perceptron original de Rosenblatt |
| Sigmoide logística | `σ(z) = 1 / (1 + e⁻ᶻ)` | `(0, 1)` | Sim | Classificação binária |
| Tangente hiperbólica | `tanh(z) = (eᶻ − e⁻ᶻ)/(eᶻ + e⁻ᶻ)` | `(−1, 1)` | Sim | Centrada em zero |
| ReLU | `max(0, z)` | `[0, ∞)` | Sim (a menos de z=0) | Padrão moderno em redes profundas |

### Derivadas (essenciais para o backpropagation)

```
σ'(z)    = σ(z) · (1 − σ(z))           ∈ (0, 0.25]
tanh'(z) = 1 − tanh²(z)                ∈ (0, 1]
ReLU'(z) = 1 se z > 0, 0 caso contrário
```

Note que a derivada máxima da sigmoide é **0.25**, enquanto a da tanh é **1.0**. Essa
diferença é a raiz prática do *vanishing gradient* comparativo entre as duas
(relevante para o Tópico 11).

### Universalidade
**Hornik, Stinchcombe & White (1989)** provaram o **Teorema da Aproximação Universal**:
uma rede com **uma única camada oculta** e uma função de ativação não-polinomial pode
aproximar qualquer função contínua em um compacto, com precisão arbitrária. O resultado
justifica teoricamente o uso de ativações suaves como sigmoide e tanh.

### Fonte acadêmica
- Hornik, K., Stinchcombe, M., & White, H. (1989). *Multilayer feedforward networks are universal approximators*. **Neural Networks**, 2(5), 359–366. https://doi.org/10.1016/0893-6080(89)90020-8

---

## 4. Predição (*Forward Pass*)

### Composição
A predição do Perceptron encadeia a parte linear e a não-linear:

```
ŷ = f(wᵀx + b)
```

### Em PyTorch
`nn.Linear(in_features, out_features)` encapsula `w` e `b` como parâmetros aprendíveis
e aplica `z = xWᵀ + b` internamente. A ativação é aplicada em seguida:

```python
self.linear   = nn.Linear(n, 1)
self.ativacao = nn.Sigmoid()

def forward(self, x):
    return self.ativacao(self.linear(x))
```

### Inicialização dos pesos
O PyTorch inicializa `nn.Linear` com a heurística de **Kaiming uniform**
(variação de He et al., 2015). A qualidade da inicialização afeta a convergência,
principalmente em redes profundas — ponto discutido por **Glorot & Bengio (2010)**.

### Do forward à regra de decisão
Para classificação binária com sigmoide, a fronteira de decisão é o conjunto
`{x : σ(wᵀx + b) = 0.5}`, equivalente a `{x : wᵀx + b = 0}` — ou seja, mesmo com
sigmoide, a **fronteira continua sendo um hiperplano**. Somente redes com múltiplas
camadas produzem fronteiras não-lineares.

### Fonte acadêmica
- Glorot, X., & Bengio, Y. (2010). *Understanding the difficulty of training deep feedforward neural networks*. **Proceedings of AISTATS**, 9, 249–256. http://proceedings.mlr.press/v9/glorot10a.html

---

# Pré-requisitos para o Tópico 11 — MLP e Ativações

O Tópico 11 compara **Sigmoid vs Tanh** em uma MLP `2 → 3 → 1` treinada no dataset
*two moons*. Para entendê-lo em profundidade, os conceitos abaixo são necessários.

## A. Limitação do Perceptron e o problema XOR
Como já mencionado, um único neurônio produz apenas fronteiras lineares. O dataset
*two moons* — duas meias-luas entrelaçadas — é propositalmente **não linearmente
separável**, análogo ao XOR. Resolver esse problema **exige** empilhar neurônios.

## B. Multi-Layer Perceptron (MLP)
Uma MLP é uma composição de transformações afins + ativações:

```
h₁ = f₁(W₁ x + b₁)      ← camada oculta
ŷ  = f₂(W₂ h₁ + b₂)     ← camada de saída
```

Na configuração do notebook (`2 → 3 → 1`):
- `W₁ ∈ ℝ³ˣ²`, `b₁ ∈ ℝ³` → 9 parâmetros
- `W₂ ∈ ℝ¹ˣ³`, `b₂ ∈ ℝ¹` → 4 parâmetros
- Total: **13 parâmetros**.

Com apenas **3 neurônios ocultos**, cada um contribui com uma "dobra" ou "curva" para a
fronteira de decisão final. É justamente essa parcimônia que amplifica as diferenças entre
ativações — com muitos neurônios, qualquer ativação razoável daria fronteiras visualmente
parecidas.

## C. Backpropagation
O algoritmo que permite treinar redes multicamadas foi popularizado por
**Rumelhart, Hinton & Williams (1986)**. A ideia é aplicar a regra da cadeia para
propagar o gradiente da função de perda, da saída rumo às camadas iniciais:

```
∂L/∂W₁ = (∂L/∂ŷ) · (∂ŷ/∂h₁) · (∂h₁/∂W₁)
```

Cada `∂hₗ/∂hₗ₋₁` contém **a derivada da função de ativação** daquela camada — por isso
a forma da derivada importa tanto.

### Fonte acadêmica
- Rumelhart, D. E., Hinton, G. E., & Williams, R. J. (1986). *Learning representations by back-propagating errors*. **Nature**, 323(6088), 533–536. https://doi.org/10.1038/323533a0

## D. Sigmoide vs Tanh em detalhe

| Propriedade | Sigmoide `σ(z)` | Tangente hiperbólica `tanh(z)` |
|---|---|---|
| Faixa de saída | `(0, 1)` | `(−1, 1)` |
| Centro | `0.5` | `0` |
| Máximo da derivada | `σ'(0) = 0.25` | `tanh'(0) = 1` |
| Relação algébrica | `σ(z) = (tanh(z/2) + 1)/2` | `tanh(z) = 2σ(2z) − 1` |

### Por que tanh costuma treinar mais rápido
1. **Gradientes maiores**. Com derivada máxima 1, o sinal que chega por
   backpropagation é, em média, **4× maior** que o da sigmoide (máx. 0.25).
2. **Saída centrada em zero**. Isso equilibra os gradientes de entrada do próximo
   `W₂`, reduzindo o fenômeno de atualizações todas com o mesmo sinal (efeito zigue-zague
   descrito por **LeCun et al., 1998**).
3. **Menos saturação em torno da origem**. Ativações pequenas ficam na região
   mais "linear" da tanh, onde a derivada é próxima de 1.

### Vanishing gradient
Ambas saturam em `|z|` grande: `σ'(z) → 0` e `tanh'(z) → 0`. Quando empilhadas em muitas
camadas, essas derivadas se **multiplicam** no backprop e o gradiente efetivo tende a zero
— problema formalizado por **Hochreiter (1991)** e central para a adoção posterior da ReLU.

### Fonte acadêmica
- LeCun, Y., Bottou, L., Orr, G. B., & Müller, K.-R. (1998). *Efficient BackProp*. In **Neural Networks: Tricks of the Trade** (pp. 9–50). Springer. https://doi.org/10.1007/3-540-49430-8_2

## E. Função de perda BCE e otimizador Adam
- **Binary Cross-Entropy** (Tópico 6 do notebook) é a perda natural para saídas em `(0, 1)`,
  pois é a log-verossimilhança negativa da distribuição Bernoulli.
- **Adam** (Kingma & Ba, 2015) combina momentum com normalização adaptativa por parâmetro,
  sendo robusto a escolhas de taxa de aprendizado — por isso é o otimizador usado no
  experimento do Tópico 11.

### Fonte acadêmica
- Kingma, D. P., & Ba, J. (2015). *Adam: A Method for Stochastic Optimization*. **3rd International Conference on Learning Representations (ICLR)**. https://arxiv.org/abs/1412.6980

## F. Reprodutibilidade via semente aleatória
O Tópico 11 chama `torch.manual_seed(42)` **antes** de instanciar cada MLP, garantindo que
ambas partam **exatamente dos mesmos pesos iniciais**. Assim, toda diferença observada em
convergência ou fronteira de decisão é atribuível **apenas** à função de ativação — controle
experimental essencial para uma comparação honesta.

## G. Fronteira de decisão como diagnóstico
Plotar a fronteira de decisão `{x : ŷ(x) = 0.5}` sobre a grade de entrada é a forma mais
direta de visualizar o que cada ativação permitiu à rede representar. Com 3 neurônios e
dados em 2D, a fronteira aparece como a união/interseção de três "semi-planos suavizados"
— um por neurônio da camada oculta.

---

## Referências consolidadas

Todas as fontes citadas são artigos/livros acadêmicos revisados por pares, escritos por humanos:

1. **McCulloch, W. S., & Pitts, W.** (1943). A logical calculus of the ideas immanent in nervous activity. *Bulletin of Mathematical Biophysics*, 5(4), 115–133.
2. **Rosenblatt, F.** (1958). The perceptron: A probabilistic model for information storage and organization in the brain. *Psychological Review*, 65(6), 386–408.
3. **Minsky, M., & Papert, S.** (1969). *Perceptrons: An Introduction to Computational Geometry*. MIT Press.
4. **Rumelhart, D. E., Hinton, G. E., & Williams, R. J.** (1986). Learning representations by back-propagating errors. *Nature*, 323(6088), 533–536.
5. **Hornik, K., Stinchcombe, M., & White, H.** (1989). Multilayer feedforward networks are universal approximators. *Neural Networks*, 2(5), 359–366.
6. **LeCun, Y., Bottou, L., Orr, G. B., & Müller, K.-R.** (1998). Efficient BackProp. In *Neural Networks: Tricks of the Trade* (pp. 9–50). Springer.
7. **Glorot, X., & Bengio, Y.** (2010). Understanding the difficulty of training deep feedforward neural networks. *Proceedings of AISTATS*, 9, 249–256.
8. **Kingma, D. P., & Ba, J.** (2015). Adam: A Method for Stochastic Optimization. *ICLR 2015*.
