import matplotlib.pyplot as plt
import math

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
plt.savefig('pic1.jpg')

print('E = ', exp_val, 'Var = ', var, 'Stand dev = ', stand_dev)


def R_k(k: int) -> float:
    """Correlation function"""
    return sum((inp[i] - exp_val)*(inp[i+k] - exp_val) for i in range(len(inp) - k)) / (len(inp) - k - 1)


def r_k(k: int) -> float:
    """Normalized correlation function"""
    return R_k(k) / R_k(0)


# normalized corr function
r = [r_k(i) for i in range(11)]

print(r)
print([R_k(i) for i in range(11)])


plt.figure(figsize=(8, 5), dpi=80)
p1, = plt.plot(r, color='r', label='Source')
p2, = plt.plot([1 / math.exp(1)] * 11, color='blue', label='+1/e -1/e')
plt.plot([-1 / math.exp(1)] * 11, color='blue')
plt.xlabel("Index number")
plt.ylabel("Normalized correlation function")
plt.legend(handles=[p1, p2])
plt.savefig('pic2.jpg')
