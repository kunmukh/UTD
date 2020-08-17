#!/usr/bin/env python3.6

# Kunal Mukherjee
# 5/29/20
# Utility to measure
# 1> CPU usage
# 2> Virtual Memory usage
# 3> Data Receive- not added
# 4> Data Sent- not added

# import statement
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import math
import psutil
import csv
from collections import Counter
from scapy.all import sniff
from threading import Thread
import time
import sys
import os

# IP port to monitor
monitorIP = "127.0.0.1"

# black background
style.use('dark_background')
# create the figure
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1)

xs = [0.]
ys1, ys2 = {}, {}
ys3, ys4 = [], []

PID = []
PID_str = "00000"
pl = {}

# Create a Packet Counter
packet_counts_recv = Counter()
packet_counts_send = Counter()


# add the label and title
def addInfoPlot():
    # create the sub plot
    ax1.set_title('CPU Usage')
    ax2.set_title('Virtual Memory Usage')
    ax3.set_title('Data Sent')
    ax4.set_title('Data Received')

    ax1.set_ylabel('%')
    ax2.set_ylabel('bytes')
    ax3.set_ylabel('# of packets')
    ax4.set_ylabel('# of packets')

    ax1.set_xlabel('sec')
    ax2.set_xlabel('sec')
    ax3.set_xlabel('sec')
    ax4.set_xlabel('sec')

    ax1.legend([pl[PID[i]] for i in range(len(PID))], PID, loc="upper right")
    ax2.legend([pl[PID[i]] for i in range(len(PID))], PID, loc="upper right")
    ax3.legend([pl[PID[i]] for i in range(len(PID))], monitorIP, loc="upper right")
    ax4.legend([pl[PID[i]] for i in range(len(PID))], monitorIP, loc="upper right")

    fig.tight_layout()


# save the figure
def saveFig():
    plt.savefig('Plot/'+PID_str + ".png")


# save the Data
def saveData():
    with open('Data/'+PID_str+'.csv', "w") as f:
        fw = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for p in PID:
            for cpu, mem, sent, recv in zip(ys1[p], ys2[p], ys3, ys4):
                fw.writerow([p, cpu, mem, sent, recv])


# function to animate
def animate(interval):
    global xs, ys1, ys2
    pidDone = 0
    for pid in PID:
        try:
            p = psutil.Process(pid)
            ys1[pid].append(p.cpu_percent(0.1) / psutil.cpu_count())
            ys2[pid].append(p.memory_info().rss)

        except psutil.NoSuchProcess:
            pidDone += 1
            if len(PID) == pidDone:
                saveFig()
                saveData()
                print('Saved')
                os._exit(0)
                sys.exit()


    xs.append(xs[-1] + .5)

    total = 0
    for key, count in packet_counts_send.items():
        total += count
    ys3.append(total)

    total = 0
    for key, count in packet_counts_recv.items():
        total += count
    ys4.append(total)

    # clear the subplot
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    # add the new subplot
    for pid in PID:
        pl[pid], = ax1.plot(xs[:len(ys1[pid])], ys1[pid], label=PID_str)
        ax2.plot(xs[:len(ys2[pid])], ys2[pid])
    ax3.plot(xs[:len(ys3)], ys3)
    ax4.plot(xs[:len(ys4)], ys4)

    addInfoPlot()


# Define our Custom Action function
def custom_action_recv(packet):
    # Create tuple of Src/Dst in sorted order
    try:
        key = tuple(sorted([packet[0][1].src, packet[0][1].dst]))
        packet_counts_recv.update([key])
        # return f"Packet #{sum(packet_counts_recv.values())}: {packet[0][1].src} ==> {packet[0][1].dst}"
        # testing
        # print("\n".join(f"Recv {f'{key[0]} <--> {key[1]}'}: {count}" for key, count in packet_counts_recv.items()))
    except AttributeError:
        return f"Packet error"


# Define our Custom Action function
def custom_action_send(packet):
    # Create tuple of Src/Dst in sorted order
    try:
        key = tuple(sorted([packet[0][1].src, packet[0][1].dst]))
        packet_counts_send.update([key])
        # return f"Packet #{sum(packet_counts_send.values())}: {packet[0][1].src} ==> {packet[0][1].dst}"
        # testing
        # print("\n".join(f"Send {f'{key[0]} <--> {key[1]}'}: {count}" for key, count in packet_counts_send.items()))
    except AttributeError:
        return f"Packet error"


def packet_capture_send():
    # Setup sniff, filtering for IP traffic
    sniff(filter="src " + monitorIP[0], prn=custom_action_send)


def packet_capture_recv():
    # Setup sniff, filtering for IP traffic
    sniff(filter="dst " + monitorIP[0], prn=custom_action_recv)


# main driver function
def main():
    global PID, PID_str, ys1, ys2, ys3, ys4, monitorIP

    print('Enter the process PID, IP')
    PID_str = input()
    PID, IP = PID_str.split(',')
    PID = [int(PID)]

    monitorIP = [IP]

    try:
        s = Thread(target=packet_capture_send)
        r = Thread(target=packet_capture_recv)

        s.start()
        r.start()
    except:
        print(f"Error: unable to start thread")

    for pid in PID:
        ys1.update({pid: [0.]})
        ys2.update({pid: [0.]})
        pl.update({pid: None})

    while True:
        ani = animation.FuncAnimation(fig, animate, interval=500)
        plt.show()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        exit()