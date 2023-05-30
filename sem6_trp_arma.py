import matplotlib.pyplot as plt
import math
import numpy as np
import scipy
import random

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


R = [R_k(i) for i in range(101)]  # corr function of the source process
r = [r_k(i) for i in range(101)]  # normalized corr func of the source process

print('\ncorr func', R)
print('\nnormalized corr func:', r)

# corr interval
for i in range(len(inp)):
    if abs(r_k(i)) < math.exp(-1):
        print('corr interval ', i)
        break


plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(r, color='r', label='Source')
p2, = plt.plot([1 / math.exp(1)] * 11, color='blue', label='+1/e -1/e')
plt.plot([-1 / math.exp(1)] * 11, color='blue')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2])
# plt.savefig('pic2.jpg')


# Autoregressive Models

def AR_coef(M: int) -> np.ndarray:
    match M:
        case 0:
            return np.array([math.sqrt(R[0])])
        case 1:
            matrix = np.array([[R[1], 1.], [R[0], 0.]])
            vec = np.array([R[0], R[1]])
        case 2:
            matrix = np.array([
                [R[1], R[2], 1.],
                [R[0], R[2], 0.],
                [R[1], R[0], 0.]
            ])
            vec = np.array([R[0], R[1], R[2]])
        case 3:
            matrix = np.array([
                [R[1], R[2], R[3], 1.],
                [R[0], R[2], R[3], 0.],
                [R[1], R[0], R[3], 0.],
                [R[1], R[2], R[0], 0.]
            ])
            vec = np.array([R[0], R[1], R[2], R[3]])

    res = np.linalg.solve(matrix, vec)
    res[M] = math.sqrt(res[M])
    return res


def r_ar(M: int, i: int) -> float:
    """theoretical corr function"""
    if M >= i:
        return r[i]
    elif M == 0 and i > 0:
        return 0
    beta = AR_coef(M)
    return sum([beta[j] * r_ar(M, i-j-1) for j in range(M)])


print('\nAR_coef: ', [list(AR_coef(i).round(4)) for i in range(4)])
# print('\nr_ar: ', [round(r_ar(3, i), 4) for i in range(11)])
print('\nar eps: ', [round(sum([pow(r_ar(j, i) - r[i], 2) for i in range(11)]), 8) for j in range(4)])


# Moving-Average Models

def cc1(x):
    return np.array([
                    x[0]*x[0]+x[1]*x[1]-R[0],
                    x[0]*x[1]-R[1]
                    ])


def cc2(x):
    return np.array([
                    x[0]*x[0]+x[1]*x[1]+x[2]*x[2]-R[0],
                    x[0]*x[1]+x[1]*x[2]-R[1],
                    x[0]*x[2]-R[2]
                    ])


def cc3(x):
    return np.array([
                    x[0]*x[0]+x[1]*x[1]+x[2]*x[2]+x[3]*x[3]-R[0],
                    x[0]*x[1]+x[1]*x[2]+x[2]*x[3]-R[1],
                    x[0]*x[2]+x[1]*x[3]-R[2],
                    x[0]*x[3]-R[3]
                    ])


print(f'0: {math.sqrt(R[0])}')
for i, cc_func in enumerate([cc1, cc2, cc3]):
    if scipy.optimize.root(cc_func, np.zeros(i+2)).success:
        print(f'{i+1}: {scipy.optimize.fsolve(cc_func, np.zeros(i+2))}')


def r_cc(N: int, i: int) -> float:
    """theoretical corr function"""
    return r[i] if N >= i else 0


for N in range(4):
    print([r_cc(N, i) for i in range(11)])

print('\ncc eps: ', [round(sum([pow(r_cc(j, i) - r[i], 2) for i in range(11)]), 8) for j in range(4)])

# ARMA
# Build mixed models of autoregression - moving average АRMA(M, N)
# up to the third order inclusive (M = 1, 2, 3; N = 1, 2, 3) (total 9 models).


