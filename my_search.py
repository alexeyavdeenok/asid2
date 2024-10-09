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

# Пример использования:
substrings_dict4 = {'abc': (1,), 'a': (1,)}
substrings_dict1 = {'aba': (0, 5, 7), 'bba': None}
substrings_dict2 = {'aba': (7, 5, 0), 'bba': (3,)}
n = 5
print(get_first_n_occurrences(substrings_dict1, n, 'last'))