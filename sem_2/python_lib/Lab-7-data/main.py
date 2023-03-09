import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def start():
    arr = np.array([5, 9, 10, 'ad', 7])
    arr = arr[::-1]
    print(arr)


def tableLoad():
    arr = np.genfromtxt('voltage.csv', delimiter=',')
    time = arr[:100,0]
    time = time[:,np.newaxis]
    curr = arr[:100,1]
    curr = curr[:,np.newaxis]
    volt = arr[:100,2]
    volt = volt[:,np.newaxis]

    plt.plot(time, curr * 50, 'b', time, volt, 'r')
    plt.show()


def hist():
    arr = np.genfromtxt('test.csv', delimiter=',')
    arr = arr[1:]
    daysInYear = 365.25

    age = np.int_(arr[:,1] / daysInYear)

    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    ax.hist(age, 100, (50, 60))
    ax.grid()
    plt.show()


def plot3d():
    np.random.seed(40)
    xs = np.linspace(0, 10, 20)
    ys = xs
    zs = np.sin(xs)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xs, ys, zs, marker='x', c='red')
    plt.show()


if __name__ == '__main__':
    start()
    #tableLoad()
    #hist()
    #plot3d()