def arcc11(x):
    a0, a1, b0 = x
    F = np.zeros(3)
    F[0] = R[1]*b0 + a0*a0 + a1*(b0*a0 + a0) - R[0]
    F[1] = R[0]*b0 + a1*a0 - R[1]
    F[2] = b0*R[1] - R[2]
    return F


def arcc12(x):
    a0, a1, a2, b0 = x
    F = np.zeros(4)
    F[0] = b0*R[1] + a0*a0 + a1*(b0*a0 + a0) + a2*(b0*(b0*a0 + a0) + a0) - R[0]
    F[1] = b0*R[0] + a1*a0 + a2*(b0*a0 + a0) - R[1]
    F[2] = b0*R[1] + a2*a0 - R[2]
    F[3] = b0*R[2] - R[3]
    return F


def arcc13(x):
    a0, a1, a2, a3, b0 = x[0], x[1], x[2], x[3], x[4]
    F = np.zeros(9)
    F[0] = b0*R[1] + a0*a0 + a1*x[6] + a2*x[7] + a3*x[8] - R[0]
    F[1] = b0*R[0] + a1*a0 + a2*x[6] + a3*x[7] - R[1]
    F[2] = b0*R[1] + a2*a0 + a3*x[6] - R[2]
    F[3] = b0*R[2] + a3*a0 - R[3]
    F[4] = b0*R[3] - R[4]
    F[5] = a0 - x[5]
    F[6] = b0*a0 + a0 - x[6]
    F[7] = b0*(b0*a0 + a0) + a0 - x[7]
    F[8] = b0*(b0*(b0*a0 + a0) + a0) + a0 - x[8]
    return F


def arcc21(x):
    F = np.zeros(6)
    F[0] = x[2]*R[1] + x[3]*R[2] + x[0]*x[4] + x[1]*x[5] - R[0]
    F[1] = x[2]*R[0] + x[3]*R[1] + x[1]*x[4] - R[1]
    F[2] = x[2]*R[1] + x[3]*R[0] - R[2]
    F[3] = x[2]*R[2] + x[3]*R[1] - R[3]
    F[4] = x[0] - x[4]
    F[5] = x[2]*x[4] + x[0] - x[5]
    return F


def arcc22(x):
    F = np.zeros(8)
    F[0] = x[3]*R[1] + x[4]*R[2] + x[0]*x[5] + x[1]*x[6] + x[2]*x[7] - R[0]
    F[1] = x[3]*R[0] + x[4]*R[1] + x[1]*x[5] + x[2]*x[6] - R[1]
    F[2] = x[3]*R[1] + x[4]*R[0] + x[2]*x[5] - R[2]
    F[3] = x[3]*R[2] + x[4]*R[1] - R[3]
    F[4] = x[3]*R[3] + x[4]*R[2] - R[4]
    F[5] = x[0] - x[5]
    F[6] = x[3]*x[5] + x[0] - x[6]
    F[7] = x[3]*x[6] + x[4]*x[5] + x[0] - x[7]
    return F


def arcc23(x):
    return [
        x[4]*R[1] + x[5]*R[2] + x[0]*x[6] + x[1]*x[7] + x[2]*x[8] + x[3]*x[9] - R[0],
        x[4]*R[0] + x[5]*R[1] + x[1]*x[6] + x[2]*x[7] + x[3]*x[8] - R[1],
        x[4]*R[1] + x[5]*R[0] + x[2]*x[6] + x[3]*x[7] - R[2],
        x[4]*R[2] + x[5]*R[1] + x[3]*x[6] - R[3],
        x[4]*R[3] + x[5]*R[2] - R[4],
        x[4]*R[4] + x[5]*R[3] - R[5],
        x[0] - x[6],
        x[4]*x[6] + x[0] - x[7],
        x[4]*x[7] + x[5]*x[6] + x[0] - x[8],
        x[4]*x[8] + x[5]*x[7] + x[0] - x[9],
    ]


