def search(string, sub_string, case_sensitivity, method, count):
    if isinstance(sub_string, str):
        sub_string = [sub_string]  # Приводим подстроки к списку, если это одна строка
    if not case_sensitivity:  # Если регистр не важен, приводим строку и подстроки к нижнему регистру
        sub_string = [i.lower() for i in sub_string]
        string = string.lower()

    list_of_subs = []
    for i in sub_string:
        list_of_subs.append(make_table(i))  # Строим таблицу смещений для каждой подстроки

    list_of_finds = []
    if method == 'first':
        for i in range(len(sub_string)):
            list_of_finds.append(
                boyer_moore_horspool(string, sub_string[i], list_of_subs[i], count))  # Ищем каждую подстроку
    else:
        for i in range(len(sub_string)):
            list_of_finds.append(
                search_from_end(string, sub_string[i], count))  # Ищем каждую подстроку

    if len(list_of_finds) == 1:
        return list_of_finds[0]  # Если одна подстрока, возвращаем результат поиска напрямую

    # Возвращаем словарь с результатами для всех подстрок
    if all(i is None for i in list_of_finds):
        return None
    dictionary = {}
    for i in range(len(list_of_finds)):
        dictionary[sub_string[i]] = list_of_finds[i]
    return dictionary


def boyer_moore_horspool(text: str, pattern: str, shift_dict: dict, count: int):
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
        # Сравниваем подстроку с конца
        j = len_pattern - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        # Если все символы совпали, сохраняем индекс
        if j == -1:
            indices.append(i)
            count1 += 1
            if count == count1:
                return tuple(indices)
            i += 1  # Смещаем на 1 символ вперед после нахождения подстроки
        else:
            # Используем таблицу смещений для пропуска ненужных символов
            shift = shift_dict.get(text[i + len_pattern - 1], len_pattern)
            i += shift

    if len(indices) == 0:
        return None
    return tuple(indices)


def search_from_end(text: str, pattern: str, count: int):
    """Ищет все вхождения подстроки pattern в строке text с конца текста."""
    len_text = len(text)
    len_pattern = len(pattern)

    # Если подстрока длиннее текста, искать нечего
    if len_pattern > len_text:
        return None

    # Построение таблицы смещений
    shift_dict = build_shift_table(pattern)

    count1 = 0
    indices = []

    # Начинаем с конца текста
    i = len_text - len_pattern
    while i >= 0:
        # Сравниваем символы с начала подстроки, но двигаемся по тексту справа налево
        j = 0
        while j < len_pattern and pattern[j] == text[i + j]:
            j += 1

        if j == len_pattern:  # Если вся подстрока совпала
            indices.append(i)
            count1 += 1
            if count == count1:
                return tuple(indices)
            i -= 1  # Смещаемся на 1 символ влево после нахождения совпадения
        else:
            # Используем таблицу смещений для пропуска ненужных символов
            shift = shift_dict.get(text[i], len_pattern)
            i -= shift

    if len(indices) == 0:
        return None
    return tuple(indices)


def build_shift_table(pattern: str) -> dict:
    """
    Создает таблицу смещений для подстроки, смещения строятся зеркально, относительно последнего символа.
    """
    set_pattern = set()  # Набор уникальных символов в подстроке
    len_pattern = len(pattern)  # Длина подстроки
    d = {}  # Таблица смещений

    for i in range(1, len_pattern):  # Проходим по подстроке с предпоследнего символа
        if pattern[i] not in set_pattern:  # Если символ еще не был добавлен в таблицу смещений
            d[pattern[i]] = i
            set_pattern.add(pattern[i])

    if pattern[0] not in set_pattern:  # Отдельно обрабатываем последний символ подстроки
        d[pattern[0]] = len_pattern

    d['*'] = len_pattern  # Смещение для всех остальных символов (которых нет в подстроке)
    return d


def make_table(t):
    S = set()  # Набор уникальных символов в подстроке
    M = len(t)  # Длина подстроки
    d = {}  # Таблица смещений

    for i in range(M - 2, -1, -1):  # Проходим по подстроке с предпоследнего символа
        if t[i] not in S:  # Если символ еще не был добавлен в таблицу смещений
            d[t[i]] = M - i - 1
            S.add(t[i])

    if t[M - 1] not in S:  # Отдельно обрабатываем последний символ подстроки
        d[t[M - 1]] = M

    d['*'] = M  # Смещение для всех остальных символов (которых нет в подстроке)
    return d

print(search('abc', ('abc', 'a'), False, 'first', 1))