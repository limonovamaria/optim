"""Модуль формирования целевых функций (включая штрафные)"""


def take_first(ar, n):
    """
    разделяет список на два списка размерами [n] и [len(ar)-n]
    """
    return ar[:n], ar[n:]


def create_func(food_energy_goal,
                food_energy_groups,
                groups_limits,
                food_limits,
                penalty=1e3, penalty_power=2):
    """
    создаёт функцию, f(x), где x - список граммовок продуктов, f - целевая функция со штрафами
    """
    zero = 0

    a_min, a_max, b_min, b_max, c_min, c_max, d_min, d_max = groups_limits

    ka, kb, kc, kd = food_energy_groups

    ga, gb, gc, gd = food_limits

    lens = tuple(map(len, food_energy_groups))

    lenka = len(ka)
    lenkb = len(kb)
    lenkc = len(kc)
    lenkd = len(kd)

    def pairwise(arr):
        # for i in range(0, len(arr), 2):
        #     yield arr[i], arr[i + 1]
        yield arr[0:lenka]
        yield arr[lenka:lenka]
        yield arr[0:lenka]
        yield arr[0:lenka]

    for pair in pairwise(food_energy_groups):
        print(pair)

    print(pairwise(my_array))
    def inner_method(x):
        EPS = 1.0  # Значение, ниже которого второй по величине параметр в группе считается подходящим
        # TODO проверку на неодинаковость размерности

        quantity_group = []
        # for food_energy_group in food_energy_groups:
        #     xa, x = take_first(x, len(food_energy_group))
            # quantity_group

        xa, x = take_first(x, lenka)
        xb, x = take_first(x, lenkb)
        xc, x = take_first(x, lenkc)
        xd, x = take_first(x, lenkd)

        food_energy_calc = zero
        food_energy_calc += sum([xi * ki for xi, ki in zip(xa, ka)])
        food_energy_calc += sum([xi * ki for xi, ki in zip(xb, kb)])
        food_energy_calc += sum([xi * ki for xi, ki in zip(xc, kc)])
        food_energy_calc += sum([xi * ki for xi, ki in zip(xd, kd)])

        f_res = (food_energy_calc - food_energy_goal)**2

        # ограничения на неотрицательность
        for xx in [xa, xb, xc, xd]:
            f_res += penalty * sum([max(-xi, 0)**penalty_power for xi in xx])

        # Ограничения на мин. каждой группы
        for xx, mmin in zip([xa, xb, xc, xd], [a_min, b_min, c_min, d_min]):
            f_res += penalty * max(-(sum([xi for xi in xx]) - mmin), 0)**penalty_power

        # Ограничения на макс. каждой группы
        for xx, mmax in zip([xa, xb, xc, xd], [a_max, b_max, c_max, d_max]):
            f_res += penalty * max(-(mmax - sum([xi for xi in xx])), 0)**penalty_power

        # ограничение на один параметр в группе
        for xx in [xa, xb, xc, xd]:
            xx_new = sorted(xx)
            f_res += penalty * max(xx_new[-2] - EPS, 0)**penalty_power

        # ограничение на граммовки
        for xx, gg in zip([xa, xb, xc, xd], [ga, gb, gc, gd]):
            for xi, gi in zip(xx, gg):
                f_res += penalty * max(xi - gi, 0)**penalty_power

        return f_res

    return inner_method