def arcc31(x):
    return [
        x[2]*R[1] + x[3]*R[2] + x[4]*R[3] + x[0]*x[5] + x[1]*x[6] - R[0],
        x[2]*R[0] + x[3]*R[1] + x[4]*R[2] + x[1]*x[5] - R[1],
        x[2]*R[1] + x[3]*R[0] + x[4]*R[1] - R[2],
        x[2]*R[2] + x[3]*R[1] + x[4]*R[0] - R[3],
        x[2]*R[3] + x[3]*R[2] + x[4]*R[1] - R[4],
        x[0] - x[5],
        x[2]*x[5] + x[0] - x[6],
    ]


def arcc32(x):
    return [
        x[3]*R[1] + x[4]*R[2] + x[5]*R[3] + x[0]*x[6] + x[1]*x[7] + x[2]*x[8] - R[0],
        x[3]*R[0] + x[4]*R[1] + x[5]*R[2] + x[1]*x[6] + x[2]*x[7] - R[1],
        x[3]*R[1] + x[4]*R[0] + x[5]*R[1] + x[2]*x[6] - R[2],
        x[3]*R[2] + x[4]*R[1] + x[5]*R[0] - R[3],
        x[3]*R[3] + x[4]*R[2] + x[5]*R[1] - R[4],
        x[3]*R[4] + x[4]*R[3] + x[5]*R[2] - R[5],
        x[0] - x[6],
        x[3]*x[6] + x[0] - x[7],
        x[3]*x[7] + x[2]*x[6] + x[0] - x[8],
    ]


def arcc33(x):
    return [
        x[4]*R[1] + x[5]*R[2] + x[6]*R[3] + x[0]*x[7] + x[1]*x[8] + x[2]*x[9] + x[3]*x[10] - R[0],
        x[4]*R[0] + x[5]*R[1] + x[6]*R[2] + x[1]*x[7] + x[2]*x[8] + x[3]*x[9] - R[1],
        x[4]*R[1] + x[5]*R[0] + x[6]*R[1] + x[2]*x[7] + x[3]*x[8] - R[2],
        x[4]*R[2] + x[5]*R[1] + x[6]*R[0] + x[3]*x[7] - R[3],
        x[4]*R[3] + x[5]*R[2] + x[6]*R[1] - R[4],
        x[4]*R[4] + x[5]*R[3] + x[6]*R[2] - R[5],
        x[4]*R[5] + x[5]*R[4] + x[6]*R[3] - R[6],
        x[0] - x[7],
        x[4]*x[7] + x[0] - x[8],
        x[4]*x[8] + x[5]*x[7] + x[0] - x[9],
        x[4]*x[9] + x[5]*x[8] + x[6]*x[7] + x[0] - x[10],
    ]


def check_model(model_func, x):
    print(f'\n{model_func.__name__}: \
    {scipy.optimize.root(model_func, x).success} \
    {scipy.optimize.fsolve(model_func, x).round(3)}')


R_0_sqrt = math.sqrt(R[0])

check_model(arcc11, np.zeros(3))
check_model(arcc12, np.zeros(4))
check_model(arcc13, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0, 0, 0]))

