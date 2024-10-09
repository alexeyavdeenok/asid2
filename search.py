import time

def log_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()  # Точнее замер начального времени
        result = func(*args, **kwargs)
        end_time = time.perf_counter()  # Точнее замер времени после выполнения
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' executed in {execution_time:.8f} seconds")
        return result
    return wrapper


@log_execution_time
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
    dictionary = get_first_n_occurrences(dictionary, count, method)
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


def make_table(substring):
    set_of_chars = set()  # Набор уникальных символов в подстроке
    len_substring = len(substring)  # Длина подстроки
    dictionary = {}  # Таблица смещений

    for i in range(len_substring - 2, -1, -1):  # Проходим по подстроке с предпоследнего символа
        if substring[i] not in set_of_chars:  # Если символ еще не был добавлен в таблицу смещений
            dictionary[substring[i]] = len_substring - i - 1
            set_of_chars.add(substring[i])

    if substring[len_substring - 1] not in set_of_chars:  # Отдельно обрабатываем последний символ подстроки
        dictionary[substring[len_substring - 1]] = len_substring

    dictionary['*'] = len_substring  # Смещение для всех остальных символов (которых нет в подстроке)
    return dictionary


def get_first_n_occurrences(substrings_dict, n, order='first'):
    # Шаг 1: Собираем все вхождения в виде списка с подстрокой и её индексом
    all_occurrences = []
    for substring, occurrences in substrings_dict.items():
        if occurrences is None:
            continue
        for index in occurrences:
            all_occurrences.append((substring, index))

    # Шаг 2: Сортируем в зависимости от порядка поиска
    if order == 'first':
        # Прямой поиск: сортируем по индексу, затем по подстроке
        all_occurrences.sort(key=lambda x: (x[1], x[0]))
    elif order == 'last':
        # Обратный поиск: сортируем сначала по убыванию индексов, затем по алфавиту
        all_occurrences.sort(key=lambda x: (-x[1], x[0]))
    else:
        raise ValueError("Order must be either 'first' or 'last'.")

    # Шаг 3: Оставляем только первые n вхождений
    selected_occurrences = all_occurrences[:n]

    # Шаг 4: Формируем новый словарь с теми же ключами
    result = {key: [] for key in substrings_dict}

    # Шаг 5: Заполняем словарь первыми вхождениями
    for substring, index in selected_occurrences:
        result[substring].append(index)

    # Шаг 6: Преобразуем значения в кортежи, как в исходных данных
    result = {key: tuple(value) if value else None for key, value in result.items()}

    return result

