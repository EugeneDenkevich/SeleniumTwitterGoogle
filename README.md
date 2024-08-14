# Тесты Google, Twitter, ChatGPT
## Несколько тестов, осуществляющих взаимодействие с UI и API Google, Twitter и CHatGPT с целью изменения и извлечения данных.

### Установка пакетов
```
poetry install --no-root
```

### Настройка pre-commit
```
pre-commit install
```

### Настройка окружения
```
cp .env-example .env
```

Заполнить `.env` нужными данными.
[Справка по Twitter API](https://developer.x.com/en/docs/platform-overview).

Перед началом тестовой сесии **убедитесь, что ввели верные значения в `.env` файле!** К примеру, вы могли оставить старые `имя` и `фамилию` аккаунта гугл.
За всеми пояснениям обратитесь к [разработчику](https://t.me/im_eugenestudio).

### Запуск
```
poetry run pytest
```

#### © Евгений Денкевич, 2024.
