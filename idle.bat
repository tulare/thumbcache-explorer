@SETLOCAL
@SET APP_DIR=%~dp0
@PATH=C:\Program Files\Git\cmd;%PATH%
@SET PIPENV_PIPFILE=%APP_DIR%\Pipfile
@SET PIPENV_VENV_IN_PROJECT=1
@START "IDLE" /B /D %APP_DIR% py -m pipenv run pythonw -m idlelib %*
@ENDLOCAL