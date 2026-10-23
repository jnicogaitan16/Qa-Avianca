@echo off
setlocal EnableExtensions
set "HERE=%~dp0"
if exist "%HERE%..\..\pbi\__main__.py" (
  set "ROOT=%HERE%..\.."
  set "PY=%HERE%python.exe"
) else (
  set "ROOT=%HERE%.."
  set "PY=%HERE%..\.venv\Scripts\python.exe"
)
pushd "%ROOT%"
"%PY%" -m pbi.atajos corre %*
set "CODE=%ERRORLEVEL%"
popd
exit /b %CODE%
