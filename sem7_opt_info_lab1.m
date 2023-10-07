beta = 0.1;
n = 1000;
m = 1000;
p = 0;
q = 5;
a = 0;
b = 10;
hx = (b-a)/n;
x = a:hx:(b-hx/2);
hxi = (q-p)/m;
xi = p:hxi:(q-hxi/2);
[X, XI] = meshgrid(x, xi);
f = exp(i*beta*x);

alpha = 1;
J = i*besselj(alpha,X).*XI;
F = J*f.'*hx

figure(1)
plot(x, abs(f));
grid on;
figure(2)
plot(x, arg(f));
grid on;
figure(3);
plot(xi, abs(F));
grid on;
figure(4);
plot(xi, arg(F));
grid on;
