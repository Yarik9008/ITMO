import sys


# функция перевода строки в байтовую
def bit_string_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')

# функция перевода байтовой строки в обычную строку
def bytes_to_bit_string(bytess):
    return bin(int.from_bytes(bytess, 'big')).split('b')[1]

# Функция для кодировки с помощью алгоритма хаффмана
def encode_huffman(path_input: str, path_output: str):
    mass_key = {}
    # рекурсивная функция которая позволяет преобразовать расположение элементов в массиве в их кодировку
    # по сути пробегается по дереву и записывает путь

    def _list_perser(listik, path=''):
        if isinstance(listik[0], list):
            _list_perser(listik[0], path + '0')
        else:
            mass_key[listik[0]] = path + '0'

        if isinstance(listik[1], list):
            _list_perser(listik[1], path + '1')
        else:
            mass_key[listik[1]] = path + '1'

    with open(path_input) as file_in:
        # читаем весь файл
        data = list(file_in.read())
        # считаем сколько раз встречается каджый элемент и сортируем по количеству
        mass_sim = sorted([[i, data.count(i)]
                          for i in set(data)], key=lambda col: col[1])
        mass_dict = mass_sim[::1]
        # составляем дерево в виде списков в списке
        while len(mass_sim) != 2:
            one = mass_sim[0][0]
            two = mass_sim[1][0]
            counter = mass_sim[0][1] + mass_sim[1][1]
            element = [[one, two], counter]
            mass_sim.append(element)
            mass_sim = sorted(mass_sim[2:], key=lambda col: col[1])
        # после последнего прохода удаляем количество встреч суммы массивов элементов первого и второго
        for i in range(len(mass_sim)):
            mass_sim[i] = mass_sim[i][0]

    # генерируем словарь ключей
    _list_perser(mass_sim)

    # генерируем конечную закодированную поледовательность и добовляем незначущую еденицу в начало строки для сохренения нулей
    out_data = bit_string_to_bytes('1' + ''.join([mass_key[i] for i in data]))

    with open(path_output, 'w', encoding='utf-8') as file_out:
        # колличество
        file_out.write((str(len(mass_key.keys())) + '\n'))
        # запись словоря
        for i in range(len(mass_dict)):
            sim = mass_dict[i][0]
            n = mass_dict[i][1]
            if sim != '\n':
                file_out.write((f'{sim}{n}\n'))
            else:
                file_out.write((f'/n{n}\n'))

    # записываем в файл байтовую закодированную строку
    with open(path_output, 'ab') as file_out:
        file_out.write(out_data)


# Функция для декодировки с помощью алгоритма хаффмана
def decode_huffman(path_input: str, path_output: str):

    mass_key = {}

    # рекурсивная функция которая позволяет преобразовать расположение элементов в массиве в их кодировку
    # по сути пробегается по дереву и записывает путь
    def _list_perser(listik, path=''):
        if isinstance(listik[0], list):
            _list_perser(listik[0], path + '0')
        else:
            mass_key[listik[0]] = path + '0'

        if isinstance(listik[1], list):
            _list_perser(listik[1], path + '1')
        else:
            mass_key[listik[1]] = path + '1'

    # читаем весь закодированный файл
    with open(path_input, 'rb') as file_in:
        data = file_in.readlines()

        mass_sim = []
        kol = int(str(data[0])[2:-5])

        data = data[1:]

        # преобразуем бинарную запись в строку
        text_in = bytes_to_bit_string(data[-1])[1:]

        # парсим словарик
        for i in range(kol):
            if '/n' in str(data[i]):
                sim, code = '\n', int(str(data[i])[4:-5])
            else:
                sim, code = str(data[i])[2:-5][0], int(str(data[i])[3:-5])
            mass_sim.append([sim, code])

        mass_sim = sorted(mass_sim, key=lambda col: col[1])

        # составляем дерево в виде списков в списке
        while len(mass_sim) != 2:
            one = mass_sim[0][0]
            two = mass_sim[1][0]
            counter = mass_sim[0][1] + mass_sim[1][1]
            element = [[one, two], counter]
            mass_sim.append(element)
            mass_sim = sorted(mass_sim[2:], key=lambda col: col[1])
            # после последнего прохода удаляем количество встреч суммы массивов элементов первого и второго
        for i in range(len(mass_sim)):
            mass_sim[i] = mass_sim[i][0]

        _list_perser(mass_sim)

        # преобразуем из словаря в массив
        mass_code = []
        for i in mass_key.keys():
            mass_code.append([i, mass_key[i]])

    text_out = ''

    # декодирование
    while len(text_in) != 0:
        for i in mass_code:
            if i[1] == text_in[:len(i[1])]:
                text_out += i[0]
                text_in = text_in[len(i[1]):]

    # запись в файл
    with open(path_output, 'w', encoding='utf-8') as file_out:
        file_out.write(text_out)


if __name__ == '__main__':
    # проверка на количество прописанных аргументов
    if len(sys.argv) == 4:
        # блок проверки параметров переданных при запуске программы на корректность
        if sys.argv[1] == '--encode':
            # проверка на корректность формата входного и выходного файла
            if sys.argv[2][-4:] == '.txt' and sys.argv[3][-4:] == '.txt':
                try:
                    # кодирование переданного файла
                    encode_huffman(sys.argv[2], sys.argv[3])
                    print("\033[92m{}\033[00m" .format(
                        'INFO: Successfully encode'))
                except:
                    print("\033[91m {}\033[00m" .format(
                        'ERROR ENCODE: Falled encoding'))
            else:
                print("\033[91m{}\033[00m" .format(
                    'ERROR INPUT: Wrong file format'))
        # блоке запуска функции декодирования реализованны аналогичные проверки с функцией кодирования
        elif sys.argv[1] == '--decode':
            if sys.argv[2][-4:] == '.txt' and sys.argv[3][-4:] == '.txt':
                try:
                    decode_huffman(sys.argv[2], sys.argv[3])
                    print("\033[92m{}\033[00m" .format(
                        'INFO: Successfully decode'))
                except:
                    print("\033[91m{}\033[00m" .format(
                        'ERROR Decode: Falled decoding'))
            else:
                print("\033[91m{}\033[00m" .format(
                    'ERROR INPUT: wrong file format'))
        # если функция переданная при запуске не найдена иили введена ошибочно
        else:
            print("\033[91m{}\033[00m" .format(
                'ERROR INPUT: invalid function'))
    else:
        print("\033[91m{}\033[00m" .format(
            'ERROR INPUT: invalid number of arguments'))
