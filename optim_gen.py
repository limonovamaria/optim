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

        k_calc = sum([xi*gi*ki for xi, gi, ki in zip(xa, a, ka)])
        k_calc += sum([xi*gi*ki for xi, gi, ki in zip(xb, b, kb)])
        k_calc += sum([xi*gi*ki for xi, gi, ki in zip(xc, c, kc)])
        k_calc += sum([xi*gi*ki for xi, gi, ki in zip(xd, d, kd)])

        f_res = (k_calc-k_targ)**2

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

# получаем данные из json (k_targ)
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


# nelder_mead(f, (xa, xb, xc, xd, a, b, c, d))
ka = [500, 300, 400]
kb = [200, 200, 300]
kc = [50, 20]
kd = [20, 10, 10]
k_targ = 2000
a_min = 50
a_max = 500
b_min = 50
b_max = 500
c_min = 50
c_max = 500
d_min = 50
d_max = 500


ff = create_func(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max)
x0 = np.zeros((len(ka)+len(kb)+len(kc)+len(kd))*2)

res, iter = nelder_mead(ff, x0, maxiter=12000)


def take_first(ar, n):
    return ar[:n], ar[n:]
# take_first = lambda ar, n: (ar[:n], ar[n:])


print(ff(res), iter)
xa, res = take_first(res, len(ka))
xb, res = take_first(res, len(kb))
xc, res = take_first(res, len(kc))
xd, res = take_first(res, len(kd))
a, res = take_first(res, len(ka))
b, res = take_first(res, len(kb))
c, res = take_first(res, len(kc))
d, res = take_first(res, len(kd))
print("xa", xa)
print("xb", xb)
print("xc", xc)  # отрицательные
print("xd", xd)  # отрицательные
print("a", a)
print("b", b)
print("c", c)
print("d", d)


# X = np.array(np.linspace(0, 4, 50))
# Y = np.array(np.linspace(0, 4, 50))
# X, Y = np.meshgrid(X, Y)
# Z = ff([X, Y])
#
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# ax.plot_surface(X, Y, Z)#, vmin=Z.min() * 2)#, cmap=cm.Blues)
# ax.scatter(xk.c()[0], xk.c()[1], func(xk.c()), marker='o', color='Red', s=50)
# plt.show()
