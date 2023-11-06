from typing import Tuple
import matplotlib.pyplot as plt

import random
import numpy as np

def distance_field(x: np.ndarray, y: np.ndarray, k: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Calc summ of squared distances between point and the line (y = k*x + b)
    :param k: k (slopes)
    :param b: b (offsets)
    :returns: distance field F(k, b) = (Σ(yi -(k * xi + b))^2)^0.5
    """
    return np.array([[np.sqrt(np.sum((y - x * k_i + b_i) ** 2)) for k_i in k] for b_i in b])


def linear_regression(x: np.ndarray, y: np.ndarray) -> Tuple[float, float]:
    """
    :returns: (k, b), which is the solution for (Σ(yi -(k * xi + b))^2)->min
    """
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    n = x.size
    k = (np.sum(x * y) - sum_x * sum_y / n) / (np.sum(x * x) - sum_x * sum_x / n)
    return k, (sum_y - k * sum_x) / n


def bi_linear_regression(x: np.ndarray, y: np.ndarray, z: np.ndarray) -> Tuple[float, float, float]:
    """
    :returns: (kx, ky, b), which is the solution for (Σ(zi - (yi * ky + xi * kx + b))^2)->min
    """
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_z = np.sum(z)
    xy = np.sum(x * y)
    xx = np.sum(x * x)
    yy = np.sum(y * y)
    zy = np.sum(z * y)
    zx = np.sum(z * x)
    n = x.size

    hesse = np.linalg.inv(np.array([[xx, xy, sum_x], [xy, yy, sum_y], [sum_x, sum_y, n]]))

    dkx = xy + xx - zx
    dky = yy + xy - zy
    db = sum_y + sum_x - sum_z

    return 1.0 - (hesse[0][0] * dkx + hesse[0][1] * dky + hesse[0][2] * db), \
           1.0 - (hesse[1][0] * dkx + hesse[1][1] * dky + hesse[1][2] * db), \
               - (hesse[2][0] * dkx + hesse[2][1] * dky + hesse[2][2] * db)


def n_linear_regression(data_rows: np.ndarray) -> np.ndarray:
    """
    :param data_rows: [x_0,x_1,...,x_n, f(x_0,x_1,...,x_n)]
    """
    _, s_cols = data_rows.shape

    hessian = np.zeros((s_cols, s_cols,), dtype=float)
    grad = np.zeros((s_cols,), dtype=float)
    x_0 = np.zeros((s_cols,), dtype=float)

    for row in range(s_cols - 1):
        x_0[row] = 1.
        for col in range(row + 1):
            value = np.sum(data_rows[:, row] @ data_rows[:, col])
            hessian[row, col] = value
            hessian[col, row] = value

    for i in range(s_cols):
        value = np.sum(data_rows[:, i])
        hessian[i, s_cols - 1] = value
        hessian[s_cols - 1, i] = value

    hessian[s_cols - 1, s_cols - 1] = data_rows.shape[0]

    for row in range(s_cols - 1):
        grad[row] = np.sum(hessian[row, 0: s_cols - 1]) - np.dot(data_rows[:, s_cols - 1], data_rows[:, row])

    grad[s_cols - 1] = np.sum(hessian[s_cols - 1, 0 : s_cols - 1]) - np.sum(data_rows[:, s_cols - 1])
    return x_0 - np.linalg.inv(hessian) @ grad


def test_date_nd(surf_params = np.array([1, 2, 3, 4, 5, 6, 12]),
                 arg_range = 10, rand_range = 0.05, n_points = 100) -> np.ndarray:
    data = np.zeros((n_points, surf_params.size))
    for i in range(surf_params.size-1):
        data[:, i] = np.array([random.uniform(-0.5*arg_range, 0.5*arg_range) for _ in range(n_points)])
        data[:, surf_params.size-1] += data[:, i] * surf_params[i]
    data[:, surf_params.size-1] += np.array([surf_params[surf_params.size-1] + random.uniform(-0.5*rand_range, 0.5*rand_range) for _ in range(n_points)])
    return data


def n_linear_reg_test():
    print(n_linear_regression(test_date_nd()))


def test_data_3d(kx = -2., ky = 2., b = 12., half_disp = 1.01, n = 100, x_step = 0.01, y_step = 0.01) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Gen the plane z = kx*x + ky*x + b + dz, where dz is the additive noise with half_disp amplitude
    :param kx: x slope
    :param ky: y slope 
    :param b: z offset
    """
    x = np.array([random.uniform(0.0, n * x_step) for _ in range(n)])
    y = np.array([random.uniform(0.0, n * y_step) for _ in range(n)])
    dz = np.array([b + random.uniform(-half_disp, half_disp) for _ in range(n)])
    return x, y, x * kx + y * ky + dz


def poly_regression(x: np.ndarray, y: np.ndarray, order: int = 5) -> np.ndarray:
    """
    polynom: y = Σ_j x^j * bj
    Σ_i(yi - Σ_j xi^j * bj)^2 -> min
    Σ_i(yi - Σ_j xi^j * bj)^2 = Σ_iyi^2 - 2 * yi * Σ_j xi^j * bj +(Σ_j xi^j * bj)^2
    min req: d/dbj Σ_i ei = d/dbj (Σ_i yi^2 - 2 * yi * Σ_j xi^j * bj +(Σ_j xi^j * bj)^2) = 0
    :return: bi coeffs for y = Σx^i*bi
    """
    a_m = np.zeros((order, order,), dtype=float)
    c_m = np.zeros((order,), dtype=float)
    n = x.size
    copy_x = 1
    for row in range(order):
        c_m[row] = np.sum(y * (copy_x)) / n
        copy_copy_x = copy_x
        for col in range(row + 1):
            a_m[row][col] = np.sum(copy_copy_x) / n
            a_m[col][row] = a_m[row][col]
            copy_copy_x = copy_copy_x * x
        copy_x= copy_x * x
    return np.linalg.inv(a_m) @ c_m



def distance_field_test(x: np.ndarray, y: np.ndarray):
    k, b = linear_regression(x, y)
    plt.imshow(distance_field(x, y, np.linspace(-2., 2., 128, dtype=float), np.linspace(-2., 2., 128, dtype=float)), extent=(-2., 2., -2., 2.))
    plt.plot(k, b,'ro') # point of optimal min
    plt.xlabel('k')
    plt.ylabel('b')
    plt.title(f'distance field\nlin reg: y(x) = {k:1.5} * x + {b:1.5}')
    plt.grid(True)
    plt.show()


def linear_reg_test(x: np.ndarray, y: np.ndarray):
    k, b = linear_regression(x, y)
    plt.plot([0, 1.], [b, k + b])
    plt.plot(x, y, 'r.')
    plt.title(f'linear regression\ny(x) = {k:1.5} * x + {b:1.5}')
    plt.show()


def bi_linear_reg_test():
    x, y, z = test_data_3d()
    kx, ky, b = bi_linear_regression(x, y, z)
    x_, y_ = np.meshgrid(np.linspace(np.min(x), np.max(x), 100), np.linspace(np.min(y), np.max(y), 100))
    z_ = kx * x_ + y_ * ky + b
    _, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot(x, y, z, 'r.')
    ax.plot_surface(x_, y_, z_, linewidth=0, antialiased=False, edgecolor='none', alpha=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'bilinear reg\nz(x, y) = {kx:.5f} * x + {ky:.5f} * y + {b:.5f}')
    plt.show()


def poly_reg_test(x: np.ndarray, y: np.ndarray):
    def polynom(x: np.ndarray, b: np.ndarray) -> np.ndarray:
        result = b[0]
        copy_x = x
        for i in range(1, b.size):
            result += b[i] * copy_x
            copy_x = copy_x * x
        return result

    coeffs = poly_regression(x, y)
    plt.plot(x, polynom(x, coeffs))
    plt.plot(x, y, 'r.')
    plt.title(f'poly reg\ny(x) = {" + ".join(f"{coeffs[i]:.4f} * x^{i}" for i in range(coeffs.size))}')
    plt.show()


def test_square_data_3d(
        surf_param = (1., 2., 3., 1., 2., 3.),
        args_range = 1., rand_range = 0.1, n = 1000
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.array([random.uniform(0.0, args_range) for _ in range(n)])
    y = np.array([random.uniform(0.0, args_range) for _ in range(n)])
    dz = np.array([random.uniform(-rand_range, rand_range) for _ in range(n)])
    Fe = x * x * surf_param[0] + x * y * surf_param[1] + y * y * surf_param[2] + \
         x * surf_param[3] + y * surf_param[4] + surf_param[5]
    Des= dz + Fe
    return x, y, Des


def square_regression_3d(x: np.ndarray, y: np.ndarray, z: np.ndarray):
    b = [x * x, x * y, y * y, x, y, np.ones(len(x))]
    m = np.zeros((len(b), len(b)), dtype=float)
    d = np.zeros((6,), dtype=float)
    for rows in range(6):
        d[rows] = (b[rows] * z).sum()
        for cols in range(rows + 1):
            m[rows, cols] = (b[rows] * b[cols]).sum()
            m[cols, rows] = m[rows, cols]
    m[5, 5] = x.size
    return np.linalg.inv(m) @ d


def quadratic_reg_test():
    x, y, z = test_square_data_3d()

    x1, y1 = np.meshgrid(np.linspace(np.min(x), np.max(x), 200), np.linspace(np.min(y), np.max(y), 200))
    surf_param = square_regression_3d(x, y, z)
    z1 = surf_param[0] * x1 ** 2 + surf_param[1] * x1 * y1 + surf_param[2] * y1 ** 2 + surf_param[3] * x1 + surf_param[4] * y1 + surf_param[5]
    _, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot(x, y, z, 'r.')
    ax.plot_surface(x1, y1, z1, linewidth=0, antialiased=False, edgecolor='none',alpha=0.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(f'quadratic reg\nz(x, y) = {surf_param[0]:1.5} x^2 + {surf_param[1]:1.5} xy + {surf_param[2]:1.5} y^2 +\n {surf_param[3]:1.5} x + {surf_param[4]:1.5} y + {surf_param[5]:1.5}')
    plt.show()


def main():
    k = 1.
    b = 0.1
    x_step = 0.01
    half_disp = 0.05

    # 2d test data
    x = np.array([i * x_step for i in range(101)])
    y = np.array([i * x_step * k + b + random.uniform(-half_disp, half_disp) for i in range(101)])

    distance_field_test(x, y)
    linear_reg_test(x, y)
    bi_linear_reg_test()
    n_linear_reg_test()
    poly_reg_test(x, y)
    quadratic_reg_test()


if __name__ == "__main__":
    main()

