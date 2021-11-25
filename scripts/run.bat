@echo off
PUSHD %~dp0

call %~dp0\env\py3.7_win\Scripts\activate.bat
python -u cube2sphere.py

popd