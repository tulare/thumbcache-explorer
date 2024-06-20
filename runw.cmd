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
@SET "PYTHONW_EXE=%PYTHON_EXE:.exe=w.exe%"
@START %PYTHONW_EXE% -m pipenv run pythonw %*

@ENDLOCAL