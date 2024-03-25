# TruckTrack

**TruckTrack** - сервис поиска ближайших машин для перевозки грузов.
## Технологический стек

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django%20Rest%20Framework-009688?style=for-the-badge&logo=django&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Celery](https://img.shields.io/badge/celery-%2337814a.svg?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white)

## Начало работы

Эти инструкции позволят вам запустить копию проекта на вашем локальном компьютере для разработки и тестирования.

<details>
<summary><strong>Запуск с использованием Docker</strong></summary>

### Предварительные требования

Убедитесь, что у вас установлены Docker и Docker Compose. Это можно сделать, следуя официальной документации Docker: https://docs.docker.com/get-docker/ и https://docs.docker.com/compose/install/

### Установка и запуск

1. Клонируйте репозиторий на компьютер:
   ```
   git clone git@github.com:ragimov700/TruckTrack.git
   ```
2. Перейдите в папку infra:
   ```
   cd TruckTrack/infra/
   ```

3. Запустите проект с помощью Docker Compose:
   ```
   docker compose -f docker-compose.local.yml up
   ```
   
   Теперь приложение должно быть доступно по адресу:

   http://localhost:8000
   
   А документация доступна по адресу:
   
   http://localhost:8000/api/schema/swagger-ui/

</details>


**Автор** - [Шериф Рагимов](https://github.com/your-github-account)