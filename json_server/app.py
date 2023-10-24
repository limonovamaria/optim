import numpy
from flask import Flask, request, jsonify
from optim import create_func, nelder_mead
import numpy as np
import sqlite3

app = Flask(__name__)


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


@app.route('/optim', methods=['POST'])
def get_optim_solu():
    ##

    connection = sqlite3.connect('my_database.db')

    req_Json = request.json
    cursor = connection.cursor()
    """""
    cursor.execute('SELECT username FROM Users where age = ?', (28,))
    usernames = cursor.fetchall()
    username = " "
    # Выводим результаты
    for user in usernames:
        username = user
    """""



    data = request.get_json()
    food_energy_goal = data['food_energy_goal']

    # калорийности продуктов (необходимо получить из БД с размерностью ккал/гр)
    KKAL_IN_GR = 0.01
    #
    ref_id = 1
    cursor.execute(
        'SELECT refrigerator_id, product_id, caloricity, categories_id FROM refrigerator_has_product JOIN  product WHERE product_id = id AND refrigerator_id = ?',
        (ref_id,))
    groups = cursor.fetchall()

    food_energy_groups = []
    for i in range(1, 9):
        b = []
        for x in groups:
            if (x[3] == i):
                b = np.append(b, x[2])
        food_energy_groups.append(b)
    #
    '''
    food_energy_groups = [
        [k * KKAL_IN_GR for k in [68]],# брать из бд 1 группа 1 продукт
        [k * KKAL_IN_GR for k in [343, 360]],
        [k * KKAL_IN_GR for k in [170]],
        [k * KKAL_IN_GR for k in [52, 89, 48]],
        [k * KKAL_IN_GR for k in [654, 553]],
        [k * KKAL_IN_GR for k in [259, 366]],
        [k * KKAL_IN_GR for k in [40, 159]],
        [k * KKAL_IN_GR for k in [15, 18]]]
    '''
    for k in food_energy_groups:
        for i in range(0, len(k)):
            k[i] = k[i]*KKAL_IN_GR



    # граммовки продуктов (необходимо получить из БД с размерностью гр)
    cursor.execute(
        'SELECT refrigerator_id, product_id, amount, categories_id FROM refrigerator_has_product JOIN  product WHERE product_id = id AND refrigerator_id = ?',
        (ref_id,))
    groups = cursor.fetchall()
    food_quantity_groups = []
    for i in range(1, 9):
        b = []
        for x in groups:
            if (x[3] == i):
                b = np.append(b, x[2])
        food_quantity_groups.append(b)

    '''
    food_quantity_groups = [ # брать от пользователя
        [200],# 1 группа 1 продукт
        [300, 200],# 2 группа 2 продукта
        [500],
        [200, 200, 150],
        [40, 50],
        [300, 150],
        [1000, 500],
        [200, 200]]
    '''

    cursor.execute('SELECT min FROM limits')
    l_min = cursor.fetchall()
    limits_min = np.zeros(8)
    k = 0
    for x in l_min:
        limits_min[k] = x[0]
        k = k + 1
    #print(min)
    # ограничения на холодильник (необходимо получить из БД с размерностью гр)
    #limits_min = [50, 50, 50, 50, 10, 10, 50, 50] # брать из бд, ограничения по каждой группе

    cursor.execute('SELECT max FROM limits')
    l_max = cursor.fetchall()
    limits_max = np.zeros(8)
    k = 0
    for x in l_max:
        limits_max[k] = x[0]
        k = k + 1
    #limits_max = [200, 200, 300, 200, 30, 30, 200, 150]

    group_limits_min = np.array(limits_min)
    group_limits_max = np.array(limits_max)

    food_energy_groups_array = np.array(flatten(food_energy_groups))
    food_limits_array = np.array(flatten(food_quantity_groups))

    groups_array = np.array([len(group) for group in food_energy_groups])

    ff = create_func(food_energy_goal,
                     groups_array,
                     food_energy_groups_array,
                     group_limits_min,
                     group_limits_max,
                     food_limits_array,
                     penalty=1e1, penalty_power=2)
    x0 = np.zeros(len(food_energy_groups_array))

    (res, iter), time = nelder_mead(ff, x0, gamma=2, maxiter=20000, dx=10)
    connection.close()
    return jsonify({'result': res.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
