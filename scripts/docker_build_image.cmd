@echo off
PUSHD ..

docker build . -t lexxai/web_hw_05
docker images

POPD