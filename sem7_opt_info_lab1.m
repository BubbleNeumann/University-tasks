beta = 0.1;
n = 1000;
m = 1000;

a = 0; b = 5; ## input scope
p = 0; q = 5; ## output scope
hx = (b-a)/n;
x = a:hx:(b-hx/2);
hxi = (q-p)/m;
xi = p:hxi:(q-hxi/2);
[X, XI] = meshgrid(x, xi);
f = exp(i*beta*x); ## input signal (task 1)

alpha = 10;
K = i*besselj(alpha,X).*XI; ## kernel (task 2)
F = K*f.'*hx ## output signal (transformation result)

figure(1)
plot(x, abs(f)); ## amplitude

figure(2)
plot(x, arg(f)); ## phase

figure(3);
plot(xi, abs(F)); ## amplitude

figure(4);
plot(xi, arg(F)); ## phase
