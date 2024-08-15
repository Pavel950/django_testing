# Django testing  
В проекте реализованы pytest-тесты для проекта ya_news и unittest-тесты для проекта ya_note.

Коллекция тестов проверяет маршруты, контент и логику приложений. В тестах применяются фикстуры и параметризация.

Структура репозитория:
```
Dev
 └── django_testing
     ├── ya_news
     │   ├── news
     │   │   ├── fixtures/
     │   │   ├── migrations/
     │   │   ├── pytest_tests/   <- Директория с тестами pytest для проекта ya_news
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanews/
     │   ├── manage.py
     │   └── pytest.ini
     ├── ya_note
     │   ├── notes
     │   │   ├── migrations/
     │   │   ├── tests/          <- Директория с тестами unittest для проекта ya_note
     │   │   ├── __init__.py
     │   │   ├── admin.py
     │   │   ├── apps.py
     │   │   ├── forms.py
     │   │   ├── models.py
     │   │   ├── urls.py
     │   │   └── views.py
     │   ├── templates/
     │   ├── yanote/
     │   ├── manage.py
     │   └── pytest.ini
     ├── .gitignore
     ├── README.md
     ├── requirements.txt
     └── structure_test.py
```
