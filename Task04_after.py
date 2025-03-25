# 1. Имеется набор геометрических фигур разного цвета. Среди фигур могут встречаться круги, квадраты и отрезки.
# Для каждой фигуры известно, какого она цвета. Кроме того, для круга известен его радиус (тип int), для квадрата
# – размер стороны (тип int), для отрезка–длина (тип float). Написать функцию, позволяющую ввести с клавиатуры
# данные для одной фигуры. Используя эту функцию, ввести сведения об N фигурах и сохранить их в бинарном файле.
# Распечатать на экране содержимое данного файла в виде таблицы.
# Для решения использовать классы, обязательно наличие конструктора(ов),
# для вывода информации переопределить метод __str__()

import struct  # Импортируем модуль для работы с бинарными данными


# Базовый класс для всех фигур
class ShapeClass:
    def __init__(self, color):
        self.color = color

    def __str__(self):
        return f"Цвет: {self.color}"


# Класс для круга
class CircleClass(ShapeClass):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius

    def __str__(self):
        return f"Круг: {super().__str__()}, Радиус: {self.radius}"


# Класс для квадрата
class SquareClass(ShapeClass):
    def __init__(self, color, side):
        super().__init__(color)
        self.side = side

    def __str__(self):
        return f"Квадрат: {super().__str__()}, Сторона: {self.side}"


# Класс для отрезка
class LineClass(ShapeClass):
    def __init__(self, color, length):
        super().__init__(color)
        self.length = length

    def __str__(self):
        return f"Отрезок: {super().__str__()}, Длина: {self.length:.2f}"


# Функция для ввода данных о фигуре
def input_shape():
    # Запрашиваем у пользователя тип фигуры
    shape_type = input("Введите тип фигуры (круг, квадрат, отрезок): ").strip().lower()
    # Запрашиваем цвет фигуры
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


# Функция для сохранения фигур в бинарный файл
def save_shapes_to_file(shapes, filename):
    with open(filename, 'wb') as f:
        for shape in shapes:
            if isinstance(shape, CircleClass):
                f.write(struct.pack('i', 1))  # Записываем тип фигуры: круг (1)
                f.write(struct.pack('i', shape.radius))  # Записываем радиус
            elif isinstance(shape, SquareClass):
                f.write(struct.pack('i', 2))  # Записываем тип фигуры: квадрат (2)
                f.write(struct.pack('i', shape.side))  # Записываем длину стороны
            elif isinstance(shape, LineClass):
                f.write(struct.pack('i', 3))  # Записываем тип фигуры: отрезок (3)
                f.write(struct.pack('f', shape.length))  # Записываем длину отрезка
            # Записываем цвет фигуры как строку, заканчивающуюся нулевым байтом
            f.write(shape.color.encode('utf-8') + b'\x00')


# Функция для загрузки фигур из бинарного файла
def load_shapes_from_file(filename):
    shapes = []
    with open(filename, 'rb') as f:
        while True:
            type_bytes = f.read(4)  # Читаем 4 байта (тип фигуры)
            if not type_bytes:
                break
            shape_type = struct.unpack('i', type_bytes)[0]  # Преобразуем байты в число

            # В зависимости от типа фигуры читаем параметр
            if shape_type == 1:  # Круг
                radius = struct.unpack('i', f.read(4))[0]  # Читаем радиус
                color = b''
                while True:
                    byte = f.read(1)  # Читаем цвет посимвольно
                    if byte == b'\x00':  # Нулевой байт означает конец строки
                        break
                    color += byte
                color = color.decode('utf-8')  # Преобразуем байты в строку
                shapes.append(CircleClass(color, radius))
            elif shape_type == 2:  # Квадрат
                side = struct.unpack('i', f.read(4))[0]  # Читаем длину стороны
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(SquareClass(color, side))
            elif shape_type == 3:  # Отрезок
                length = struct.unpack('f', f.read(4))[0]  # Читаем длину отрезка
                color = b''
                while True:
                    byte = f.read(1)
                    if byte == b'\x00':
                        break
                    color += byte
                color = color.decode('utf-8')
                shapes.append(LineClass(color, length))
    return shapes


# Функция для вывода фигур в виде таблицы
def print_shapes_table(shapes):
    # Выводим заголовок таблицы
    print("{:<10} {:<10} {:<10}".format("Тип", "Цвет", "Параметр"))
    print("-" * 30)  # Разделитель
    for shape in shapes:
        # В зависимости от типа фигуры выводим информацию
        if isinstance(shape, CircleClass):
            print("{:<10} {:<10} {:<10}".format("Круг", shape.color, f"Радиус: {shape.radius}"))
        elif isinstance(shape, SquareClass):
            print("{:<10} {:<10} {:<10}".format("Квадрат", shape.color, f"Сторона: {shape.side}"))
        elif isinstance(shape, LineClass):
            print("{:<10} {:<10} {:<10}".format("Отрезок", shape.color, f"Длина: {shape.length:.2f}"))


# Основная часть программы
if __name__ == "__main__":
    try:
        N = int(input("Введите количество фигур: "))
    except ValueError:
        raise ValueError("Некорректный ввод")
    shapes = []
    for _ in range(N):
        shapes.append(input_shape())
    filename = "shapes.bin"  # Имя файла для сохранения данных
    save_shapes_to_file(shapes, filename)
    loaded_shapes = load_shapes_from_file(filename)
    print_shapes_table(loaded_shapes)
