from time import sleep, time

def test(times, sleep_time):
    a = []
    for _ in range(times):
        temp = time()
        sleep(sleep_time)
        # print(abs(time()-temp-sleep_time), flush=True)
        a.append(abs(time()-temp-sleep_time))
    return a
print(test(100, 0.06))

"""test"""
# for i in range(5, 100, 5):
#     times_var = test(100, i*0.001)
#     print(i*0.001, "TOTAL", sum(times_var)/len(times_var))