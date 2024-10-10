@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("%~nx0 h",0)(window.close)&&exit
:begin
taskkill /IM kcwebplus.exe /F  /T
timeout /t 1 /nobreak
kcwebplus server
timeout /t 3 /nobreak
start http://127.0.0.1:39001