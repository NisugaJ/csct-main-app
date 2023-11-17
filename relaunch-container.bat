docker system prune --force
docker container kill csct_main_app
docker container rm csct_main_app
docker build -t csct_main_app:latest . && docker run -p 127.0.0.1:5842:5842 --name csct_main_app csct_main_app:latest
