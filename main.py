import argparse
import os
from search import search
from colorama import init, Fore, Style, Back


# Создание парсера для аргументов командной строки
def create_parser():
    parser = argparse.ArgumentParser(description="Утилита для поиска подстрок в строке с различными параметрами")

    # Аргумент для исходной строки
    parser.add_argument(
        "-s", "--string",
        type=str,
        help="Целевая строка для поиска подстрок.",
        required=False
    )

    # Аргумент для подстрок, которые нужно найти
    parser.add_argument(
        "-sub", "--substrings",
        nargs='+',
        type=str,
        help="Подстроки для поиска (можно указать несколько).",
        required=True
    )

    # Аргумент для чувствительности к регистру
    parser.add_argument(
        "-cs", "--case-sensitivity",
        action='store_true',
        help="Чувствительность к регистру (по умолчанию - нечувствительный поиск)."
    )

    # Аргумент для метода поиска (с начала или с конца строки)
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=['first', 'last'],
        default='first',
        help="Метод поиска: 'first' для поиска с начала, 'last' для поиска с конца."
    )

    # Аргумент для ограничения количества совпадений
    parser.add_argument(
        "-c", "--count",
        type=int,
        help="Количество совпадений, которые нужно найти (по умолчанию - все совпадения)."
    )

    # Аргумент для указания пути к файлу
    parser.add_argument(
        "-f", "--file",
        type=str,
        help="Путь к файлу для поиска подстрок в содержимом файла.",
        required=False
    )

    # Аргумент для ограничения на количество выводимых строк
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=10,
        help="Ограничение на количество выводимых строк (по умолчанию - 10 строк)."
    )

    return parser


# Функция для чтения файла, если указан путь к файлу
def read_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Главная функция, которая получает аргументы и вызывает функцию поиска
def main():
    parser = create_parser()
    args = parser.parse_args()

    # Если указан файл, читаем содержимое из файла
    if args.file:
        target_string = read_file(args.file)
    else:
        if args.string is None:
            raise ValueError("Необходимо указать либо строку, либо путь к файлу.")
        target_string = args.string

    # Параметры для поиска
    substrings = args.substrings
    case_sensitivity = args.case_sensitivity
    method = args.method
    count = args.count
    limit = args.limit
    print(target_string, substrings, case_sensitivity, method, count)

    # Здесь должна быть реализация функции поиска в search.py
    # Например:
    # from search import search
    # result = search(target_string, substrings, case_sensitivity, method, count)
    init()
    # Выводим результат (для примера используем заглушку)
    if len(substrings) == 1:
        tuple_subs = search(target_string, substrings[0], case_sensitivity, method, count)
        list_of_subs = []
        for i in tuple_subs:
            mas = [i, len(substrings[0]), Fore.RED]
            list_of_subs.append(tuple(mas))
        print(color_text(target_string, list_of_subs))


def color_text(text, highlights):
    """
    Окрашивает подстроки в строке по заданным параметрам.

    :param text: исходная строка
    :param highlights: список кортежей формата (индекс начала подстроки, длина подстроки, цвет)
    :return: строка с окрашенными подстроками
    """
    colored_text = ""
    last_index = 0

    # Сортируем по индексу начала подстроки, чтобы корректно обрабатывать перекрытия
    highlights = sorted(highlights, key=lambda x: x[0])

    for start, length, color in highlights:
        # Добавляем неокрашенную часть строки
        colored_text += text[last_index:start]
        # Добавляем окрашенную подстроку
        colored_text += color + text[start:start + length] + Style.RESET_ALL
        # Обновляем индекс последней обработанной позиции
        last_index = start + length

    # Добавляем оставшуюся часть строки, если она есть
    colored_text += text[last_index:]

    return colored_text


if __name__ == "__main__":
    main()
