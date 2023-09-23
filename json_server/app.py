from flask import Flask, request, jsonify
from optim import create_func, nelder_mead
import numpy as np

app = Flask(__name__)


def flatten(list_of_lists):
    return [item for sublist in list_of_lists for item in sublist]


@app.route('/optim', methods=['POST'])
def get_optim_solu():
    data = request.get_json()
    food_energy_goal = data['food_energy_goal']

    # калорийности продуктов (необходимо получить из БД с размерностью ккал/гр)
    KKAL_IN_GR = 0.01
    food_energy_groups = [
        [k * KKAL_IN_GR for k in [68]],
        [k * KKAL_IN_GR for k in [343, 360]],
        [k * KKAL_IN_GR for k in [170]],
        [k * KKAL_IN_GR for k in [52, 89, 48]],
        [k * KKAL_IN_GR for k in [654, 553]],
        [k * KKAL_IN_GR for k in [259, 366]],
        [k * KKAL_IN_GR for k in [40, 159]],
        [k * KKAL_IN_GR for k in [15, 18]]]

    # граммовки продуктов (необходимо получить из БД с размерностью гр)
    food_quantity_groups = [
        [200],
        [300, 200],
        [500],
        [200, 200, 150],
        [40, 50],
        [300, 150],
        [1000, 500],
        [200, 200]]

    # ограничения на холодильник (необходимо получить из БД с размерностью гр)
    limits_min = [50, 50, 50, 50, 10, 10, 50, 50]
    limits_max = [200, 200, 300, 200, 30, 30, 200, 150]

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

    return jsonify({'result': res.tolist()})


if __name__ == '__main__':
    app.run(debug=True)
