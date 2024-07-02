import json

from flask import Flask, request, jsonify
from optim import create_func, nelder_mead
import numpy as np
import sqlite3
import psycopg2

app = Flask(__name__)


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]

@app.route('/optim_bak', methods=['POST'])
def get_optim_solu_test():
    data = {
        "isResult": True,
        "menu_breakfast": [
            {
            "caloricity": "73",
            "category_id": 1,
            "id": 1,
            "product_name": "Овсянка",
            "weight": 204.0895934768988,
            "weight_for_one": 0
            },
            {
            "caloricity": "89",
            "category_id": 4,
            "id": 6,
            "product_name": "Банан",
            "weight": 67.3676377486061,
            "weight_for_one": 200
            },
            {
            "caloricity": "553",
            "category_id": 5,
            "id": 9,
            "product_name": "Кешью",
            "weight": 17.146871788427067,
            "weight_for_one": 0
            },
            {
            "caloricity": "366",
            "category_id": 6,
            "id": 11,
            "product_name": "Хлебцы",
            "weight": 19.654424269662965,
            "weight_for_one": 10
            }
        ],
        "menu_dinner": [

            {
            "caloricity": "89",
            "category_id": 4,
            "id": 6,
            "product_name": "Банан",
            "weight": 67.3676377486061,
            "weight_for_one": 200
            },
            {
            "caloricity": "553",
            "category_id": 5,
            "id": 9,
            "product_name": "Кешью",
            "weight": 17.146871788427067,
            "weight_for_one": 0
            },
            {
            "caloricity": "366",
            "category_id": 6,
            "id": 11,
            "product_name": "Хлебцы",
            "weight": 19.654424269662965,
            "weight_for_one": 10
            },
            {
            "caloricity": "159",
            "category_id": 7,
            "id": 13,
            "product_name": "Творог",
            "weight": 264.6777071355749,
            "weight_for_one": 0
            }
        ],
        "menu_lunch": [
            {
            "caloricity": "130",
            "category_id": 2,
            "id": 3,
            "product_name": "Рис",
            "weight": 207.28282737013086,
            "weight_for_one": 0
            },
            {
            "caloricity": "170",
            "category_id": 3,
            "id": 4,
            "product_name": "Курица вареная",
            "weight": 209.52370029453573,
            "weight_for_one": 0
            },
            {
            "caloricity": "366",
            "category_id": 6,
            "id": 11,
            "product_name": "Хлебцы",
            "weight": 19.654424269662965,
            "weight_for_one": 10
            },
            {
            "caloricity": "15",
            "category_id": 8,
            "id": 14,
            "product_name": "Огурец",
            "weight": 200.84032729043813,
            "weight_for_one": 110
            }
        ],
        "menu_snack": [
            {
            "caloricity": "89",
            "category_id": 4,
            "id": 6,
            "product_name": "Банан",
            "weight": 67.3676377486061,
            "weight_for_one": 200
            },
            {
            "caloricity": "553",
            "category_id": 5,
            "id": 9,
            "product_name": "Кешью",
            "weight": 17.146871788427067,
            "weight_for_one": 0
            }
        ]
        }
    return jsonify(data)


