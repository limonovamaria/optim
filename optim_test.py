from optim_gen import create_func, create_func_2, take_first
from optim import nelder_mead
import numpy as np


def myprint(**kwargs):
    for arg_name in kwargs:
        xx = kwargs[arg_name]
        print(arg_name, end=':')
        for x in xx:
            print("{a:10.2f}".format(a=x), end='')
        print()


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

ff = create_func_2(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max, k=1e4)
x0 = np.zeros((len(ka) + len(kb) + len(kc) + len(kd)))  # *2
# x0 = np.random.random_sample(len(ka) + len(kb) + len(kc) + len(kd)) * 100
(res, iter), time = nelder_mead(ff, x0, gamma=2, maxiter=10000, dx=100)

# TODO нужно запоминать лучшее решение, чтобы при достижении границы что-то выдать

print("Ф(x)={a:10.2e}, iterations={b:d}, time={c:5.1f}".format(a=ff(res), b=iter, c=time))
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