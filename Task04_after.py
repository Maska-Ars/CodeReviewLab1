# 1. Имеется набор геометрических фигур разного цвета. Среди фигур могут встречаться круги, квадраты и отрезки.
# Для каждой фигуры известно, какого она цвета. Кроме того, для круга известен его радиус (тип int), для квадрата
# – размер стороны (тип int), для отрезка–длина (тип float). Написать функцию, позволяющую ввести с клавиатуры
# данные для одной фигуры. Используя эту функцию, ввести сведения об N фигурах и сохранить их в бинарном файле.
# Распечатать на экране содержимое данного файла в виде таблицы.
# Для решения использовать классы, обязательно наличие конструктора(ов),
# для вывода информации переопределить метод __str__()

import struct  # Импортируем модуль для работы с бинарными данными

NUMBER_OF_SHAPE_TYPE = {
    'Circle': 1,
    'Square': 2,
    'Line': 3
}


class ShapeClass:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"Цвет: {self.color}"


class CircleClass(ShapeClass):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def __str__(self):
        return f"Круг: {super().__str__()}, Радиус: {self.radius}"


class SquareClass(ShapeClass):
    def __init__(self, color, side):
        super().__init__(color)
        self.side = side

    def __str__(self):
        return f"Квадрат: {super().__str__()}, Сторона: {self.side}"


class LineClass(ShapeClass):
    def __init__(self, color, length):
        super().__init__(color)
        self.length = length

    def __str__(self):
        return f"Отрезок: {super().__str__()}, Длина: {self.length:.2f}"


def input_shape():
    shape_type = input("Введите тип фигуры (круг, квадрат, отрезок): ").strip().lower()
    color = input("Введите цвет фигуры: ").strip()

    # В зависимости от типа фигуры запрашиваем дополнительные параметры
    if shape_type == "круг":
        radius = int(input("Введите радиус круга: "))
        return CircleClass(color, radius)
    elif shape_type == "квадрат":
        side = int(input("Введите размер стороны квадрата: "))
        return SquareClass(color, side)
    elif shape_type == "отрезок":
        length = float(input("Введите длину отрезка: "))
        return LineClass(color, length)
    else:
        raise ValueError("Неизвестный тип фигуры")


def save_shapes_to_file(shapes, filename):
    with open(filename, 'wb') as f:
        for shape in shapes:
            if isinstance(shape, CircleClass):
                f.write(struct.pack('i', NUMBER_OF_SHAPE_TYPE['Circle']))
                f.write(struct.pack('i', shape.radius))
            elif isinstance(shape, SquareClass):
                f.write(struct.pack('i', NUMBER_OF_SHAPE_TYPE['Square']))
                f.write(struct.pack('i', shape.side))
            elif isinstance(shape, LineClass):
                f.write(struct.pack('i', NUMBER_OF_SHAPE_TYPE['Line']))
                f.write(struct.pack('f', shape.length))
            # Записываем цвет фигуры как строку, заканчивающуюся нулевым байтом,
            # чтобы при чтении возможно было определить конец строки
            f.write(shape.color.encode('utf-8') + b'\x00')


def load_shapes_from_file(filename):
    shapes = []
    with open(filename, 'rb') as f:
        while True:
            type_bytes = f.read(4)
            if not type_bytes:
                break
            shape_type = struct.unpack('i', type_bytes)[0]

            # В зависимости от типа фигуры читаем параметр
            if shape_type == NUMBER_OF_SHAPE_TYPE['Circle']:
                radius = struct.unpack('i', f.read(4))[0]
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(CircleClass(color, radius))

            elif shape_type == NUMBER_OF_SHAPE_TYPE['Square']:
                side = struct.unpack('i', f.read(4))[0]
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(SquareClass(color, side))

            elif shape_type == NUMBER_OF_SHAPE_TYPE['Line']:
                length = struct.unpack('f', f.read(4))[0]
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(LineClass(color, length))

    return shapes


if __name__ == "__main__":
    try:
        N = int(input("Введите количество фигур: "))
    except ValueError:
        raise ValueError("Некорректный ввод")

    shapes = []
    for _ in range(N):
        shapes.append(input_shape())

    file_name = input('Введите название файла для сохранения: ')
    save_shapes_to_file(shapes, file_name)

    loaded_shapes = load_shapes_from_file(file_name)
    for shape in loaded_shapes:
        print(shape)
