from multiprocessing import Pool
import multiprocessing
from multiprocessing import Process
from itertools import repeat
from multiprocessing.spawn import freeze_support
from threading import Thread

class t:
    def __init__(self, x, y, resultados, i):
        resultados[i] = x**y

#with multiprocessing.Pool(processes=4) as pool:
#    resultados = pool.starmap(f, zip([3, 3, 3, 3], [4, 4, 4, 4]))

threads = [None] * 10
resultados = [None] * 10

for i in range(len(threads)):
    threads[i] = Thread(target=t, args=(2, i, resultados, i))
    threads[i].start()
    threads[i].join()

for i in range(len(threads)):
    threads[i].join()

print(resultados)