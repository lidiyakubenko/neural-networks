from PIL import Image

numbers = [1, 2, 3, 4, 5, 6]
entry_numbers = [1, 3, 5]

img_height = 99
img_width = 99


def common_func(px):
    vector = []
    for i in range(img_height):

        for j in range(img_width):
            value = px[j, i][0]
            vector.append(1 if value < 100 else 0)

    return vector


def get_vectors_from_images():
    vectors = []

    for num in numbers:
        with Image.open('./images/numbers/' + str(num) + '.png') as im:
            px = im.load()

        v = common_func(px)
        vectors.append(v)

    return vectors


def get_entry_instance(num):
    with Image.open('./images/numbers/' + str(num) + '_entry.png') as im:
        px = im.load()
    v = common_func(px)

    return v


instances = get_vectors_from_images()

entry_instance1 = get_entry_instance(1)
entry_instance3 = get_entry_instance(3)
entry_instance5 = get_entry_instance(5)
