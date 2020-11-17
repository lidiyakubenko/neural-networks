from functools import reduce

# дискретная нейронная сеть хопфилда
# пример синхронной работы

instances = [
    [1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1],  # x1
    [-1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1],  # x2
    [-1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1]  # x3
]

# испорченные образцы
y1 = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
y2 = [-1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1]
y3 = [1, -1, 1, -1, -1, -1,  1, 1, 1, -1, -1, -1]


# каждый вектор транспонируем и умножаем на сам себя
def get_matrix_from_instance(v):
    matrix = []

    for index in range(len(v)):
        matrix.append([])

        for index2 in range(len(v)):
            matrix[index].append(v[index2] * v[index])

    return matrix


all_matrices = list(map(get_matrix_from_instance, instances))


# складываем все матрицы
def add_up_the_matrices(matrices):
    matrix = []

    for index in range(len(matrices)):
        if index == 0:
            matrix = matrices[index]
        else:
            for i1 in range(len(matrices[index])):
                for i2 in range(len(matrices[index][i1])):
                    matrix[i1][i2] = matrix[i1][i2] + matrices[index][i1][i2]

    return matrix


matrix_w = add_up_the_matrices(all_matrices)

# выводим полученную матрицу(W)
print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                 for row in matrix_w]))


# умножаем полученную матрицу(W) на вектор испорченного образца
def multiply_matrix_by_bad_instance(vector, counter):
    new_vector = []

    if counter == 10:
        print('Не соответствует ни одному образцу')
        return

    for i in range(len(matrix_w)):
        new_vector.append(0)

        for i2 in range(len(matrix_w[i])):
            new_vector[i] = new_vector[i] + (matrix_w[i][i2] * vector[i2])

    super_puper_vector = activation_func(new_vector)
    equal = compare_result_with_instances(super_puper_vector)

    if equal:
        return
    else:
        counter = counter + 1
        multiply_matrix_by_bad_instance(super_puper_vector, counter)


# передаем полученный вектр в активационную функцию
def activation_func(vector):
    return list(map(lambda x: -1 if x < 0 else 1, vector))


def compare_result_with_instances(vector):
    equal = None

    for i1 in range(len(instances)):
        val = list(map(lambda x, y: True if x == y else False, vector, instances[i1]))
        if False not in val:
            equal = True
            print(
                'образец #' + str(i1 + 1) + ': ' + str(instances[i1]) + ' равен входному образцу:' + str(y1))
            break

    return equal


multiply_matrix_by_bad_instance(y1, 0)
