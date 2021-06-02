chars = "  .:!+*e$@8"
length = len(chars)-1


def closer(num, i):
    i += 1
    if i>600: return
    print(num, 255/num)
    if 255/num >= length:
        closer(round(num+.01, 2), i)
    else:
        closer(round(num-.01, 2), i)

closer(30, 0)
# import string
# print(string.printable)