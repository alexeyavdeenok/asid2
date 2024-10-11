"""
Модуль реализует функцию поиска подстроки в строке,
используя алгоритм Бойера-Мура-Хорспула
"""


def search(string, sub_string, case_sensitivity, method, count):
    """
    Функция соединяет в себе все фугкции для поиска подстроки в строке
    :param string: Строка, в которой ведется поиск
    :param sub_string: Одна или несколько подстрок
    :param case_sensitivity: Чувствительность к регистру
    :param method: Поиск с начала или с конца строки
    :param count: Количество совпадений
    :return: None или словарь с индексами или кортеж с индексами
    """
    if isinstance(sub_string, str):
        sub_string = [sub_string]
    if not case_sensitivity:
        sub_string = [i.lower() for i in sub_string]
        string = string.lower()

    list_of_subs = []
    for i in sub_string:
        list_of_subs.append(make_table(i))

    list_of_finds = []
    if method == 'first':
        for i in range(len(sub_string)):
            list_of_finds.append(
                boyer_moore_horspool(string, sub_string[i],
                                     list_of_subs[i], count))
    else:
        for i in range(len(sub_string)):
            list_of_finds.append(
                search_from_end(string, sub_string[i], count))

    if len(list_of_finds) == 1:
        return list_of_finds[0]

    if all(i is None for i in list_of_finds):
        return None
    dictionary = {}
    for i in range(len(list_of_finds)):
        dictionary[sub_string[i]] = list_of_finds[i]
    dictionary = get_first_n_occurrences(dictionary, count, method)
    return dictionary


def boyer_moore_horspool(text, pattern, shift_dict, count):
    """
    Реализует алгоритм Бойера-Мура-Хорспула для поиска подстроки в строке.

    :param text: Исходная строка, в которой ищется подстрока.
    :param pattern: Подстрока, которую необходимо найти.
    :param shift_dict: Словарь со смещениями для символов.
    :param count: Количество вхождений которое необходимо найти
    :return: Кортеж с индексами вхождений подстроки в строке.
    """
    len_text = len(text)
    len_pattern = len(pattern)
    count1 = 0
    if len_pattern > len_text:
        return None

    indices = []
    i = 0

    while i <= len_text - len_pattern:
        j = len_pattern - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j == -1:
            indices.append(i)
            count1 += 1
            if count == count1:
                return tuple(indices)
            i += 1
        else:
            shift = shift_dict.get(text[i + len_pattern - 1],
                                   len_pattern)
            i += shift

    if len(indices) == 0:
        return None
    return tuple(indices)


def search_from_end(text: str, pattern: str, count: int):
    """
    Функция для поиска подстрок с конца текста
    :param text: строка
    :param pattern: подстрока
    :param count: число вхождений
    :return: кортеж индексов вхождений
    """
    len_text = len(text)
    len_pattern = len(pattern)

    if len_pattern > len_text:
        return None

    shift_dict = build_shift_table(pattern)

    count1 = 0
    indices = []

    i = len_text - len_pattern
    while i >= 0:
        j = 0
        while j < len_pattern and pattern[j] == text[i + j]:
            j += 1

        if j == len_pattern:
            indices.append(i)
            count1 += 1
            if count == count1:
                return tuple(indices)
            i -= 1
        else:
            shift = shift_dict.get(text[i], len_pattern)
            i -= shift

    if len(indices) == 0:
        return None
    return tuple(indices)


def build_shift_table(pattern: str) -> dict:
    """
    Создание таблицы смещений для поиска с конца
    :param pattern: подстрока
    :return: таблица смещений (словарь)
    """
    set_pattern = set()
    len_pattern = len(pattern)
    dictionary = {}

    for i in range(1, len_pattern):
        if pattern[i] not in set_pattern:
            dictionary[pattern[i]] = i
            set_pattern.add(pattern[i])

    if pattern[0] not in set_pattern:
        dictionary[pattern[0]] = len_pattern

    dictionary['*'] = len_pattern
    return dictionary


def make_table(substring):
    """
    Таблица смещений для поиска с начала строки
    :param substring: подсторка
    :return: таблица смещений (словарь)
    """
    set_of_chars = set()
    len_substring = len(substring)
    dictionary = {}

    for i in range(len_substring - 2, -1, -1):
        if substring[i] not in set_of_chars:
            dictionary[substring[i]] = len_substring - i - 1
            set_of_chars.add(substring[i])

    if substring[len_substring - 1] not in set_of_chars:
        dictionary[substring[len_substring - 1]] = len_substring

    dictionary['*'] = len_substring
    return dictionary


def get_first_n_occurrences(substrings_dict, num, order='first'):
    """
    Получает словарь со всеми вхождениями и оставляет только первые n
    :param substrings_dict: словарь вхождений подстрок в строку
    :param num: количество допустимых вхождений
    :param order: поиск с начала или с конца
    :return: словарь
    """
    all_occurrences = []
    for substring, occurrences in substrings_dict.items():
        if occurrences is None:
            continue
        for index in occurrences:
            all_occurrences.append((substring, index))

    if order == 'first':
        all_occurrences.sort(key=lambda x: (x[1], x[0]))
    elif order == 'last':
        all_occurrences.sort(key=lambda x: (-x[1], x[0]))
    else:
        raise ValueError("Order must be either 'first' or 'last'.")

    selected_occurrences = all_occurrences[:num]

    result = {key: [] for key in substrings_dict}

    for substring, index in selected_occurrences:
        result[substring].append(index)

    result = {key: tuple(value) if value else None
              for key, value in result.items()}

    return result
