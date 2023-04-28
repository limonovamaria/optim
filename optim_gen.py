import numpy as np
from optim import nelder_mead
import matplotlib.pyplot as plt


def create_func(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max, k=1000, p=2):
    def inner_method(x):
        take_first = lambda ar, n: (ar[:n], ar[n:])

        # TODO проверку на неодинаковость размерности
        xa, x = take_first(x, len(ka))
        xb, x = take_first(x, len(kb))
        xc, x = take_first(x, len(kc))
        xd, x = take_first(x, len(kd))
        a, x = take_first(x, len(ka))
        b, x = take_first(x, len(kb))
        c, x = take_first(x, len(kc))
        d, x = take_first(x, len(kd))

        k_calc = sum([xi * gi * ki for xi, gi, ki in zip(xa, a, ka)])
        k_calc += sum([xi * gi * ki for xi, gi, ki in zip(xb, b, kb)])
        k_calc += sum([xi * gi * ki for xi, gi, ki in zip(xc, c, kc)])
        k_calc += sum([xi * gi * ki for xi, gi, ki in zip(xd, d, kd)])

        f_res = (k_calc - k_targ) ** 2

        for x in [xa, xb, xc, xd, a, b, c, d]:
            f_res += k * sum([max(-y, 0) ** p for y in x])
        # for x in [a, b, c, d]:
        #     f_res += k * sum([max(-y, 0) ** p for y in x])
        # for x in [a, b, c, d]:
        #     f_res += k * sum([max(y-100, 0) ** p for y in x])
        #
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xa, a)])-a_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xb, b)])-b_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xc, c)])-c_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xd, d)])-d_min), 0) ** p
        #
        # f_res += k * max(-(a_max-(sum([xi*gi for xi, gi in zip(xa, a)]))), 0) ** p
        # f_res += k * max(-(b_max-(sum([xi*gi for xi, gi in zip(xb, b)]))), 0) ** p
        # f_res += k * max(-(c_max-(sum([xi*gi for xi, gi in zip(xc, c)]))), 0) ** p
        # f_res += k * max(-(d_max-(sum([xi*gi for xi, gi in zip(xd, d)]))), 0) ** p

        return f_res

    return inner_method


def create_func_2(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max, k=1e4, p=2):
    def inner_method(x):
        take_first = lambda ar, n: (ar[:n], ar[n:])

        # TODO проверку на неодинаковость размерности
        xa, x = take_first(x, len(ka))
        xb, x = take_first(x, len(kb))
        xc, x = take_first(x, len(kc))
        xd, x = take_first(x, len(kd))

        k_calc = 0
        k_calc += sum([xi * ki for xi, ki in zip(xa, ka)])
        k_calc += sum([xi * ki for xi, ki in zip(xb, kb)])
        k_calc += sum([xi * ki for xi, ki in zip(xc, kc)])
        k_calc += sum([xi * ki for xi, ki in zip(xd, kd)])

        f_res = (k_calc - k_targ) ** 2

        # ограничения на неотрицательность
        for xx in [xa, xb, xc, xd]:
            f_res += k * sum([max(-xi, 0) ** p for xi in xx])

        # for x in [a, b, c, d]:
        #     f_res += k * sum([max(-y, 0) ** p for y in x])
        # for x in [a, b, c, d]:
        #     f_res += k * sum([max(y-100, 0) ** p for y in x])

        # k1 = 1
        # for xx in [xa, xb, xc, xd]:
        #     prod = k1
        #     for xi in xx:
        #         prod *= xi
        #     f_res += prod

        # ИДЕЯ: степень штрафа зависит от нагруженности сервера

        # ограничения на мин/макс каждой группы
        f_res += k * max(-(sum([xi for xi in xa]) - a_min), 0) ** p
        f_res += k * max(-(a_max - sum([xi for xi in xa])), 0) ** p
        f_res += k * max(-(sum([xi for xi in xa]) - b_min), 0) ** p
        f_res += k * max(-(b_max - sum([xi for xi in xb])), 0) ** p
        f_res += k * max(-(sum([xi for xi in xc]) - c_min), 0) ** p
        f_res += k * max(-(c_max - sum([xi for xi in xc])), 0) ** p
        f_res += k * max(-(sum([xi for xi in xd]) - d_min), 0) ** p
        f_res += k * max(-(d_max - sum([xi for xi in xd])), 0) ** p

        xb_new = sorted(xb)  # тоже вариант плохо получается
        if xb_new[-1] < (xb_new[-2] * 10**2):
            f_res += k

        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xa, a)])-a_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xb, b)])-b_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xc, c)])-c_min), 0) ** p
        # f_res += k * max(-(sum([xi*gi for xi, gi in zip(xd, d)])-d_min), 0) ** p
        #
        # f_res += k * max(-(a_max-(sum([xi*gi for xi, gi in zip(xa, a)]))), 0) ** p
        # f_res += k * max(-(b_max-(sum([xi*gi for xi, gi in zip(xb, b)]))), 0) ** p
        # f_res += k * max(-(c_max-(sum([xi*gi for xi, gi in zip(xc, c)]))), 0) ** p
        # f_res += k * max(-(d_max-(sum([xi*gi for xi, gi in zip(xd, d)]))), 0) ** p

        return f_res

    return inner_method


