@SETLOCAL
@PATH=C:\Program Files\Git\cmd;%PATH%
@SET PIPENV_VENV_IN_PROJECT=1
@py -m pipenv %*
@ENDLOCAL