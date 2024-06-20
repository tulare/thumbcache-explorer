@SETLOCAL

@IF EXIST .venv\Scripts\python.exe @GOTO :python_exe
@ECHO Aucun environement virtuel avec python
@GOTO :EOF

:python_exe
@FOR /F %%p in ('.venv\Scripts\python.exe -c "import sys; print(sys._base_executable)"') DO @(
	SET "PYTHON_EXE=%%p"
)

:pipenv
@SET PIPENV_VENV_IN_PROJECT=1
@%PYTHON_EXE% -m pipenv run python %*

@ENDLOCAL