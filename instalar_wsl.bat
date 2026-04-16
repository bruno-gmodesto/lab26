@echo off
chcp 65001 >nul
title Instalador WSL - Lab26

echo ============================================
echo   Instalador do WSL para o projeto Lab26
echo ============================================
echo.

:: Verifica se esta rodando como administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Este script precisa ser executado como ADMINISTRADOR.
    echo Clique com o botao direito no arquivo e selecione "Executar como administrador".
    pause
    exit /b 1
)

echo [INFO] Verificando se o WSL ja esta instalado...
wsl --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] WSL ja esta instalado no sistema.
    echo.
    wsl --version
    echo.
    echo Se quiser prosseguir com a configuracao do ambiente,
    echo abra o Ubuntu pelo menu Iniciar e execute o script setup_poetry.sh
    pause
    exit /b 0
)

echo [INFO] WSL nao encontrado. Iniciando instalacao...
echo.
echo [AVISO] Apos a instalacao, o computador precisara REINICIAR.
echo Pressione qualquer tecla para continuar ou feche esta janela para cancelar.
pause >nul

echo.
echo [1/2] Instalando o WSL com Ubuntu (padrao)...
echo       Isso pode demorar alguns minutos...
echo.
wsl --install

if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Falha na instalacao do WSL.
    echo Verifique se a virtualizacao esta habilitada na BIOS.
    pause
    exit /b 1
)

echo.
echo ============================================
echo   Instalacao do WSL concluida!
echo ============================================
echo.
echo [PROXIMO PASSO] O computador precisa ser REINICIADO.
echo Apos reiniciar:
echo   1. O Ubuntu vai abrir automaticamente para criar seu usuario
echo   2. Defina um nome de usuario e senha
echo   3. Abra o terminal Ubuntu e execute o script setup_poetry.sh
echo.
echo Deseja reiniciar agora? (S/N)
set /p resposta="> "
if /i "%resposta%"=="S" (
    shutdown /r /t 10 /c "Reiniciando para finalizar instalacao do WSL..."
    echo [INFO] O computador reiniciara em 10 segundos...
) else (
    echo [INFO] Lembre-se de reiniciar o computador antes de usar o WSL.
)

pause
