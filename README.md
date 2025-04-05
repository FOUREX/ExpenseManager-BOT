# БОТ Менеджер витрат
[![Python](https://img.shields.io/badge/Python-3.13+-3776AB?logo=python&logoColor=white&style=flat)](https://www.python.org/downloads/release/python-3132/)
[![Poetry](https://img.shields.io/badge/Aiogram-3.x-blue?style=flat&logo=telegram)](https://aiogram.dev/)


## Запуск проєкту
### 1. Встановлення необхідних залежностей
```shell
poetry install --no-root
```

### 2. Запуск віртуального середовища
```shell
poetry env use python3.13
```

Для Windows (якщо результатом виконання команди буде тільки шлях до `.bat` файлу - вставте його в консоль та запустіть):
```shell
poetry env activate
```

Для Linux:
```shell
eval $(poetry env activate)
```

### 3. Створити файл `.env` в корені проєкту на основі `.env.template` та заповнити необхідні поля
```
BOT_TOKEN=token
API_URL=http://127.0.0.1:25565
```

### 4. Запуск бота
```shell
py -m src.main
```
