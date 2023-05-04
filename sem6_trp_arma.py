import matplotlib.pyplot as plt
import math
import numpy as np

f = open('sem6_trp_arma_input.txt', 'r')
inp = [float(line.strip()) for line in f]

exp_val = sum(i for i in inp) / len(inp)
var = sum((i - exp_val) ** 2 for i in inp) / (len(inp) - 1)
stand_dev = var ** 0.5

plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(inp[:101], color='black', label='Source process')
p2, = plt.plot([exp_val] * 101, color='r', label='Average')
p3, = plt.plot([exp_val + stand_dev] * 101, color='blue', label='Standard deviation')
plt.plot([exp_val - stand_dev] * 101, color='blue')
plt.legend(handles=[p1, p2, p3], loc='best')
# plt.savefig('pic1.jpg')

print('E = ', exp_val, '\nVar = ', var, '\nStand dev = ', stand_dev)


def R_k(k: int) -> float:
    """Correlation function"""
    return sum((inp[i] - exp_val)*(inp[i+k] - exp_val) for i in range(len(inp) - k)) / (len(inp) - k - 1)


def r_k(k: int) -> float:
    """Normalized correlation function"""
    return R_k(k) / R_k(0)


r = [r_k(i) for i in range(11)]

print('\ncorr func', [R_k(i) for i in range(11)])
print('\nnormalized corr func:', r)


plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(r, color='r', label='Source')
p2, = plt.plot([1 / math.exp(1)] * 11, color='blue', label='+1/e -1/e')
plt.plot([-1 / math.exp(1)] * 11, color='blue')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2])
# plt.savefig('pic2.jpg')


# Autoregressive Models

def AR_coef(M: int) -> np.array:
    R_k_l = [R_k(i) for i in range(M+1)]
    match M:
        case 0:
            return np.array([math.sqrt(R_k_l[0])])
        case 1:
            matrix = np.array([[R_k_l[1], 1.], [R_k_l[0], 0.]])
            vec = np.array([R_k_l[0], R_k_l[1]])
        case 2:
            matrix = np.array([
                [R_k_l[1], R_k_l[2], 1.],
                [R_k_l[0], R_k_l[2], 0.],
                [R_k_l[1], R_k_l[0], 0.]
            ])
            vec = np.array([R_k_l[0], R_k_l[1], R_k_l[2]])
        case 3:
            matrix = np.array([
                [R_k_l[1], R_k_l[2], R_k_l[3], 1.],
                [R_k_l[0], R_k_l[2], R_k_l[3], 0.],
                [R_k_l[1], R_k_l[0], R_k_l[3], 0.],
                [R_k_l[1], R_k_l[2], R_k_l[0], 0.]
            ])
            vec = np.array([R_k_l[0], R_k_l[1], R_k_l[2], R_k_l[3]])

    res = np.linalg.solve(matrix, vec)
    res[M] = math.sqrt(res[M])
    return res


def r_ar(M: int, i: int) -> float:
    """Corr function"""
    if M >= i:
        return r_k(i)
    elif M == 0 and i > 0:
        return 0
    beta = AR_coef(M)
    return sum([beta[j] * r_ar(M, i-j-1) for j in range(M)])


print('\nAR_coef: ', [list(AR_coef(i).round(4)) for i in range(4)])
# print('\nr_ar: ', [round(r_ar(3, i), 4) for i in range(11)])
print('\neps: ', [round(sum([pow(r_ar(j, i) - r_k(i), 2) for i in range(11)]), 8) for j in range(4)])

print(AR_coef(0))