check_model(arcc21, np.array([R_0_sqrt, 0, 0, 0, 0, 0]))
check_model(arcc22, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0, 0]))
check_model(arcc23, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

check_model(arcc31, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0]))
check_model(arcc32, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0, 0, 0]))
check_model(arcc33, np.array([R_0_sqrt, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))


def r_arcc12(i) -> float:
    return r[i] if i < 5 else -0.515 * r_arcc12(i-1)


def r_arcc13(i) -> float:
    return r[i] if i < 5 else -0.061 * r_arcc13(i-1)


def r_arcc21(i) -> float:
    return r[i] if i < 4 else -0.41 * r_arcc21(i - 1) - 0.41 * r_arcc21(i - 2)


def r_arcc22(i) -> float:
    return r[i] if i < 4 else -0.462 * r_arcc22(i - 1) - 0.207 * r_arcc22(i - 2)


for r_func in [r_arcc12, r_arcc13, r_arcc21, r_arcc22]:
    print(round(sum([pow(r_func(i) - r[i], 2) for i in range(11)]), 6))

# Comparative analysis of the constructed models

e = [random.uniform(-250, 250) for _ in range(7000)]
ar3 = [0] * 6000
ma2 = [0] * 6000
arma13 = [0] * 6000

coef_ar3 = [-0.247, -0.3985, 0.0197, 16.5102]  # b1, b2, b3, a0
coef_ma2 = [7.63427093, 3.73419945, -16.07115135]  # a0, a1, a2
coef_arma13 = [-0.061, 18.625, 5.488, -9.5, 2.992]  # b1, a0, a1, a2, a3

for i in range(3, 6000):
    ar3[i] = coef_ar3[0] * ar3[i-1] + coef_ar3[1] * ar3[i-2] + coef_ar3[2] * ar3[i-3] + coef_ar3[3] * e[i]
    ma2[i] = coef_ma2[0] * e[i] + coef_ma2[1] * e[i-1] + coef_ma2[2] * e[i-2]
    arma13[i] = coef_arma13[0] * arma13[i-1] + coef_arma13[1] * e[i] + coef_arma13[2] * e[i-1] + coef_arma13[3] * e[i-2] + coef_arma13[4] * e[i-3]


# print(ma2)

def R_k_n(k: int, rp) -> float:
    expected_val = 0
    for i in range(len(rp)):
        expected_val += rp[i]
    expected_val = expected_val/len(rp)
    a = 0
    for i in range(len(rp) - k):
        a += (rp[i] - expected_val)*(rp[i+k] - expected_val)
    a = a / (len(rp) - k)
    return a


R_n1 = [R_k_n(i, ar3[1000:]) for i in range(len(ar3[1000:]))]
R_n2 = [R_k_n(i, ma2[1000:]) for i in range(len(ar3[1000:]))]
R_n3 = [R_k_n(i, arma13[1000:]) for i in range(len(ar3[1000:]))]


# TODO remove this func
def r_k_n(k: int, n) -> float:
    if n == 1:
        return R_n1[k]/R_n1[0]
    elif n == 2:
        return R_n2[k]/R_n2[0]
    return R_n3[k]/R_n3[0]


r1 = [r_k_n(i, 1) for i in range(101)]
r2 = [r_k_n(i, 2) for i in range(101)]
r3 = [r_k_n(i, 3) for i in range(101)]


# print(R_n2)
r1_t = []
for i in range(101):
    if i <= 3:
        r1_t.append(r[i])
    else:
        beta = coef_ar3
        res = 0
        for j in range(3):
            res += beta[j]*r1_t[i-j-1]
        r1_t.append(res)

r2_t = [r_cc(2, i) for i in range(101)]
# r2_t = []
# for i in range(101):
#     r
# print(r2_t)
r3_t = []
for i in range(101):
    r3_t.append(r[i] if i < 5 else -0.061 * r3_t[i-1])

plt.figure(figsize=(8, 5), dpi=80)
ax = plt.subplot(111)
p1, = plt.plot(r[:101], color='r', label='Source')
p2, = plt.plot(r1[:101], color='b', label='ARMA(3, 0)')
p3, = plt.plot(r1_t[:101], color='g', label='Imitation')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2, p3])
plt.savefig('pic3.jpg')

plt.figure(figsize=(8, 5), dpi=80)
ax = plt.subplot(111)
p1, = plt.plot(r[:101], color='r', label='Source')
p2, = plt.plot(r2[:101], color='blue', label='ARMA(0, 2)')
p3, = plt.plot(r2_t[:101], color='green', label='Imitation')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2, p3])
plt.savefig('pic4.jpg')

plt.figure(figsize=(8, 5), dpi=80)
ax = plt.subplot(111)
p1, = plt.plot(r[:101], color='r', label='Source')
p2, = plt.plot(r3[:101], color='blue', label='ARMA(1, 3)')
p3, = plt.plot(r3_t[:101], color='green', label='Imitation')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2, p3])
plt.savefig('pic5.jpg')

