from flask import Flask, request, jsonify
from optim import create_func, nelder_mead
import numpy as np

app = Flask(__name__)


@app.route('/optim', methods=['POST'])
def get_optim_solu():
    data = request.get_json()
    food_energy_goal = data['food_energy_goal']
    value2 = data['value2']


    KKAL_IN_GR = 0.01

    ka = [k * KKAL_IN_GR for k in [68]]
    kb = [k * KKAL_IN_GR for k in [343, 360]]
    kc = [k * KKAL_IN_GR for k in [170]]
    kd = [k * KKAL_IN_GR for k in [52, 89, 48]]
    ke = [k * KKAL_IN_GR for k in [654, 553]]
    kf = [k * KKAL_IN_GR for k in [259, 366]]
    kg = [k * KKAL_IN_GR for k in [40, 159]]
    kh = [k * KKAL_IN_GR for k in [15, 18]]

    # граммовки продуктов
    ga = [200]
    gb = [300, 200]
    gc = [500]
    gd = [200, 200, 150]
    ge = [40, 50]
    gf = [300, 150]
    gg = [1000, 500]
    gh = [200, 200]

    group_limits_min = np.array([50, 50, 50, 50, 10, 10, 50, 50])
    group_limits_max = np.array([200, 200, 300, 200, 30, 30, 200, 150])

    food_energy_groups = np.array(ka + kb + kc + kd + ke + kf + kg + kh)
    food_limits = np.array(ga + gb + gc + gd + ge + gf + gg + gh)

    groups = np.array([len(group) for group in [ka, kb, kc, kd, ke, kf, kg, kh]])

    ff = create_func(food_energy_goal,
                     groups,
                     food_energy_groups,
                     group_limits_min,
                     group_limits_max,
                     food_limits,
                     penalty=1e1, penalty_power=2)
    x0 = np.zeros(len(food_energy_groups))
    # x0 = np.random.random_sample(len(ka) + len(kb) + len(kc) + len(kd)) * 100
    (res, iter), time = nelder_mead(ff, x0, gamma=2, maxiter=20000, dx=10)

    return jsonify({'result': res.tolist()})


@app.route('/sum', methods=['POST'])
def sum_two_values():
    data = request.get_json()
    value1 = data['value1']
    value2 = data['value2']
    result = value1 + value2
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
