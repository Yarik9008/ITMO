from random import sample

# путь до текстового файлика с названиями географических мест 
PATH = 'C:/Users/Yarik/Documents/ITMO_1/Random_Ira/name.txt'


def read_to_list(path: str):
    # функция парсинга файла с данными
    with open(path, encoding="utf8") as file:
        data_out = []
        for a in [i[:-1].strip() for i in file.readlines()]:
            if a != '':
                data_out.append(a)
        return data_out


def random_out(data: list, quantity: int):
    # функция выдачи заданного количество элементов их массива данных
    data = sample(data, quantity)
    str_out = ''
    for i in range(len(data)):
        name = data[i]
        i += 1
        str_out += f'{i}) {name}\n'
        i -= 1
    return str_out

# вывод в консоль заданного количества названий 
print(random_out(read_to_list(PATH), 10))
