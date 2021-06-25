chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
length = len(chars)
print(length)
import sys
sys.setrecursionlimit(999999999)
global t
t = []
def closer(num, i):
    i += 1
    if len(t) > 10:
        if t[-1] == t[-3]:
            print(i)
            return
    t.append((num, 255/num))
    if 255/num >= length:
        closer(round(num+.01, 2), i)
    else:
        closer(round(num-.01, 2), i)

closer(20, 0)
print(t[-2:])
# import string
# print(string.printable)