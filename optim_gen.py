"""Модуль формирования целевых функций (включая штрафные)"""


def take_first(ar, n):
    return ar[:n], ar[n:]


def create_func(k_targ, ka, kb, kc, kd, a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max, k=1e3, p=2):
    def inner_method(x):
        EPS = 1.0  # Значение, ниже которого второй по величине параметр в группе считается подходящим
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

        f_res = (k_calc - k_targ)**2

        # ограничения на неотрицательность
        for xx in [xa, xb, xc, xd]:
            f_res += k * sum([max(-xi, 0) ** p for xi in xx])

        # Ограничения на мин. каждой группы
        for xx, mmin in zip([xa, xb, xc, xd], [a_min, b_min, c_min, d_min]):
            f_res += k * max(-(sum([xi for xi in xx]) - mmin), 0) ** p
        # Ограничения на макс. каждой группы
        for xx, mmax in zip([xa, xb, xc, xd], [a_max, b_max, c_max, d_max]):
            f_res += k * max(-(mmax - sum([xi for xi in xx])), 0) ** p

        # ограничение на один параметр в группе
        for xx in [xa, xb, xc, xd]:
            xx_new = sorted(xx)
            f_res += k * max(xx_new[-2]-EPS, 0) ** p

        return f_res

    return inner_method


