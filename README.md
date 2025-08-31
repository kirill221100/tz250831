создайте .env файл на подобии .env.example

запустить приложение: docker compose --env-file .env up --build

запустить тесты в докере: docker compose -f tests/test-docker-compose.yml --env-file .env up --build
