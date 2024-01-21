import os


def load_level(filename, pos_x, pos_y) -> list:
    """
    Читаем уровень, убирая символы перевода строки и подсчитываем максимальную длину
    дополняем каждую строку пустыми клетками (".").
    """
    filename = os.path.join('data', 'levels', filename)

    with open(filename, 'r') as map_file:
        map_file = tuple(map_file)
        start_point = tuple(map(int, map_file[0].split()))
        finish_point = tuple(map(int, map_file[1].split()))
        level_map = [line.strip() for line in map_file[2:]]

    max_width = max(map(len, level_map))

    result_list = list(map(lambda x: x.ljust(max_width, '.'), level_map))  # Яндекс возвращал это

    delta_x = start_point[0] - pos_x

    for _ in range(abs(delta_x)):
        for i in range(len(result_list)):
            if delta_x >= 0:
                result_list[i] = result_list[i][1:] + result_list[i][0]
            else:
                result_list[i] = result_list[i][-1] + result_list[i][:-1]

    delta_y = start_point[1] - pos_y
    for _ in range(abs(delta_y)):
        if delta_y >= 0:
            result_list = result_list[1:] + [result_list[0]]
        else:
            result_list = [result_list[-1]] + result_list[:-1]

    return result_list
