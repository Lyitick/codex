# Finance Bot

Telegram бот для ведения личных финансов на базе **aiogram 3**, SQLite и FSM. Проект готов к деплою и оснащён тестами.

## Возможности
- Учёт доходов и расходов, в том числе спонтанных покупок.
- Вишлист с приоритетами и отметкой выполнения.
- Базовая статистика по расходам и выполненным желаниям.
- FSM-сценарии для пошагового ввода данных.
- Логирование в файл и консоль.

## Требования
- Python 3.10+
- [Poetry](https://python-poetry.org/) или `pip`

## Установка
```bash
# клонирование и подготовка
git clone <YOUR_REPO_URL>
cd finance_bot

# установка зависимостей с Poetry
poetry install

# или с помощью pip
pip install -r requirements.txt
```

## Настройка окружения
1. Скопируйте файл `.env.example` в `.env`.
2. Укажите токен телеграм-бота и при необходимости путь к базе данных:
```
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=sqlite+aiosqlite:///./finance_bot.db
LOG_LEVEL=INFO
```

## Запуск бота
```bash
# через poetry
poetry run python bot/main.py

# или напрямую
python bot/main.py
```

## Тесты
```bash
# все тесты
poetry run pytest --cov=bot --cov-report=term-missing

# или
python -m pytest
```

## Работа с GitHub
```bash
git init
git remote add origin <YOUR_GITHUB_REPOSITORY_URL>
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main
```

## Структура проекта
Основные директории:
- `bot/` — код бота, конфиги, хэндлеры, состояния и т.д.
- `tests/` — модульные и интеграционные тесты.
- `logs/` — папка для логов (игнорируется гитом).

