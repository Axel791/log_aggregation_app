## Инструкция

1) Для запуска создайте .env файл и скопируйте переменный из .env.example и заполните их
2) Запуск docker-compose up --build
3) Для создания супер пользователя перейдите в контейнер с web docker exec -it <container_name> bash
4) Создайте супер пользователя python manage.py createsuperuser
5) Чтобы обработать nginx логи используйте команду python manage.py pars_nginx_logs your/file/path

### Доступы:

1) Админка: http://localhost/admin/
2) Документация: http://localhost/redoc/