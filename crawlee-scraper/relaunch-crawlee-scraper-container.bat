docker system prune --force
docker container kill crawlee_scraper
docker container rm crawlee_scraper
docker build -t crawlee_scraper:latest . && docker run -d  --memory 4g -p 127.0.0.1:5840:5840 --name crawlee_scraper crawlee_scraper:latest
