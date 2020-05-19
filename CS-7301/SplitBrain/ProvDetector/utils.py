
import math
import re

def nCr(n,r):
    f = math.factorial
    res =  f(n) / f(r) / f(n-r)
    return int(res)

def get_basename(path):
    if "\\" in path:
        return path.split("\\")[-1]
    elif "/" in path:
        return path.split("/")[-1]
    return path

def split_merged_names(name):
    res = []
    indexes = [m.start() for m in re.finditer('[A-Z]:/', name)]
    if len(indexes)==0:
        return [name]
    for i in range(0, len(indexes)-1):
        res.append(name[indexes[i]:indexes[i+1]].strip())
    res.append(name[indexes[-1]:].strip())
    return res

def get_filetype(path):
    return path.split(".")[-1]

def readlines(file_path):
    return [line.replace("\n","") for line in open(file_path).readlines()]

def merge_lists(list_of_list):
    res = []
    for l in list_of_list:
        for item in l:
            res.append(item)
    return res

def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def slice_list(l, ratio):
    l = sorted(l)
    size = int(len(l) * (1-ratio))
    start = int((ratio/2) *len(l))
    end = start + size
    return l[start: end]

