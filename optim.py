import numpy as np


def nelder_mead(f, x0, alpha=1, gamma=2, rho=0.5, sigma=0.5, tol=1e-6, maxiter=1000, dx=1):
    '''
    f - целевая функция
    x0 - начальная точка
    alpha - коэффициент отражения
    gamma - коэффициент растяжения
    rho - коэффициент сжатия
    sigma - коэффициент глобального сжатия
    tol - допустимая точность
    '''
    # Создаём начальный симплекс (n+1 мерный)
    simplex = [x0]
    for i in range(len(x0)):
        point = x0.copy()
        point[i] = point[i] + dx
        simplex.append(point)

    # Основной цикл
    for iter in range(maxiter):
        # Шаг 1: сортировка вершин по значению функции
        simplex.sort(key=f)

        # Шаг 2: вычисление центра тяжести без худшей точки
        centroid = np.mean(simplex[:-1], axis=0)

        # Шаг 3: отражение
        xr = centroid + alpha * (centroid - simplex[-1])
        if f(simplex[0]) <= f(xr) < f(simplex[-2]):
            simplex[-1] = xr

        # Шаг 4: растяжение
        elif f(xr) < f(simplex[0]):
            xe = centroid + gamma * (xr - centroid)
            if f(xe) < f(xr):
                simplex[-1] = xe
            else:
                simplex[-1] = xr
        # Шаг 5: сжатие
        else:
            xc = centroid + rho * (simplex[-1] - centroid)
            if f(xc) < f(simplex[-1]):
                simplex[-1] = xc
            else:
                # Шаг 6: глобальное сжатие симплекса к точке с наименьшим значением
                for i in range(1, len(simplex)):
                    simplex[i] = simplex[0] + sigma * (simplex[i] - simplex[0])

        # Проверка условия остановки
        if all([np.linalg.norm(simplex[0] - simplex[i]) < tol for i in range(1, len(simplex))]):
            break

    return simplex[0], iter

