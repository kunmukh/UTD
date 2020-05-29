#!/usr/bin/env python3.6

# Kunal Mukherjee
# 5/29/20
# Utility to measure
# 1> CPU usage
# 2> Virtual Memory usage
# 3> Data Received
# 4> Data Sent

# import statement
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math
import psutil
import csv

# black background
style.use('dark_background')
# create the figure
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

xs = [0.]
ys1, ys2, ys3, ys4 = {}, {}, {}, {}

PID = []
PID_str = ""


# add the label and title
def addInfoPlot():
    # create the sub plot
    ax1.set_title('CPU Usage')
    ax2.set_title('Virtual Memory Usage')
    ax3.set_title('Data Received')
    ax4.set_title('Data Sent')

    ax1.set_ylabel('%')
    ax2.set_ylabel('bytes')
    ax3.set_ylabel('test')
    ax4.set_ylabel('test')

    ax1.set_xlabel('sec')
    ax2.set_xlabel('sec')
    ax3.set_xlabel('sec')
    ax4.set_xlabel('sec')

    fig.tight_layout()


# save the figure
def saveFig():
    plt.savefig('Plot/'+PID_str + ".png")


# save the Data
def saveData():
    with open('Data/'+PID_str+'.csv', "w") as f:
        fw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for p in PID:
            for cpu, mem in zip(ys1[p], ys2[p]):
                fw.writerow([p, cpu, mem])


# function to animate
def animate(interval):
    global xs, ys1, ys2
    try:
        for pid in PID:
            p = psutil.Process(pid)

            ys1[pid].append(p.cpu_percent(0.1) / psutil.cpu_count())
            ys2[pid].append(p.memory_info().rss)
        xs.append(xs[-1] + 1)

    except psutil.NoSuchProcess:
        saveFig()
        saveData()
        exit()

    # slear the subplot
    ax1.clear()
    ax2.clear()
    # add the new subplot
    for pid in PID:
        ax1.plot(xs, ys1[pid], label=PID_str)
        ax2.plot(xs, ys2[pid], label=PID_str)

    addInfoPlot()


# main driver function
def main():

    global PID, PID_str, ys1, ys2, ys3, ys4

    print('Enter the process PID')
    PID_str = input()
    PID = PID_str.split(',')
    PID = [int(i) for i in PID]

    for pid in PID:
        ys1.update({pid: [0.]})
        ys2.update({pid: [0.]})
        ys3.update({pid: [0.]})
        ys4.update({pid: [0.]})

    print(ys1, ys2, ys3, ys4)

    while True:
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        plt.show()


if __name__ == '__main__':
    main()