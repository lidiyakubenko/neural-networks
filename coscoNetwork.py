from functools import reduce
import numpy as np
from PIL import Image
from instances import entry_instance1, entry_instance3, entry_instance5

# нейронная сеть коско
# гетероассоциативная память

# каждый вектор ассоциирован с другим вектором
# x - вектор входного образца
# y - натуральные числа в двоичной записи переведенные в биполярную кодировку
# 1 => 001 => [-1, -1, 1]

numbers_list = [
    [-1, -1, 1],
    [-1, 1, -1],
    [-1, 1, 1],
    [1, -1, -1],
    [1, -1, 1],
    [1, 1, -1]
]


def common_func(px):
    vector = []
    for i in range(99):

        for j in range(99):
            value = px[j, i][0]
            vector.append(1 if value < 100 else 0)

    return vector


def get_vectors_from_images():
    vectors = []

    for index in range(len(numbers_list)):
        with Image.open('./images/numbers/' + str(index + 1) + '.png') as im:
            px = im.load()

        v = common_func(px)
        vectors.append({'x': v, 'y': numbers_list[index]})

    return vectors


# instances = [
#     {'x': [1, -1, 1, -1], 'y': [-1, -1, 1]},  # x1
#     {'x': [-1, 1, -1, 1], 'y': [-1, 1, -1]},  # x1
#     {'x': [-1, -1, 1, 1], 'y': [-1, 1, 1]},  # x1
# ]

instances = get_vectors_from_images()

# необходимо узнать с каким натуральным числом ассоциирован входящий образец
# entry_instance_x = [1, -1, 1, 1]
entry_instance_y1 = [1, 1, 1]  # 7
entry_instance_y2 = [-1, -1, 1]

text_file = open("test.txt", "w")


# транспонированный вектор y умножаем на вектор x
def get_matrix_from_instance(x, y):
    matrix = []

    for valY in y:
        matrix.append([valX * valY for valX in x])

    return np.array(matrix)


def get_all_matrices(instances_list):
    return [get_matrix_from_instance(v['x'], v['y']) for v in instances_list]


def get_main_matrix(instances_list):
    return reduce(lambda m1, m2: m1 + m2, get_all_matrices(instances_list))


matrix_W = get_main_matrix(instances)
print('Получили матрицу')


# умножаем матрицу на вектор входящего образца
def multiply_matrix_by_instance(matrix, vector):
    a = matrix
    b = np.array([vector]).T
    return a.dot(b)


# активационная функция
def activation_func(vector):
    return list(map(lambda x: -1 if x[0] < 0 else 1, vector))


# сравниваем с образцами в памяти
def compare_result_with_instances(vector, instances_list, entry_type):
    is_equal = False

    for index in range(len(instances_list)):
        instance = instances_list[index]['x' if entry_type == 'y' else 'y']

        if np.array_equal(vector, instance):
            is_equal = True
            print('Успех! ' + str(vector) + ' = #' + str(index + 1))
            break

    return is_equal


def iterating_to_result(matrix, entry_instance, entry_type, counter=5):
    counter = counter - 1
    vector = multiply_matrix_by_instance(matrix, entry_instance)
    activated_vector = activation_func(vector)
    is_equal = compare_result_with_instances(activated_vector, instances, entry_type)

    e_type = 'y' if entry_type == 'x' else 'x'
    m = matrix.T

    if counter < 0 and not is_equal:
        print('не удалось вычислить образец')
        return
    if not is_equal:
        iterating_to_result(m, activated_vector, e_type, counter)


iterating_to_result(matrix_W, entry_instance1, 'x')
iterating_to_result(matrix_W, entry_instance3, 'x')
iterating_to_result(matrix_W, entry_instance5, 'x')

iterating_to_result(matrix_W.T, entry_instance_y1, 'y')
iterating_to_result(matrix_W.T, entry_instance_y2, 'y')