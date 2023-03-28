import time
import cv2


PATH_IMG = 'C:/Users/Yarik/Documents/ITMO/sem_2/python_lib/lab-8/lab-8-data/images/variant-8.jpg'


def task_1():
    # считываем изображение
    img = cv2.imread(PATH_IMG)
    res = img.shape
    # реализуем обработку ситуаций когда изображение меньше чем крадрат с размерами 400 на 400 
    if res[0] < 400 or res[1] < 400:
        return 'The resolution of the input image is less than (400, 400)'
    else:
        # вырезаем из массива NumPy нужную область из файла
        out_img = img[(img.shape[0] - 400) // 2: ((img.shape[0] - 400) // 2) + 400,
                    (img.shape[1] - 400) // 2: ((img.shape[1] - 400) // 2) + 400]
        # выводим откоректированное изображение для отладки
        cv2.imshow('image', out_img)
        # сохраняем полученное изображение
        cv2.imwrite('out_im_task_1.jpg', out_img)
        # закрываем окошко вывода
        cv2.waitKey(0)

def task_2():
    cap = cv2.VideoCapture(0)
    
    while True:
        result, frame = cap.read()
        if result:
            cv2.imshow('frame', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


if __name__ == '__main__':
    # реализания первого задания 
    #task_1()
    # реализация второго задания 
    task_2()
