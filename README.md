# Interview Preparation Telegram Bot

Telegram-бот для подготовки к техническим собеседованиям в области IT.

Проект позволяет выбрать направление (Frontend, Backend, ML+DS, Mobile), уровень сложности (Junior, Middle, Senior) и пройти тест с вопросами и вариантами ответов. По завершении теста бот показывает темы, которые стоит повторить.

---

## 🚀 Быстрый старт

1. Клонируйте репозиторий:

```bash
git clone https://github.com/ВАШ_НИК/ВАШ_РЕПОЗИТОРИЙ.git
cd ВАШ_РЕПОЗИТОРИЙ
````

2. Создайте виртуальное окружение:

```bash
python -m venv venv
venv\Scripts\activate    # для Windows
# или
source venv/bin/activate  # для Mac/Linux
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Укажите свой токен бота в файле `bot/bot.py`:

```python
TOKEN = 'ВАШ_ТОКЕН_ОТ_BOTFATHER'
```

5. Запустите бота:

```bash
python -m bot.bot
```

---

## 📚 Структура проекта

```
interview_tg_bot/
├── bot/
│   ├── __init__.py
│   ├── bot.py          # основной код бота
│   ├── utils.py        # загрузка вопросов
├── data/
│   ├── Backend/
│   ├── Frontend/
│   ├── ML_and_DS/
│   ├── Mobile/
│       └── (JSON-файлы с вопросами по направлениям и уровням)
├── requirements.txt     # зависимости проекта
└── README.md             # описание проекта
```

---

## ⚙️ Функциональность

* Выбор направления: Frontend, Backend, ML+DS, Mobile
* Выбор уровня сложности: Junior, Middle, Senior
* 20 случайных вопросов на сессию
* Подсчёт количества правильных ответов
* Вывод тем и полезных ссылок для повторения после теста
* Обработка ошибок и пропуск некорректных вопросов

---

## 🛠 Стек технологий

* Python 3.11
* Библиотека [python-telegram-bot==13.15](https://github.com/python-telegram-bot/python-telegram-bot)
* JSON-файлы для хранения вопросов

---

## 📌 Заметки

* Папка `data/` с вопросами должна быть расположена в корне проекта.
* Папка виртуального окружения `venv/` добавлена в `.gitignore` и не загружается на GitHub.
* Для корректной работы все вопросы в JSON должны иметь обязательные поля: `question`, `answers`, `correct_answer_id`, `useful_info`, `theme`.

---

## 📩 Обратная связь

Если у вас есть идеи по улучшению проекта или вы нашли баги — открывайте issue или делайте pull request!

---