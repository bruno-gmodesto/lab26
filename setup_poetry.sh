#!/bin/bash
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[INFO]${NC} $1"; }
ok()    { echo -e "${GREEN}[OK]${NC} $1"; }
warn()  { echo -e "${YELLOW}[AVISO]${NC} $1"; }
erro()  { echo -e "${RED}[ERRO]${NC} $1"; exit 1; }

echo ""
echo "============================================"
echo "  Setup do ambiente Poetry - Lab26"
echo "============================================"
echo ""

# --------------------------------------------------
# 1. Atualizar repositorios
# --------------------------------------------------
info "Atualizando lista de pacotes (apt update)..."
sudo apt update -y
ok "Lista de pacotes atualizada."
echo ""

# --------------------------------------------------
# 2. Instalar dependencias do sistema
# --------------------------------------------------
info "Instalando dependencias do sistema (python3, pip, pipx, git)..."
sudo apt install -y python3 python3-pip python3-venv pipx git
ok "Dependencias do sistema instaladas."
echo ""

# --------------------------------------------------
# 3. Garantir que o PATH do pipx esta configurado
# --------------------------------------------------
info "Configurando PATH do pipx..."
pipx ensurepath
ok "PATH do pipx configurado."
echo ""

# Recarrega o PATH para a sessao atual
export PATH="$HOME/.local/bin:$PATH"

# --------------------------------------------------
# 4. Instalar Poetry via pipx
# --------------------------------------------------
if command -v poetry &> /dev/null; then
    ok "Poetry ja esta instalado: $(poetry --version)"
else
    info "Instalando Poetry via pipx..."
    pipx install poetry
    ok "Poetry instalado: $(poetry --version)"
fi
echo ""

# --------------------------------------------------
# 5. Clonar o projeto (se nao estiver na pasta dele)
# --------------------------------------------------
REPO_URL=""
PROJETO_DIR=""

# Verifica se ja existe um pyproject.toml no diretorio atual
if [ -f "pyproject.toml" ]; then
    ok "pyproject.toml encontrado no diretorio atual."
    PROJETO_DIR="$(pwd)"
else
    # Pede a URL do repositorio
    warn "Nenhum pyproject.toml encontrado no diretorio atual."
    echo ""
    read -p "Cole a URL do repositorio git do projeto (ou Enter para pular): " REPO_URL
    if [ -n "$REPO_URL" ]; then
        PROJETO_DIR="$HOME/$(basename "$REPO_URL" .git)"
        if [ -d "$PROJETO_DIR" ]; then
            warn "Diretorio $PROJETO_DIR ja existe. Usando o existente."
        else
            info "Clonando repositorio..."
            git clone "$REPO_URL" "$PROJETO_DIR"
            ok "Repositorio clonado em $PROJETO_DIR"
        fi
        cd "$PROJETO_DIR"
    else
        erro "Nenhum projeto encontrado. Execute este script dentro da pasta do projeto ou informe a URL do repositorio."
    fi
fi
echo ""

# --------------------------------------------------
# 6. Instalar dependencias do projeto via Poetry
# --------------------------------------------------
info "Instalando dependencias do projeto (poetry install)..."
info "Isso pode demorar na primeira vez..."
poetry install
ok "Dependencias instaladas com sucesso."
echo ""

# --------------------------------------------------
# 7. Instrucoes finais
# --------------------------------------------------
echo "============================================"
echo -e "  ${GREEN}Setup concluido!${NC}"
echo "============================================"
echo ""
echo "Para ativar o ambiente virtual e rodar seus arquivos:"
echo ""
echo -e "  ${YELLOW}cd ${PROJETO_DIR:-\$(pwd)}${NC}"
echo -e "  ${YELLOW}eval \$(poetry env activate)${NC}"
echo -e "  ${YELLOW}python3 ./seu_arquivo.py${NC}"
echo ""
echo "Dica: sempre que abrir um novo terminal, execute:"
echo -e "  ${YELLOW}eval \$(poetry env activate)${NC}"
echo "para entrar no ambiente virtual antes de rodar os scripts."
echo ""
