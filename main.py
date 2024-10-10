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
    else:
        print(color_text_many(target_string, make_tuple_of_subs(search(target_string, substrings, case_sensitivity
                                                                 , method, count))))


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


def make_tuple_of_subs(dictionary):
    list_of_tuples = []
    colors = [Fore.GREEN, Fore.RED, Fore.YELLOW, Fore.BLUE, Fore.BLACK + Back.WHITE, Fore.CYAN,
              Fore.MAGENTA, Fore.RED + Back.WHITE, Fore.YELLOW + Back.WHITE, Fore.GREEN + Back.WHITE,
              Fore.MAGENTA + Back.WHITE]
    index_colors = 0
    for key, value in dictionary.items():
        if value is None:
            continue
        for i in value:
            list_of_tuples.append(tuple([i, key, colors[index_colors]]))
        index_colors += 1
    return list_of_tuples


# def color_text_many(text, subs):
#     subs.sort(key=lambda x: (x[0], x[1]))
#     current_index = 0
#     new_text = text[current_index:subs[0][0]]
#     current_index += len(new_text)
#     index_of_subs = 0
#     while current_index < len(text):
#         if current_index == subs[index_of_subs][0]:
#             new_text += subs[index_of_subs][2] + text[subs[index_of_subs][0]:subs[index_of_subs][0] +
#                                                                           len(subs[index_of_subs][1])] + Style.RESET_ALL
#             current_index += len(subs[index_of_subs][1])
#             index_of_subs += 1
#         elif current_index > subs[index_of_subs][0]:
#             if current_index > subs[index_of_subs][0] + len(subs[index_of_subs][1]) - 1:
#                 index_of_subs += 1
#                 new_text += text[current_index]
#                 current_index += 1
#             else:
#                 new_text += subs[index_of_subs][2] + text[current_index: subs[index_of_subs][0] + len(subs[index_of_subs][1])] \
#                             + Style.RESET_ALL
#         else:
#             new_text += text[current_index]
#             current_index += 1
#     return new_text
def color_text_many(text, subs):
    # Sort first by the start index (x[0]) and then alphabetically by the substring (x[1])
    subs.sort(key=lambda x: (x[0], x[1]))  # Sort by index and then by the substring alphabetically
    colored_text = ""
    current_index = 0
    subs_index = 0

    while subs_index < len(subs):
        start, substring, color = subs[subs_index]
        length = len(substring)

        # If the current index is less than the start of the substring, add the plain text until that point
        if current_index < start:
            colored_text += text[current_index:start]
            current_index = start

        # If the current index overlaps with the new substring, handle overlap
        if current_index >= start:
            overlap = current_index - start
            non_overlap_substring = substring[overlap:]  # Take the non-overlapping part of the substring

            # Add the colored non-overlapping part of the substring
            colored_text += color + non_overlap_substring + Style.RESET_ALL
            current_index += len(non_overlap_substring)

        subs_index += 1

    # Add any remaining plain text after the last colored substring
    if current_index < len(text):
        colored_text += text[current_index:]

    return colored_text




if __name__ == "__main__":
    main()
