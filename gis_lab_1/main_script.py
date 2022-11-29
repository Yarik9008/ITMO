import sys


# массив символов и их кодировок 
mass_key = {}

# рекурсивная функция которая позволяет преобразовать расположение элементов в массиве в их кодировку
# по сути пробегается по дереву и записывает путь 
def _list_perser(listik, path=''):
    if isinstance(listik[0], list):
        _list_perser(listik[0],path + '0')
    else:
        mass_key[listik[0]] = path + '0'
        
    if isinstance(listik[1], list):
        _list_perser(listik[1], path + '1')
    else: 
        mass_key[listik[1]] = path + '1'
    

def encode_huffman(path_input:str, path_output:str):
    with open(path_input, encoding='utf 8') as file:
        # читаем весь файл 
        data = list(file.read())
        # считаем сколько раз встречается каджый элемент и сортируем по количеству 
        mass_sim = sorted([[i,data.count(i)] for i in set(data)], key=lambda col: col[1])
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
    
    out_data = ''.join([mass_key[i] for i in data]).encode()
    
    
    # не совсем понял момент с записью в бинарном виде если надо как то по другому то велком 
    with open(path_output, 'rb+') as file_out:
        file_out.write((str(len(mass_key.keys())) + '\n').encode())
        file_out.write((str(mass_key)+ '\n').encode())
        file_out.write(out_data)
        
    
def decode_huffman(path_input:str, path_output:str):
    pass


#encode_huffman('C:/Users/Yarik/Documents/ITMO_1/gis_lab_1/input_file.txt', '')


if __name__ == '__main__':
    # проверка на количество прописанных аргументов 
    if len(sys.argv) == 4:
        # блок проверки параметров переданных при запуске программы на корректность 
        if sys.argv[1] == '--encode':
            # проверка на корректность формата входного и выходного файла 
            if sys.argv[2][-4:] == '.txt' and sys.argv[3][-4:] == '.txt':
                #try:
                    # кодирование переданного файла
                    encode_huffman(sys.argv[2], sys.argv[3])
                    print("\033[92m{}\033[00m" .format('INFO: Successfully encode'))
                #except:
                    #print("\033[91m {}\033[00m" .format('ERROR ENCODE: Falled encoding'))
            else:
                print("\033[91m{}\033[00m" .format('ERROR INPUT: Wrong file format'))
        # блоке запуска функции декодирования реализованны аналогичные проверки с функцией кодирования 
        elif sys.argv[1] == '--decode':
            if sys.argv[2][-4:] == '.txt' and sys.argv[3][-4:] == '.txt':
                try:
                    decode_huffman(sys.argv[2], sys.argv[3])
                    print("\033[92m{}\033[00m" .format('INFO: Successfully decode'))
                except:
                    print("\033[91m{}\033[00m" .format('ERROR ENCODE: Falled decoding'))
            else:
                print("\033[91m{}\033[00m" .format('ERROR INPUT: wrong file format'))
        # если функция переданная при запуске не найдена иили введена ошибочно
        else:
            print("\033[91m{}\033[00m" .format('ERROR INPUT: invalid function'))
    else:
        print("\033[91m{}\033[00m" .format('ERROR INPUT: invalid number of arguments'))

