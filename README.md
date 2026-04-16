# Lab26 for Windows (WSL Port)

Fork do laboratorio de **Algoritmos de Busca e Aprendizado de Maquina** do prof. [davips](https://github.com/davips), adaptado para rodar no **Windows via WSL (Windows Subsystem for Linux)**.

A biblioteca original foi feita para Linux, o que obrigava alunos com Windows a usarem uma maquina virtual com desempenho ruim. Este repositorio resolve isso: com o WSL voce roda tudo nativamente no Windows, sem VM, sem perda de desempenho.

---

## O que tem no projeto

| Pasta | Conteudo |
|-------|----------|
| `src/lab/busca/` | Biblioteca de busca: agente, grade, grafo, alvo |
| `src/lab/am/` | Aprendizado de maquina: classificacao, modelos (Perceptron, MLP) |
| `src/lab/gan/` | GAN: redes geradora e discriminadora |
| `src/lab/` | Utilitarios: dataset (MNIST), perceptron |
| `busca/` | Exercicios de busca: aleatoria, largura, gulosa |
| `aprendizado/` | Exercicios de aprendizado: decision boundary com PyTorch |
| `examples/` | Exemplos de uso da biblioteca |
| `*.ipynb` | Notebooks com experimentos (Perceptron, PyTorch) |

---

## Inicio rapido

### 1. Instalar o WSL (so uma vez)

Abra o **PowerShell como Administrador** e execute:

```powershell
wsl --install
```

**Reinicie o computador.** Na volta, o Ubuntu abre para voce criar usuario e senha.

> Tambem disponibilizei o script `instalar_wsl.bat` que automatiza esse passo.  
> Clique com o botao direito > "Executar como administrador".

### 2. Configurar o ambiente (so uma vez)

No terminal Ubuntu:

```bash
# Atualizar pacotes
sudo apt update -y

# Instalar dependencias
sudo apt install -y python3 python3-pip python3-venv pipx git

# Configurar PATH do pipx
pipx ensurepath
source ~/.bashrc

# Instalar Poetry
pipx install poetry

# Clonar o projeto e instalar dependencias
git clone <URL_DO_REPOSITORIO>
cd lab26
poetry install
```

> Tambem disponibilizei o script `setup_poetry.sh` que automatiza todos esses passos.  
> Dentro do Ubuntu, na pasta do projeto: `chmod +x setup_poetry.sh && ./setup_poetry.sh`

### 3. Rodar os arquivos

Toda vez que abrir o terminal:

```bash
cd ~/lab26
eval $(poetry env activate)
python3 ./busca/largura.py
```

Pronto. Mesma saida que no Linux nativo.

---

## Scripts auxiliares

| Arquivo | Onde rodar | O que faz |
|---------|-----------|-----------|
| `instalar_wsl.bat` | Windows (como admin) | Instala o WSL + Ubuntu automaticamente |
| `setup_poetry.sh` | Dentro do Ubuntu/WSL | Configura Poetry, clona o repo e instala dependencias |

---

## IDE recomendada: VS Code

Particularmente, utilizo o **Visual Studio Code** e recomendo. Com a extensao **WSL** (o VS Code sugere instalar automaticamente), voce tem:

- Terminal integrado ja dentro do Ubuntu
- Execucao de arquivos `.py` com o mesmo resultado do Linux
- Visualizacao e execucao de **Jupyter Notebooks (`.ipynb`)** normalmente, com graficos e outputs
- Autocomplete, syntax highlighting e todas as funcionalidades da IDE

Para abrir o VS Code conectado ao WSL:

```bash
cd ~/lab26
code .
```

---

## Dependencias principais

- Python 3.11+
- PyTorch (CPU)
- scikit-learn
- matplotlib / seaborn / plotly
- NumPy / SciPy / Pandas

Todas gerenciadas pelo Poetry — basta rodar `poetry install`.

---

## Guia completo

Para um passo a passo detalhado (com prints, dicas e solucao de problemas), veja o [GUIA_WSL_SETUP.md](GUIA_WSL_SETUP.md).

---

> Projeto original: [davips/lab](https://github.com/davips) — UTFPR  
> Port para Windows (WSL): Bruno Azevedo
