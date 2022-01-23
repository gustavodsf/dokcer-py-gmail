@ECHO OFF

ECHO Criando a imagem do aplicativo para o Docker
docker build . -t py-gmail-app

Echo Colocando a imagem para rodar
docker run -d  -v c:/data:/data py-gmail-app

PAUSE