# Получаем данные из json (k_targ)
# считаем количество параметров для формирования симплекса
# формируем функцию
# надо сделать шаблон
# как засунуть коэффициенты в функцию? функция обращается к серверу БД? Нет, держит в кэше, обращается к серверу раз в какое-то время
# во всех операциях отражения и т.п. нужно учитывать тип переменных для a, b, c, d

# xa = np.array([0, 0, 0])
# a = np.array([0, 0, 0])
# xb = np.array([0, 0])
# b = np.array([0, 0])
# xc = np.array([0, 0, 0])
# c = np.array([0, 0, 0])
# xd = np.array([0, 0])
# d = np.array([0, 0])
KKAL_IN_GR = 0.01

# nelder_mead(f, (xa, xb, xc, xd, a, b, c, d))
ka = [k * KKAL_IN_GR for k in [360, 300, 400]]
kb = [k * KKAL_IN_GR for k in [200, 200, 300, 350]]
kc = [k * KKAL_IN_GR for k in [50, 20]]
kd = [k * KKAL_IN_GR for k in [20, 10, 10]]
k_targ = 2000
a_min = 50
a_max = 200
b_min = 50
b_max = 500
c_min = 50
c_max = 500
d_min = 50
d_max = 500

ff = create_func_2(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max)
x0 = np.zeros((len(ka) + len(kb) + len(kc) + len(kd)))  # *2

res, iter = nelder_mead(ff, x0, gamma=2, maxiter=10000, dx=10)


def take_first(ar, n):
    return ar[:n], ar[n:]


# take_first = lambda ar, n: (ar[:n], ar[n:])


print("Ф(x)={a:10.2e}, iterations={b:d}".format(a=ff(res), b=iter))
xa, res = take_first(res, len(ka))
xb, res = take_first(res, len(kb))
xc, res = take_first(res, len(kc))
xd, res = take_first(res, len(kd))
# a, res = take_first(res, len(ka))
# b, res = take_first(res, len(kb))
# c, res = take_first(res, len(kc))
# d, res = take_first(res, len(kd))
# print("xa*100:", "\t".join([str(x*100) for x in xa]))
# print("xb*100:", "\t".join([str(x*100) for x in xb]))


def myprint(**kwargs):
    for arg_name in kwargs:
        xx = kwargs[arg_name]
        print(arg_name, end=':')
        for x in xx:
            print("{a:10.2f}".format(a=x), end='')
        print()

print()
myprint(xa=xa, xb=xb, xc=xc, xd=xd)

k_calc = 0
k_calc += sum([xi * ki for xi, ki in zip(xa, ka)])
k_calc += sum([xi * ki for xi, ki in zip(xb, kb)])
k_calc += sum([xi * ki for xi, ki in zip(xc, kc)])
k_calc += sum([xi * ki for xi, ki in zip(xd, kd)])
print("\nk_targ={a:12.6f}".format(a=k_targ))
print("k_calc={a:12.6f}".format(a=k_calc))

# X = np.array(np.linspace(0, 4, 50))
# Y = np.array(np.linspace(0, 4, 50))
# X, Y = np.meshgrid(X, Y)
# Z = ff([X, Y])
#
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.plot_surface(X, Y, Z)#, vmin=Z.min() * 2)#, cmap=cm.Blues)
# ax.scatter(xk.c()[0], xk.c()[1], func(xk.c()), marker='o', color='Red', s=50)
# plt.show()
