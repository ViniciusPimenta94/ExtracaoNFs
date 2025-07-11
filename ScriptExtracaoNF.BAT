@echo off
setlocal ENABLEDELAYEDEXPANSION
chcp 65001 >nul

REM Caminhos
set CONFIG_DIR=D:\ExtracaoNF\configs\extracao_nf_gpt
set EXECUTAVEL=D:\ExtracaoNF\dist\ExtratorNF\ExtratorNF.exe
set LOG_DIR=D:\ExtracaoNF\logs
set AGENDA_LOG=%LOG_DIR%\tarefa_agendada.log

REM Criar diret�rio de logs se n�o existir
if not exist %LOG_DIR% (
    mkdir %LOG_DIR%
)

REM Log da execu��o agendada - in�cio
echo [%DATE% %TIME%] Inicio da tarefa agendada >> %AGENDA_LOG%

echo Inicio da execucao em massa: %DATE% %TIME%
echo -------------------------------------------

REM Loop por todos os arquivos de configura��o
for %%F in (%CONFIG_DIR%\appsettings_*.json) do (
    set "ARQUIVO_CONFIG=%%~F"
    set "FILENAME=%%~nxF"
    set "CLIENTE=%%~nF"
    set "CLIENTE=!CLIENTE:appsettings_=!"

    echo.
    echo Cliente: !CLIENTE!
    echo Configuracao: !FILENAME!
    set CONFIG_FILE=!ARQUIVO_CONFIG!
    
    "%EXECUTAVEL%"
    
    echo Cliente !CLIENTE! finalizado.
    echo [%DATE% %TIME%] Executado !CLIENTE! >> %AGENDA_LOG%
)

echo.
echo Execucao concluida: %DATE% %TIME%
echo [%DATE% %TIME%] Fim da tarefa agendada >> %AGENDA_LOG%

endlocal
