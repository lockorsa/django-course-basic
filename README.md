# django-course-basic

# python версия 3.10
# Для управления пакетами и зависимостями использую poetry
1. pip install poetry (можно ставить в глобальный pip)
2. poetry update (скачиваем пакеты из лок-файла)
3. poetry shell (активируем окружение в терминале)
* необходимо выполнять каждый раз при начале работы
# Миграции
1. python manage.py makemigrations
2. python manage.py migrate
# Тестовые данные(фикстуры)
* для товаров и категорий важен порядок установки (у категорий ManyToManyField к продуктам)
1. manage.py loaddata products 
2. manage.py loaddata categories
# Добавляем в бд суперюзера (django geekbrains)
1. python manage.py set_admin
