@echo off
PUSHD ..\tests

docker run -it -d --rm -p 8000:8000  -v web_hw_05_volume:/app/logs  --name web_hw_05  lexxai/web_hw_05   

docker volume ls
                    

POPD