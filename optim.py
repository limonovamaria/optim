import numpy as np


def nelder_mead(f, x0, alpha=1, gamma=2, rho=0.5, sigma=0.5, tol=1e-6):
    '''
    f - целевая функция
    x0 - начальная точка
    alpha - коэффициент отражения
    gamma - коэффициент растяжения
    rho - коэффициент сжатия
    sigma - коэффициент уменьшения
    tol - допустимая точность
    '''
    # Задаем начальные точки
    simplex = [x0]
    for i in range(len(x0)):
        point = x0.copy()
        point[i] = point[i] + 1
        simplex.append(point)

    # Основной цикл
    while True:
        # Шаг 1: сортировка вершин по значению функции
        simplex.sort(key=f)

        # Шаг 2: вычисление центра тяжести
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
                # Шаг 6: уменьшение
                for i in range(1, len(simplex)):
                    simplex[i] = simplex[0] + sigma * (simplex[i] - simplex[0])

        # Проверка условия остановки
        if all([np.linalg.norm(simplex[0] - simplex[i]) < tol for i in range(1, len(simplex))]):
            break

    return simplex[0]


def rosenbrock(x):
    return (1-x[0])**2 + 100*(x[1]-x[0]**2)**2


def ff(x):
    return x[0]**2+(x[1]-2)**2+x[2]**2


x0 = np.array([1.0, 1.0, 1.0])
xmin = nelder_mead(ff, x0)
print('Минимум:', xmin)