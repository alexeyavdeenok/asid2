"""
Модуль реализует окрашивание подстрок в строке
"""
import argparse
import os
import time
from colorama import init, Fore, Style, Back
from search import search


def log_execution_time(func):
    """
    Логирование времени выполнения
    :param func: функция
    :return:
    """
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in "
              f"{execution_time:.8f} seconds")
        return result
    return wrapper


def create_parser():
    """
    Создание парсера для строки аргументов
    :return:
    """
    parser = argparse.ArgumentParser(description="Утилита для поиска "
                                                 "подстрок в строке с "
                                                 "различными параметрами")

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
        help="Чувствительность к регистру "
             "(по умолчанию - нечувствительный поиск)."
    )

    # Аргумент для метода поиска (с начала или с конца строки)
    parser.add_argument(
        "-m", "--method",
        type=str,
        choices=['first', 'last'],
        default='first',
        help="Метод поиска: 'first' для поиска с начала, "
             "'last' для поиска с конца."
    )

    # Аргумент для ограничения количества совпадений
    parser.add_argument(
        "-c", "--count",
        type=int,
        help="Количество совпадений, "
             "которые нужно найти (по умолчанию - все совпадения)."
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
        help="Ограничение на количество выводимых строк "
             "(по умолчанию - 10 строк)."
    )

    return parser


def read_file(file_path, line_limit=10):
    """
    Функция для чтения текста из фала
    :param file_path: путь к файлу
    :param line_limit: максимальное число строк
    :return: строка
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        limited_lines = lines[:line_limit]

        return ''.join(limited_lines)


@log_execution_time
def main():
    """
    Основная функция которая реализует окрашивание строки
    :return:
    """
    parser = create_parser()
    args = parser.parse_args()

    # Если указан файл, читаем содержимое из файла
    if args.file:
        try:
            target_string = read_file(args.file)
        except FileNotFoundError:
            print('Файл не найден')
            return
    else:
        if args.string is None:
            raise ValueError("Необходимо указать либо строку, "
                             "либо путь к файлу.")
        target_string = args.string

    # Параметры для поиска
    substrings = args.substrings
    case_sensitivity = args.case_sensitivity
    method = args.method
    count = args.count

    init()

    if len(substrings) == 1:
        tuple_subs = search(target_string, substrings[0],
                            case_sensitivity, method, count)
        if tuple_subs is None:
            print(target_string)
        else:
            list_of_subs = []
            for i in tuple_subs:
                mas = [i, len(substrings[0]), Fore.RED]
                list_of_subs.append(tuple(mas))
            print(color_text(target_string, list_of_subs))
    else:
        dictionary = search(target_string, substrings,
                            case_sensitivity, method, count)
        if dictionary is None:
            print(target_string)
        else:
            print(color_text_many(target_string,
                                  make_tuple_of_subs(dictionary)))


def color_text(text, highlights):
    """
    Окрашивает подстроки в строке по заданным параметрам.

    :param text: исходная строка
    :param highlights: список кортежей формата
    (индекс начала подстроки, длина подстроки, цвет)
    :return: строка с окрашенными подстроками
    """
    colored_text = ""
    last_index = 0

    highlights = sorted(highlights, key=lambda x: x[0])

    for start, length, color in highlights:
        colored_text += text[last_index:start]
        colored_text += color + text[start:start + length] + Style.RESET_ALL
        last_index = start + length

    colored_text += text[last_index:]

    return colored_text


def make_tuple_of_subs(dictionary):
    """
    Создает вспомогательный список кортежей формата
    (индекс, подстрока, цвет)
    :param dictionary: словарь
    :return: список кортежей
    """
    list_of_tuples = []
    colors = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE,
              Fore.BLACK + Back.WHITE, Fore.CYAN,
              Fore.MAGENTA, Fore.RED + Back.WHITE, Fore.YELLOW + Back.WHITE,
              Fore.GREEN + Back.WHITE,
              Fore.MAGENTA + Back.WHITE, Fore.RED + Back.YELLOW,
              Fore.BLACK + Back.YELLOW,
              Fore.GREEN + Back.RED, Fore.GREEN + Back.YELLOW,
              Fore.CYAN + Back.RED]
    index_colors = 0
    for key, value in dictionary.items():
        if value is None:
            continue
        for i in value:
            list_of_tuples.append(tuple([i, key, colors[index_colors]]))
        index_colors += 1
    return list_of_tuples


def color_text_many(text, subs):
    """
    Окрашивание строки если введено несколько подстрок
    :param text: строка
    :param subs: подстроки
    :return: окрашенный текст
    """
    subs.sort(key=lambda x: (x[0], x[1]))
    colored_text = ""
    current_index = 0

    while subs:
        start, substring, color = subs.pop(0)
        length = len(substring)

        if current_index < start:
            colored_text += text[current_index:start]
            current_index = start

        if current_index > start:
            overlap = current_index - start
            non_overlap_substring = substring[overlap:]
            original_substring_part = \
                text[current_index:current_index + len(non_overlap_substring)]

            colored_text += color + original_substring_part + Style.RESET_ALL

            current_index += len(non_overlap_substring)
        else:
            original_substring_part = text[start:start + length]
            colored_text += color + original_substring_part + Style.RESET_ALL

            current_index = start + length

    if current_index < len(text):
        colored_text += text[current_index:]

    return colored_text


if __name__ == "__main__":
    main()
