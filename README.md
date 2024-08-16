# Backend 

### Используемая методология TDD (Test-Driven Development)

- **Основные принципы**:
  - **Писать тесты перед реализацией функционала**: Сначала создаются тесты для новых функций, а затем пишется код, который удовлетворяет этим тестам.
  - **Частые и небольшие циклы разработки**: Тесты пишутся для небольших изменений в коде, что позволяет быстрее находить и исправлять ошибки.
  - **Чистый и поддерживаемый код**: Регулярное рефакторинг кода после успешного прохождения тестов.
 
### Используемые технологии:
 - fastapi
 - sqlalchemy
 - pytest-asyncio
 - poetry
 - alembic

### Миграции
Все созданные модели таблиц базы данных должны быть импортированы в src/models.py

- **Автогенерация миграций** - ```alembic revision --autogenerate```
- **Применить миграции** - ```alembic upgrade head```
- **Откатить миграции** - ```alembic downgrade {идентификатор ревизии}```

### Ендпоинты
* [Endpoints](https://github.com/RideTrip-tour/Wiki/blob/main/Endpoints.md)
