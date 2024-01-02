docker system prune --force
docker container kill nisugaj/crawlee_scraper:latest
docker container rm nisugaj/crawlee_scraper:latest
docker build -t nisugaj/crawlee_scraper:latest .
docker push nisugaj/crawlee_scraper:latest
docker run -d  --memory 4G -p 127.0.0.1:5840:5840 --name crawlee_scraper nisugaj/crawlee_scraper:latest
