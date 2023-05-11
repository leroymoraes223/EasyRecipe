@echo off

set /P secret_key="Enter Your Secret Key: "
echo %secret_key%
set /P database_name="Enter Name of database:"
echo SECRET_KEY="%secret_key%" > .\.env
echo &echo\DATABASE_URI="sqlite:///%database_name%.db" >> .\.env

start python -m venv venv
echo "wait for python window to close then "
pause
start .\venv\Scripts\pip.exe install -r ./requirements.txt
