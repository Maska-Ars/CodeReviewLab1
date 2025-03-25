'''Дан файл целых чисел. Удвоить его размер, записав
в конец файла все его исходные элементы
(в обратном порядке)'''

import struct

# fixme перед функцией отсутствуют 2 пустые строки
#создаем файл и записываем в него числа
def create_file(filename):
    numbers = input("Введите целые числа через пробел: ")
    # fixme отсутствует обработка некорректного ввода
    numbers_list = list(map(int, numbers.split()))
    with open(filename, 'wb') as f:
        for number in numbers_list:
            f.write(struct.pack('i', number))  # запись целого числа в бинарном формате


def double_file_size(filename):
    # чтение всех чисел из файла
    numbers = []
    with open(filename, "rb") as f:
        while True:
            data = f.read(4)  # читаем 4 байта (int)
            # fixme очевидный комментарий
            if not data: #если строка пустая(конец файла)
                break
            number = struct.unpack("i", data)[0]  # преобразуем байты в целое число
            numbers.append(number)

    # запись элементов в обратном порядке в конец файла
    # fixme очевидный комментарий
    with open(filename, "ab") as f:  # открываем файл для добавления
        for i in range(len(numbers) - 1, -1, -1):
            number = numbers[i]
            data = struct.pack("i", number)  # преобразуем целое число обратно в байты
            # fixme очевидный комментарий
            f.write(data)  # записываем байты в файл

    print("Файл успешно удвоен.")

# fixme перед функцией отсутствуют 2 пустые строки
# fixme название функции не отражает её назначение
#вывод содержимого файла на экран
def open_file(filename):
    numbers = []
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(4)  # чтение 4 байт
            if not bytes_read:
                break
            number = struct.unpack('i', bytes_read)[0]
            # fixme очевидный комментарий
            numbers.append(str(number))  # преобразуем число в строку и добавляем в список
    # fixme очевидный комментарий
    print(" ".join(numbers))  # объединяем числа в строку и выводим


filename = 'laba14n3.bin'
create_file(filename)
double_file_size(filename)
print("Содержимое файла после удвоения:")
open_file(filename)
