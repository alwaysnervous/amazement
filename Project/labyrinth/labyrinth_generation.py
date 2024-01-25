import random
import os


class Labyrinth:
    def __init__(self, n, m):
        self.n = (n + 2) // 2
        self.m = (m + 2) // 2

    def start_point_generate(self):
        """Функция выбора точки начала лабиринта"""
        if random.choice([True, False]):
            if random.choice([True, False]):
                start_point = (0, random.randint(0, self.m - 1))
            else:
                start_point = (self.n - 1, random.randint(0, self.m - 1))
        else:
            if random.choice([True, False]):
                start_point = (random.randint(0, self.n - 1), 0)
            else:
                start_point = (random.randint(0, self.n - 1), self.m - 1)
        return start_point

    def finish_point_generate(self):
        """Выбор точки конца лабиринта"""
        start_point = self.start_point_generate()
        return self.n - 1 - start_point[0], self.m - 1 - start_point[1]

    @staticmethod
    def transition_choice(x, y, rm):
        """Функция выбора дальнейшего пути в генерации лабиринта"""
        choice_list = []
        if x > 0:
            if not rm[x - 1][y]:
                choice_list.append((x - 1, y))
        if x < len(rm) - 1:
            if not rm[x + 1][y]:
                choice_list.append((x + 1, y))
        if y > 0:
            if not rm[x][y - 1]:
                choice_list.append((x, y - 1))
        if y < len(rm[0]) - 1:
            if not rm[x][y + 1]:
                choice_list.append((x, y + 1))
        if choice_list:
            nx, ny = random.choice(choice_list)
            if x == nx:
                if ny > y:
                    tx, ty = x * 2, ny * 2 - 1
                else:
                    tx, ty = x * 2, ny * 2 + 1
            else:
                if nx > x:
                    tx, ty = nx * 2 - 1, y * 2
                else:
                    tx, ty = nx * 2 + 1, y * 2
            return nx, ny, tx, ty
        else:
            return -1, -1, -1, -1

    def create_labyrinth(self):
        """Генерация лабиринта"""
        reach_matrix = []
        for i in range(self.n):  # создаём матрицу достижимости ячеек
            reach_matrix.append([])
            for j in range(self.m):
                reach_matrix[i].append(False)
        transition_matrix = []
        for i in range(self.n * 2 - 1):  # заполнение матрицы переходов
            transition_matrix.append([])
            for j in range(self.m * 2 - 1):
                if i % 2 == 0 and j % 2 == 0:
                    transition_matrix[i].append(True)
                else:
                    transition_matrix[i].append(False)
        start_point = self.start_point_generate()
        finish_point = self.finish_point_generate()
        list_transition = [start_point]
        x, y = start_point
        reach_matrix[x][y] = True
        x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
        for i in range(1, self.m * self.n):
            while not (x >= 0 and y >= 0):
                x, y = list_transition[-1]
                list_transition.pop()
                x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
            reach_matrix[x][y] = True
            list_transition.append((x, y))
            transition_matrix[tx][ty] = True
            x, y, tx, ty = self.transition_choice(x, y, reach_matrix)
        return transition_matrix, start_point, finish_point  # возвращаем матрицу проходов и начальную точку


def level_view_of_the_matrix(matrix_and_points: [list, tuple, tuple]):
    character_sign = '@'
    wall_sign = '#'
    empty_sign = '.'
    finish_sign = '~'

    def replace_random_dots(s: str, replacement: str = 'c', num_replacements: int = 1) -> str:
        s = list(s)
        dot_indices = [i for i, char in enumerate(s) if char == '.']
        random.shuffle(dot_indices)
        for i in dot_indices[:num_replacements]:
            s[i] = replacement
        return ''.join(s)

    # Приведение матрицы в игровой вид
    matrix, start, finish = matrix_and_points
    matrix = [[empty_sign if cell else wall_sign for cell in row] for row in matrix]
    matrix[start[1]][start[0]] = character_sign
    matrix[finish[1]][finish[0]] = finish_sign

    with open(os.path.join('data', 'levels', 'map_generated.txt'), 'w') as map_file:
        print(start[0] + 1, start[1] + 1, file=map_file)
        print(finish[0] + 1, finish[1] + 1, file=map_file)
        print('#' * (len(matrix[0]) + 1), file=map_file)
        for row in matrix:
            print('#', replace_random_dots(''.join(row), 'c', len(matrix[0]) // 7), sep='', file=map_file)


# labyrinth_new = Labyrinth(20, 20)
# level_view_of_the_matrix(labyrinth_new.create_labyrinth())
