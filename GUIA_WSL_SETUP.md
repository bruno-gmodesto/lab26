# Guia: Configurando o WSL para rodar o projeto Lab26 no Windows

Este guia resolve o problema de dependencias que so funcionam em Linux. Em vez de usar uma maquina virtual pesada e lenta, vamos usar o **WSL (Windows Subsystem for Linux)**, que roda Ubuntu diretamente dentro do Windows com desempenho nativo.

> **Resumo:** WSL + Ubuntu + Poetry = rodar o projeto no Windows como se estivesse no Linux, sem VM.

---

## Pre-requisitos

- Windows 10 (versao 2004+) ou Windows 11
- Conexao com a internet
- Acesso de administrador no computador

---

## Parte 1 — Instalar o WSL no Windows

### Opcao A: Usar o script automatico

1. Clique com o **botao direito** no arquivo `instalar_wsl.bat`
2. Selecione **"Executar como administrador"**
3. Siga as instrucoes na tela
4. **Reinicie o computador** quando solicitado

### Opcao B: Fazer manualmente

#### 1.1. Abrir o PowerShell como Administrador

- Pressione `Win + S`, digite **PowerShell**
- Clique com o botao direito em **"Windows PowerShell"**
- Selecione **"Executar como administrador"**

#### 1.2. Instalar o WSL

No PowerShell, execute:

```powershell
wsl --install
```

Esse comando instala o WSL 2 com Ubuntu como distribuicao padrao.

> **Nota:** Se o comando retornar erro, pode ser necessario habilitar a virtualizacao na BIOS do computador. Procure por "Intel VT-x" ou "AMD-V" nas configuracoes da BIOS.

#### 1.3. Reiniciar o computador

Apos a instalacao, **reinicie o computador**. Isso e obrigatorio para finalizar a configuracao do WSL.

#### 1.4. Configurar o usuario Ubuntu

Apos a reinicializacao, o Ubuntu vai abrir automaticamente (ou abra pelo menu Iniciar procurando por **"Ubuntu"**).

Ele vai pedir:

- **Nome de usuario** — escolha um nome simples (ex: `aluno`)
- **Senha** — defina uma senha (ela nao aparece enquanto voce digita, isso e normal)

Pronto! Voce agora tem um terminal Linux rodando dentro do Windows.

---

## Parte 2 — Configurar o ambiente do projeto

### Opcao A: Usar o script automatico

1. No terminal Ubuntu, navegue ate a pasta onde esta o `setup_poetry.sh`:

```bash
cd /caminho/para/o/projeto
```

> **Dica:** Seus arquivos do Windows ficam acessiveis em `/mnt/c/Users/SeuUsuario/...`  
> Exemplo: `/mnt/c/Users/joao/Downloads/lab26`

2. De permissao de execucao e rode o script:

```bash
chmod +x setup_poetry.sh
./setup_poetry.sh
```

3. Siga as instrucoes na tela.

### Opcao B: Fazer manualmente

#### 2.1. Atualizar os pacotes do sistema

```bash
sudo apt update -y
```

Isso atualiza a lista de pacotes disponiveis. Necessario antes de instalar qualquer coisa.

#### 2.2. Instalar dependencias do sistema

```bash
sudo apt install -y python3 python3-pip python3-venv pipx git
```

O que cada um faz:
- `python3` — interpretador Python
- `python3-pip` — gerenciador de pacotes Python
- `python3-venv` — suporte a ambientes virtuais
- `pipx` — instala ferramentas Python em ambientes isolados (usado para instalar o Poetry)
- `git` — para clonar repositorios

#### 2.3. Configurar o PATH do pipx

```bash
pipx ensurepath
```

Depois, **feche e reabra o terminal** (ou execute `source ~/.bashrc`) para aplicar a mudanca no PATH.

#### 2.4. Instalar o Poetry

```bash
pipx install poetry
```

Verifique se instalou corretamente:

```bash
poetry --version
```

Deve exibir algo como `Poetry (version 2.x.x)`.

#### 2.5. Clonar o repositorio do projeto

