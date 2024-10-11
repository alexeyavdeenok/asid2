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


def highlight_substrings(text, substring, color_code="\033[93m"):  # 93 - желтый
    # Получаем индексы всех вхождений подстроки
    def find_substring_indices(text, substring):
        indices = []
        start = 0
        while start < len(text):
            start = text.find(substring, start)
            if start == -1:
                break
            indices.append(start)
            start += len(substring)
        return indices

    indices = find_substring_indices(text, substring)
    if not indices:
        return text  # Если вхождений нет, возвращаем исходную строку

    highlighted_text = ""
    last_index = 0

    # Проходим по каждому индексу и выделяем цветом
    for index in indices:
        highlighted_text += text[last_index:index]  # Добавляем текст до подстроки
        highlighted_text += f"{color_code}{substring}\033[0m"  # Добавляем подстроку с цветом
        last_index = index + len(substring)

    highlighted_text += text[last_index:]  # Добавляем оставшуюся часть строки

    return highlighted_text


# Пример использования
input_text = "Это пример строки с повторяющейся подстрокой. Подстрока - это часть строки."
substring_to_highlight = "строк"
result = highlight_substrings(input_text, substring_to_highlight)
print(result)

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