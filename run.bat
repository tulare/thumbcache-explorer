@SETLOCAL
@SET APP_DIR=%~dp0
@PATH=C:\Program Files\Git\cmd;%PATH%
@SET PIPENV_PIPFILE=%APP_DIR%\Pipfile
@SET PIPENV_VENV_IN_PROJECT=1
@py -m pipenv run python %APP_DIR%\main.py %*
@ENDLOCAL