import json
import os

def load_questions(direction: str, level: str):
    filename = f"{level.lower()}_{direction.lower()}.json"
    filepath = os.path.join('data', direction, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")

    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Теперь data — это список option'ов
    all_questions = []
    for option in data:
        all_questions.extend(option['questions'])

    return all_questions