@app.route('/optim', methods=['POST'])
def get_optim_solu():

    #connection = sqlite3.connect('my_database.db')
    connection = psycopg2.connect(dbname='testmenumaker', user='postgres', password='123', host='localhost', port=5432)
    cursor = connection.cursor()
    data = request.get_json()
    food_energy_goal = data['food_energy_goal']
    ref_id = data['ref_id']
    # калорийности продуктов (необходимо получить из БД с размерностью ккал/гр)
    # [1:[], 2:[], ...]
    KKAL_IN_GR = 0.01
    #ref_id = 1
    #Запрос проверен
    cursor.execute(
        'SELECT fridge_id, product_id, caloricity, category_id FROM fridgehasproduct JOIN product ON product_id = id AND fridge_id = '+
        str(ref_id)+' ORDER BY product_id')
    groups = cursor.fetchall()

    food_energy_groups = []
    for i in range(1, 9):
        b = []
        for x in groups:
            if (x[3] == i):
                b = np.append(b, x[2])
        food_energy_groups.append(b)

    for k in food_energy_groups:
        for i in range(0, len(k)):
            k[i] = float(k[i])*KKAL_IN_GR

    # граммовки продуктов (необходимо получить из БД с размерностью гр)
    # [1:[], 2:[], ...]
    # Запрос проверен
    cursor.execute(
        'SELECT fridge_id, product_id, gramms, category_id FROM fridgehasproduct JOIN product ON product_id = id AND fridge_id = '+
        str(ref_id) +' ORDER BY product_id')
    groups = cursor.fetchall()
    food_quantity_groups = []
    for i in range(1, 9):
        b = []
        for x in groups:
            if (x[3] == i):
                b = np.append(b, x[2])
        food_quantity_groups.append(b)
    # Запрос изменен и проверен
    cursor.execute('SELECT min FROM category GROUP BY (id, min) ORDER BY id;')
    l_min = cursor.fetchall()
    limits_min = np.zeros(8)
    k = 0
    for x in l_min:
        limits_min[k] = x[0]
        k = k + 1

    # ограничения на холодильник (необходимо получить из БД с размерностью гр)
     # брать из бд, ограничения по каждой группе
    # Запрос изменен и проверен
    cursor.execute('SELECT max FROM category GROUP BY (id, max) ORDER BY id;')
    l_max = cursor.fetchall()
    limits_max = np.zeros(8)
    k = 0
    for x in l_max:
        limits_max[k] = x[0]
        k = k + 1

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

#Выводим названия продуктов
    #Запрос проверен
    cursor.execute(
        'SELECT id, name, category_id, weight_for_one, caloricity FROM fridgehasproduct JOIN product ON product_id = product.id WHERE fridge_id = ' +
        str(ref_id)+' ORDER BY id')
    names = cursor.fetchall()

    jsonList = []

    breakfast = []
    lunch = []
    dinner = []
    snack = []

    k = 0

    for name in names:
        if (name[2]==1 and res[k]>15):
            breakfast.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k], "weight_for_one": name[3], "caloricity":name[4]})
        elif ((name[2]==2 or name[2]==3) and res[k]>15):
            lunch.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k],"weight_for_one": name[3], "caloricity": name[4]})
        elif ((name[2]==4 or name[2]==5) and res[k]>15):
            breakfast.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3,"weight_for_one": name[3], "caloricity": name[4]})
            dinner.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3, "weight_for_one": name[3], "caloricity": name[4]})
            snack.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3, "weight_for_one": name[3], "caloricity": name[4]})
        elif (name[2]==6 and res[k]>15):
            breakfast.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3, "weight_for_one": name[3], "caloricity": name[4]})
            lunch.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3, "weight_for_one": name[3], "caloricity": name[4]})
            dinner.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k] / 3,"weight_for_one": name[3], "caloricity": name[4]})
        elif (name[2]==7 and res[k]>15):
            dinner.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k],"weight_for_one": name[3], "caloricity": name[4]})
        elif (name[2]==8 and res[k]>15):
            lunch.append({"id": name[0], "product_name": name[1], "category_id": name[2], "weight": res[k],"weight_for_one": name[3], "caloricity": name[4]})
        k = k + 1



    isResult = False
    for grs in res:
        if(grs > 1):
            isResult = True


    connection.close()
   # return jsonify({'isResult': isResult, 'result': jsonList, 'breakfast': breakfast, 'lunch': lunch, 'dinner': dinner, 'snack': snack })
    return jsonify({'isResult': isResult, 'menu_breakfast': breakfast, 'menu_lunch': lunch, 'menu_dinner': dinner, 'menu_snack': snack })

if __name__ == '__main__':
    app.run(debug=True)
