# импортируем модуль для работы с движителем из модуля ev3dev.ev3
from ev3dev.ev3 import LargeMotor
# импортируем модуль работы с временем 
import time

# создаем экземпляр класса LargeMotor и указываем мотор outA
motorA = LargeMotor('outA')
# создаем список значений напряжения в процентах с движением вперед
voltages = [10, 15, 20, 25, 30, 35, 40, 45, 50]
# создаем список значений напряжения в процентах с движением назад
# voltages = [-10, -15, -20, -25, -30, -35, -40, -45, -50]
# создаем обработчик ошибок 
try:
    # с помощью цикла перебераем последоваетльно значения из списка 
    for vol in voltages:
        # создаем таймер 
        timeStart = time.time()
        # считываем начальную позицию мотора 
        startPos = motorA. position
        # создаем название файла с соответвующим значением напряжения
        name = "data" + str (vol)
        # создаем файл с указаным именем 
        file = open(name, "w")
        # создаем бесконечный цикл 
        while True:
            # получаем текущее время и вычитаем начальное тем самым узнаем сколько времени прошло 
            timeNow = time.time() - timeStart
            # подаем напряжение на мотор 
            motorA.run_direct(duty_cycle_sp = vol)
            # получаем текущую позицию и вычитаем стартовую тем самым узнаем на сколько изменилась позиция 
            pos = motorA. position - startPos
            # записываем в файл время позицию и скорость через пробел 
            file. write (str (timeNow) + " "+ str(pos) +" "+ str(motorA.speed) + "\n")
            # если с начала прошла секунда то считаем что мотор набрал полную скорость и останавливаем ее в выходим из цикла wile
            if timeNow > 1:
                motorA.run_direct (duty_cycle_sp = 0)
                break
        # закрываем файл
        file .close()
        # ждем 5 секунд чтбы мотор остановился 
        time.sleep(5)
# если в блоке try возникает исключение то возвращаем ошибку 
except Exception as e:
    raise e
# в конце программы в любом случае останавливаем мотор и закрываем файл 
finally:
    motorA.stop(stop_action = 'brake')
    file .close()
    