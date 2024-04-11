##Получить продольное распределение интенсивности светового поля (вдоль оси z
##при r=0) в фокусе апланатического объектива при фокусировке радиально-
##поляризованного света l = 1 с длиной волны 0,532 мкм в воздухе (n = 1). Вычисления
##произвести для значений числовой апертуры NA равной 0,65, 0,8 и 0,95. Оценить вклад
##числовой апертуры в уменьшение размеров фокусного пятна.

close all;
clear;

r = 0;
l = 1;
h = 0.532; %мкм
n = 1;
NA = [ 0.65, 0.8, 0.95]; %апертуры по условию
psi = 0;
k=2*pi/h; %волновое число
N = 150; % количество разбиений интеграла

z = linspace(-1, 1, N);
y = linspace(-1, 1, N);

A = 1;

T = @(tetha) cos(tetha).^0.5;

f_x_1 = @(r, z, psi, tetha)l*T(tetha)*sin(tetha)*(1-cos(tetha))*exp(i*k*z*cos(tetha))*besselj(2, k*r*sin(tetha));
f_x_2 = @(r, z, psi, tetha) l*T(tetha)*sin(tetha)*(1+cos(tetha))*exp(i*k*z*cos(tetha))*besselj(0, k*r*sin(tetha));
f_y = @(r, z, psi, tetha) l*T(tetha)*sin(tetha)*(1-cos(tetha))*exp(i*k*z*cos(tetha))*besselj(2, k*r*sin(tetha));
f_z = @(r, z, psi, tetha) l*T(tetha)*sin(tetha)^2*exp(i*k*z*cos(tetha))*besselj(1, k*r*sin(tetha));

for aperture_i = NA
        alpha = asin(aperture_i / n);

        %Интегрируем все функции
        integral_x_1 = integral(@(tetha)f_x_1(r, z, psi, tetha),  0, alpha,'ArrayValued', true);
        integral_x_2 = integral(@(tetha)f_x_2(r, z, psi, tetha),  0, alpha,'ArrayValued', true);
        integral_y = integral(@(tetha)f_y(r, z, psi, tetha), 0, alpha,'ArrayValued', true);
        integral_z = integral(@(tetha)f_z(r, z, psi, tetha), 0, alpha,'ArrayValued', true);
        %домножаем на коэффициенты
        E_x = -i*A*cos(2*psi)*integral_x_1 - i*A*integral_x_2;
        E_y = -i*A*sin(2*psi)*integral_y;
        E_z = -2*A*sin(psi)*integral_z;
        %находим интенсивности
        I_x = abs(E_x).^2;
        I_y = abs(E_y).^2;
        I_z = abs(E_z).^2;
        I = I_x + I_y + I_z;

        % вычисляем минимум и максимумы
        % для отображения всех графиков на 1 масштабе
        max_val = max(I(:));
        min_val = min(I(:));

        figure;
        colormap jet;
        imagesc(z, y, I, [min_val,max_val]);
        title(sprintf('{I}, NA = %.2f', aperture_i));
        xlabel('y, мкм');
        ylabel('z, мкм');
        colorbar;
        axis('xy');

##        figure;
##        imagesc(z, y, I_x, [min_val,max_val]);
##        title(sprintf('{I_x}, NA = %.2f', aperture_i));
##        xlabel('x, мкм');
##        ylabel('y, мкм');
##        colorbar;
##        axis('xy');
##
##        figure;
##        colormap jet;
##        imagesc(z, y, I_y, [min_val,max_val]);
##        title(sprintf('{I_y}, NA = %.2f', aperture_i));
##        xlabel('x, мкм');
##        ylabel('y, мкм');
##        colorbar;
##        axis('xy');
##
##        figure;
##        colormap jet;
##        imagesc(z, y, I_z, [min_val,max_val]);
##        title(sprintf('{I_z}, NA = %.2f', aperture_i));
##        xlabel('x, мкм');
##        ylabel('y, мкм');
##        colorbar;
##        axis('xy');

 end