```bash
cd ~
git clone <URL_DO_REPOSITORIO>
cd lab26
```

> Substitua `<URL_DO_REPOSITORIO>` pela URL do repositorio fornecida pelo professor.

#### 2.6. Instalar as dependencias do projeto

Dentro da pasta do projeto (onde esta o `pyproject.toml`):

```bash
poetry install
```

Isso cria um ambiente virtual e instala todas as bibliotecas listadas no `pyproject.toml`.

> **Nota:** Na primeira vez pode demorar bastante pois precisa baixar o PyTorch e outras dependencias grandes.

---

## Parte 3 — Rodar os arquivos Python

### 3.1. Ativar o ambiente virtual

Toda vez que abrir um novo terminal, antes de rodar qualquer script do projeto, ative o ambiente virtual:

```bash
cd ~/lab26
eval $(poetry env activate)
```

Voce vai notar que o prompt do terminal muda, indicando que o ambiente virtual esta ativo.

### 3.2. Executar um arquivo

```bash
python3 ./seu_arquivo.py
```

Exemplo:

```bash
python3 ./examples/exemplo.py
```

A saida sera identica a que voce veria rodando em uma VM Linux ou em um computador com Linux nativo.

---

## Resumo dos comandos (cola rapida)

```bash
# 1. No PowerShell como Admin (so uma vez):
wsl --install
# Reiniciar o PC

# 2. No terminal Ubuntu (so uma vez):
sudo apt update -y
sudo apt install -y python3 python3-pip python3-venv pipx git
pipx ensurepath
# Fechar e reabrir o terminal
pipx install poetry
git clone <URL_DO_REPOSITORIO>
cd lab26
poetry install

# 3. Toda vez que for rodar um script:
cd ~/lab26
eval $(poetry env activate)
python3 ./seu_arquivo.py
```

---

## Dicas uteis

### Acessar arquivos do Windows pelo Ubuntu

Os discos do Windows ficam montados em `/mnt/`:
- `C:\` fica em `/mnt/c/`
- `D:\` fica em `/mnt/d/`

Exemplo: `C:\Users\joao\Desktop` = `/mnt/c/Users/joao/Desktop`

### Acessar arquivos do Ubuntu pelo Windows

No Explorador de Arquivos do Windows, digite na barra de endereco:

```
\\wsl$\Ubuntu\home\seu_usuario
```

### Abrir o VS Code integrado com o WSL (recomendado)

Particularmente, utilizo o **Visual Studio Code** como IDE para este projeto e recomendo. Alem de executar arquivos `.py` normalmente pelo terminal integrado (com o mesmo resultado que no Linux), ele tambem abre e renderiza **Jupyter Notebooks (`.ipynb`)** sem nenhum problema, mantendo a visualizacao de celulas, graficos e outputs igual ao que voce veria em qualquer outro ambiente.

Para abrir o VS Code conectado ao WSL, dentro do terminal Ubuntu na pasta do projeto:

```bash
code .
```

Isso abre o VS Code conectado ao WSL, com acesso direto aos arquivos Linux.

> Requer a extensao **"WSL"** no VS Code (ele sugere instalar automaticamente).

Com o VS Code + WSL voce tem:
- Terminal integrado ja dentro do Ubuntu (sem precisar ficar alternando janelas)
- Execucao de arquivos `.py` com os mesmos resultados do Linux
- Visualizacao e execucao de notebooks `.ipynb` normalmente
- Syntax highlighting, autocomplete e todas as funcionalidades da IDE

### Problemas comuns

| Problema | Solucao |
|----------|---------|
| `wsl --install` da erro | Verifique se a virtualizacao esta habilitada na BIOS |
| `poetry: command not found` | Execute `pipx ensurepath` e reabra o terminal |
| `poetry install` falha em resolver dependencias | Tente `poetry lock --no-update` e depois `poetry install` |
| Permissao negada ao rodar `.sh` | Execute `chmod +x setup_poetry.sh` |
| Python nao encontra os pacotes | Certifique-se de ter ativado o venv com `eval $(poetry env activate)` |
