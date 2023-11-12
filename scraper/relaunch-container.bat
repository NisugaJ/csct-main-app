docker system prune --force
docker container kill scraper
docker container rm scraper
docker build -t scraper:latest . && docker run -p 127.0.0.1:5842:5842 --name scraper scraper:latest
