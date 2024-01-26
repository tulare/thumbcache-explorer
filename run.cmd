@SETLOCAL

@REM -- Paramétrage --
@SET "APPLI_NAME=%1"

@REM -- Environnement --
@SET "APP_DIR=%~dp0"
@SET "PIPENV_PIPFILE=%APP_DIR%Pipfile"
@SET PIPENV_VENV_IN_PROJECT=1
@SET PIPENV_NO_INHERIT=1
@SET PIPENV_TIMEOUT=300

@REM -- Vérification présence environnement virtuel (.venv) --
@py.exe -m pipenv --venv || GOTO :novenv

@REM -- Exécuter l'application --
@PUSHD "%APP_DIR%"
@ECHO %APP_DIR%%APPLI_NAME%
@py.exe -m pipenv run %*
@GOTO :EOF

:novenv
@ECHO Erreur: aucun environnement virtuel (.venv) n'est disponible

@ENDLOCAL