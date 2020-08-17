import os
import psutil
import numpy as np

def foo():
    i = 100

    while True:
        i *= 10050505
        p = psutil.Process(os.getpid())
        print(p.cpu_percent(interval=0.1))
        print(p.memory_info().rss)


if __name__ == '__main__':
    print('PID: ',  os.getpid())
    input()
    foo()