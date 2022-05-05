from random import randint
from PIL import Image
import numpy as np
import math

#1
# black picture
# image_matrix = np.zeros((200, 300), dtype=np.uint8)
# image = Image.fromarray(image_matrix, 'L')
# image.save('image-black.jpg')

# white picture
# image_matrix = np.full((200, 300), 255, dtype=np.uint8)
# image = Image.fromarray(image_matrix, 'L')
# image.save('image-white.jpg')

# red picture
# image_matrix = np.zeros((200, 300, 3), dtype=np.uint8)
# image_matrix[:, :, 0] = 255
# image = Image.fromarray(image_matrix, 'RGB')
# image.save('image-red.jpg')

# grad picture
# image_matrix = np.zeros((200, 300, 3), dtype=np.uint8)
# image_matrix[:, :, 0] = 255

# for i in range(200):
#     for j in range(300):
#         image_matrix[i,j,0] = (i)%256
#         image_matrix[i,j,1] = (j)%256
#         image_matrix[i,j,1] = (i+j)%256

# image = Image.fromarray(image_matrix, 'RGB')
# image.save('image-grad.jpg')  


def drawLine1(x1, y1, x2, y2, canvas):
    for t_i in range(100):
        t = 0.01*t_i
        x = int (x1 * t + x2 * (1.0 - t))
        y = int (y1 * t + y2 * (1.0 - t))
        canvas[y, x] = 0

def drawLine2(x1, y1, x2, y2, canvas):

    steep = False
    if abs(x1-x2)<abs(y1-y2):
        x1, x2, y1, y2 = y1, y2, x1, x2
        steep = True

    if x1 > x2:
        for x in range(x1, x2, -1):
            t = (x-x1)/(float)(x2-x1)
            y = int(y1*(1.0-t)+y2*t)
            if steep:
                canvas[y, x] = 0
            else:
                canvas[x, y] = 0
    else:
        for x in range(x1, x2):
            t = (x-x1)/(float)(x2-x1)
            y = int(y1*(1.0-t)+y2*t)
            if steep:
                canvas[y, x] = 0
            else:
                canvas[x, y] = 0

def drawLine4(x1, y1, x2, y2, canvas) -> None:
    
    x1 = int(x1)
    x2 = int(x2)
    y1 = int(y1)
    y2 = int(y2)
    steep = False
    if abs(x1-x2)<abs(y1-y2):
        x1, x2, y1, y2 = y1, y2, x1, x2
        steep = True
    
    dx = x2-x1
    dy = y2-y1
    if dx:
        derror = abs(dy/float(dx)) 
    error = 0
    y = y1   

    if x1 > x2:
        a = -1
    else:
        a = 1  
        
    for x in range(x1, x2, a):
        t = (x-x1)/(float)(x2-x1)
        y = int(y1*(1.0-t)+y2*t)
        if steep:
            canvas[x, y] = 0
        else:
            canvas[y, x] = 0
        error += derror
        if error > 0.5: 
            if y2>y1:
                y+=1
            else:
                y-=1
            error -=1

# 3
# img = np.full((201, 201), 255, dtype=np.uint8)

# for i in range(13):
#     drawLine1(100, 100, int(100+95*math.cos(i*2*math.pi/13)), int(100+95*math.sin(i*2*math.pi/13)), img)

# image = Image.fromarray(img, 'L')
# image.save('line1.png')

# img = np.full((201, 201), 255, dtype=np.uint8)
# for i in range(13):
#     drawLine2(100, 100, int(100+95*math.cos(i*2*math.pi/13)), int(100+95*math.sin(i*2*math.pi/13)), img)

# image = Image.fromarray(img, 'L')
# image.save('line2.png')

#img = np.full((201, 201), 255, dtype=np.uint8)
#for i in range(13):
#    drawLine4(100, 100, int(100+95*math.cos(i*2*math.pi/13)), int(100+95*math.sin(i*2*math.pi/13)), img)

#image = Image.fromarray(img, 'L')
#image.save('line4.png')


# 4
data = []
with open('deer.obj', 'r') as fileobj:
    lines = fileobj.readlines()
    for i in lines:
        if (len(i) > 1):
            data.append(i[:len(lines) - 1].split())
    
    del data[:3]

    fileobj.close()


# 5
# img = np.full((1000, 1000), 255, dtype=np.uint8)

# for point in data:
#     if point[0] == 'v':
#         x, y = int(float(point[1]) / 5) + 500, int(float(point[2]) / 5) + 500
#         img[x, y] = 0
#     else:
#         break

# image = Image.fromarray(img, 'L')
# image.save('points.png')

# 6
f = []
v = []
vt = []
for point in range(len(data)):
    if data[point][0] == 'v':
        xyz = []
        for i in range(1, 4):
            xyz.append(float(data[point][i]))
        v.append(xyz)

    elif data[point][0] == 'f':
        xyz = []
        for i in range(1, 4):
            x, y = data[point][i].split('/')
            xyz.append(int(x))
        f.append(xyz)
    elif data[point][0] == 'vt':
        xyz = []
        for i in range(1, 4):
            xyz.append(float(data[point][i]))
        vt.append(xyz)


# 7
#img = np.full((1000, 1000), 255, dtype=np.uint8)
#a = 3
#for i in f:
#    drawLine4(v[i[0] - 1][0] / a + 500, v[i[0] - 1][1] / -a + 500, v[i[1] - 1][0] / a + 500, v[i[1] - 1][1] / -a + 500, img)
#    drawLine4(v[i[1] - 1][0] / a + 500, v[i[1] - 1][1] / -a + 500, v[i[2] - 1][0] / a + 500, v[i[2] - 1][1] / -a + 500, img)
#    drawLine4(v[i[0] - 1][0] / a + 500, v[i[0] - 1][1] / -a + 500, v[i[2] - 1][0] / a + 500, v[i[2] - 1][1] / -a + 500, img)

#image = Image.fromarray(img, 'L')
#image.save('polygonaldeer.png')

# 8
def bar_coord(x, y, x0, y0, x1, y1, x2, y2):

    if ((x1 - x2)*(y0 - y2) - (y1 - y2)*(x0 - x2)):
        lambda1 = ((x1 - x2)*(y - y2) - (y1 - y2)*(x - x2)) / ((x1 - x2)*(y0 - y2) - (y1 - y2)*(x0 - x2))
    else:
        lambda1 = 0 
    
    if ((x2 - x0)*(y1 - y0) - (y2 - y0)*(x1 - x0)):
        lambda2 = ((x2 - x0)*(y - y0) - (y2 - y0)*(x - x0)) / ((x2 - x0)*(y1 - y0) - (y2 - y0)*(x1 - x0))
    else: 
        lambda2 = 0

    if ((x0 - x1)*(y2 - y1) - (y0 - y1)*(x2 - x1)):
        lambda3 = ((x0 - x1)*(y - y1) - (y0 - y1)*(x - x1)) / ((x0 - x1)*(y2 - y1) - (y0 - y1)*(x2 - x1))
    else:
        lambda3 = 0

    return lambda1, lambda2, lambda3

# 9
def draw_triangle(x0, y0, x1, y1, x2, y2, canvas, color):
   xmin = int(min(x0, x1, x2))
   ymin = int(min(y0, y1, y2))
   xmax = int(max(x0, x1, x2))
   ymax = int(max(y0, y1, y2))
   if (xmin < 0):
       xmin = 0
   if (xmax > len(canvas)):
       xmax = len(canvas) - 1
   if (ymin < 0):
       ymin = 0
   if (ymax > len(canvas)):
       ymax = len(canvas) - 1
   for x in range(xmin, xmax+1):
       for y in range(ymin, ymax+1):
           lambda1, lambda2, lambda3 = bar_coord(x, y, x0, y0, x1, y1, x2, y2)
           if (lambda1 >= 0 and lambda2 >= 0 and lambda3 >= 0):
               canvas[y, x] = color

# 10
# img = np.full((200, 200), 255, dtype=np.uint8)                
# draw_triangle(10.0, 25.0, 50.0, 55.0, 70.0, 10.0, img, 0)
# draw_triangle(90.0, 150.0, 100.0, 250.0, 110.0, 190.0, img, 115)
# image = Image.fromarray(img, 'L')
# image.save('triangle.png')


# 11

# a = 3
# img = np.full((1000, 1000), 255, dtype=np.uint8)  
# for i in f:
#     color = np.random.randint(0, 255)
#     draw_triangle(v[i[0] - 1][0] / a + 500, v[i[0] - 1][1] / -a + 500, v[i[1] - 1][0] / a + 500, v[i[1] - 1][1] / -a + 500, v[i[2] - 1][0] / a + 500, v[i[2] - 1][1] / -a + 500, img, color)
# image = Image.fromarray(img, 'L')
# image.save('triangledeer.png')

# 12

find_normal = lambda x0, y0, z0, x1, y1, z1, x2, y2, z2: np.cross([x1-x0, y1-y0, z1-z0], [x1-x2, y1-y2, z1-z2])

# 13
# calculates color value of given poligon

def find_scalar(x0, y0, z0, x1, y1, z1, x2, y2, z2):
    l = [0, 0, 1]
    n = find_normal(x0, y0, z0, x1, y1, z1, x2, y2, z2)
    return np.dot(n, l) / np.linalg.norm(n)


# 14
def draw_triangle_with_light(x0, y0, z0, x1, y1, z1, x2, y2, z2, canvas) -> None:

   scalar = find_scalar(x0, y0, z0, x1, y1, z1, x2, y2, z2)

   if (scalar > 0):
       return

   xmin = int(min(x0, x1, x2))
   ymin = int(min(y0, y1, y2))
   xmax = int(max(x0, x1, x2))
   ymax = int(max(y0, y1, y2))
   if (xmin < 0):
       xmin = 0
   if (xmax > len(canvas)):
       xmax = len(canvas) - 1
   if (ymin < 0):
       ymin = 0
   if (ymax > len(canvas)):
       ymax = len(canvas) - 1
   for x in range(xmin, xmax+1):
       for y in range(ymin, ymax+1):
           lambda1, lambda2, lambda3 = bar_coord(x, y, x0, y0, x1, y1, x2, y2)
           if (lambda1 >= 0 and lambda2 >= 0 and lambda3 >= 0):
               canvas[y, x] = -255*scalar

# a = 3
# img = np.full((1000, 1000), 255, dtype=np.uint8)  
# for i in f:
#   draw_triangle_with_light(v[i[0] - 1][0] / a + 500, v[i[0] - 1][1] / -a + 500, v[i[0] - 1][2] / a + 500, v[i[1] - 1][0] / a + 500, v[i[1] - 1][1] / -a + 500, v[i[1] - 1][2] / a + 500, v[i[2] - 1][0] / a + 500, v[i[2] - 1][1] / -a + 500, v[i[2] - 1][2] / a + 500, img)
# image = Image.fromarray(img, 'L')
# image.save('triangledeer2.png')

# 15
def draw_triangle_with_zbuffer2(firstvertice, secondvertice, thirdvertice, origin_first, origin_second, origin_third, canvas, zbuffer): 
    xmin = int(min(firstvertice[0], secondvertice[0], thirdvertice[0]))
    ymin = int(min(firstvertice[1], secondvertice[1], thirdvertice[1]))
    xmax = int(max(firstvertice[0], secondvertice[0], thirdvertice[0]))
    ymax = int(max(firstvertice[1], secondvertice[1], thirdvertice[1]))
    if (xmin < 0):
       xmin = 0
    if (xmax > len(canvas)):
       xmax = len(canvas) - 1
    if (ymin < 0):
       ymin = 0
    if (ymax > len(canvas)):
       ymax = len(canvas) - 1


    color = 255*find_scalar(origin_first[0], origin_first[1], origin_first[2], origin_second[0], origin_second[1], origin_second[2], origin_third[0], origin_third[1], origin_third[2])


    for x in range(xmin, xmax+1):
       for y in range(ymin, ymax+1):
        #    using new coords
           lambda1, lambda2, lambda3 = bar_coord(x, y, firstvertice[0], firstvertice[1], secondvertice[0], secondvertice[1], thirdvertice[0], thirdvertice[1])
           if (lambda1 >= 0 and lambda2 >= 0 and lambda3 >= 0):
               z = lambda1*origin_first[2] + lambda2*origin_second[2] + lambda3*origin_third[2]
               if z <= zbuffer[y, x]:
                   canvas[y, x] = color
                   zbuffer[y, x] = z

# a = 3
# img = np.full((1000, 1000), 255, dtype=np.uint8)  
# zbuffer = np.full(img.shape, np.inf, np.float64)
# for i in f:
#    draw_triangle_with_zbuffer2(v[i[0] - 1][0] / a + 500, v[i[0] - 1][1] / -a + 500, v[i[0] - 1][2] / a + 500, v[i[1] - 1][0] / a + 500, v[i[1] - 1][1] / -a + 500, v[i[1] - 1][2] / a + 500, v[i[2] - 1][0] / a + 500, v[i[2] - 1][1] / -a + 500, v[i[2] - 1][2] / a + 500, img, zbuffer)
# image = Image.fromarray(img, 'L')
# image.save('triangledeer3.png')

# 16
# scales an object on image
def projective_transform(x, y, z, ax, ay, canvas) -> list:
    matrix = [[ax, 0, canvas.shape[1] / 2],
              [0, ay, canvas.shape[0] / 1.5],
              [0, 0, 1]]
    coord = [x, y, 1]
    #res = np.dot(matrix, coord)
    #res /= z
    res = np.dot(matrix, coord)
    return res


# img = np.full((1000, 1000), 255, dtype=np.uint8)  
# zbuffer = np.full(img.shape, np.inf, np.float64)

# for i in f:

# #     # where v is list of all vertices and f is list of all poligons;

#     ax = 0.4
#     ay = -0.4

#     firsttriangle = projective_transform(v[i[0] - 1][0], v[i[0] - 1][1], v[i[0] - 1][2], ax, ay, img)
#     secondtriangle = projective_transform(v[i[1] - 1][0], v[i[1] - 1][1], v[i[1] - 1][2], ax, ay, img)
#     thirdtriangle = projective_transform(v[i[2] - 1][0], v[i[2] - 1][1], v[i[2] - 1][2], ax, ay, img)


#     print(firsttriangle, secondtriangle, thirdtriangle)
# #     # print(firsttriangle)#,secondtriangle, thirdtriangle)
# #     draw_triangle_with_zbuffer(firsttriangle[0], firsttriangle[1], firsttriangle[2], secondtriangle[0], secondtriangle[1], secondtriangle[2], thirdtriangle[0], thirdtriangle[1], thirdtriangle[2], img, zbuffer)
# #     # draw_triangle_with_light(firsttriangle[0], firsttriangle[1], firsttriangle[2], secondtriangle[0], secondtriangle[1], secondtriangle[2], thirdtriangle[0], thirdtriangle[1], thirdtriangle[2], img)
    
#     if (firsttriangle[0] > 0 and firsttriangle[1] > 0 and secondtriangle[0] > 0 and secondtriangle[1] > 0 and thirdtriangle[0] > 0 and thirdtriangle[1] > 0):
#         draw_triangle_with_zbuffer2(firsttriangle, secondtriangle, thirdtriangle, v[i[0] - 1], v[i[1] - 1], v[i[2] - 1], img, zbuffer)
#     print('---')

# image = Image.fromarray(img, 'L')
# image.save('triangledeerwithtransformedcoords.png')



# 17
def rotate(point: list, alpha: int, beta: int, gamma: int) -> list:
    R1 = np.array([[1, 0, 0], [0, math.cos(alpha), math.sin(alpha)], [0, -math.sin(alpha), math.cos(alpha)]])
    R2 = np.array([[math.cos(beta), 0, math.sin(beta)], [0, 1, 0], [-math.sin(beta), 0, math.cos(beta)]])
    R3 = np.array([[math.cos(gamma), math.sin(gamma), 0], [-math.sin(gamma), math.cos(gamma), 0], [0, 0, 1]])
    R4 = np.dot(R1, R2)
    rotate_matrix = np.dot(R4, R3)
    res = np.dot(rotate_matrix, point)
    return res



# img = np.full((1000, 1000), 255, dtype=np.uint8)  
# zbuffer = np.full(img.shape, np.inf, np.float64)

# for i in f:
#     # where v is list of all vertices and f is list of all poligons;

#     ax = 0.4
#     ay = -0.4
#     rotated_first = rotate(v[i[0] - 1], 0, 30, 0)
#     rotated_second = rotate(v[i[1] - 1], 0, 30, 0)
#     rotated_third = rotate(v[i[2] - 1], 0, 30, 0)


#     firsttriangle = projective_transform(rotated_first[0], rotated_first[1], rotated_first[2], ax, ay, img)
#     secondtriangle = projective_transform(rotated_second[0], rotated_second[1], rotated_second[2], ax, ay, img)
#     thirdtriangle = projective_transform(rotated_third[0], rotated_third[1], rotated_third[2], ax, ay, img)
    
#     if (firsttriangle[0] > 0 and firsttriangle[1] > 0 and secondtriangle[0] > 0 and secondtriangle[1] > 0 and thirdtriangle[0] > 0 and thirdtriangle[1] > 0):
#         draw_triangle_with_zbuffer2(firsttriangle, secondtriangle, thirdtriangle, rotated_first, rotated_second, rotated_third, img, zbuffer)
    

# image = Image.fromarray(img, 'L')
# image.save('rotateddeer.png')

# 18
def shading_color(h1, h2, h3, normal) -> int:
    light_source = [0, 0, 1]
    light_source_norm = np.linalg.norm(light_source)
    l1 = np.cross(normal[0], light_source) / (np.linalg.norm(normal[0]) * light_source_norm)
    l2 = np.cross(normal[1], light_source) / (np.linalg.norm(normal[1]) * light_source_norm)
    l3 = np.cross(normal[2], light_source) / (np.linalg.norm(normal[2]) * light_source_norm)
    color = np.linalg.norm(255*(h1*l1 + h2*l2 + h3*l3))
    return color

def draw_triangle_with_zbuffer3(firstvertice, secondvertice, thirdvertice, origin_first, origin_second, origin_third, canvas, zbuffer, normals): 
    xmin = int(min(firstvertice[0], secondvertice[0], thirdvertice[0]))
    ymin = int(min(firstvertice[1], secondvertice[1], thirdvertice[1]))
    xmax = int(max(firstvertice[0], secondvertice[0], thirdvertice[0]))
    ymax = int(max(firstvertice[1], secondvertice[1], thirdvertice[1]))
    if (xmin < 0):
       xmin = 0
    if (xmax > len(canvas)):
       xmax = len(canvas) - 1
    if (ymin < 0):
       ymin = 0
    if (ymax > len(canvas)):
       ymax = len(canvas) - 1

    for x in range(xmin, xmax+1):
       for y in range(ymin, ymax+1):
        #    using new coords
           lambda1, lambda2, lambda3 = bar_coord(x, y, firstvertice[0], firstvertice[1], secondvertice[0], secondvertice[1], thirdvertice[0], thirdvertice[1])
           if (lambda1 >= 0 and lambda2 >= 0 and lambda3 >= 0):
               z = lambda1*origin_first[2] + lambda2*origin_second[2] + lambda3*origin_third[2]
               if z <= zbuffer[y, x]:
                   canvas[y, x] = shading_color(lambda1, lambda2, lambda3, normals)
                   zbuffer[y, x] = z


img = np.full((1000, 1000), 255, dtype=np.uint8)  
zbuffer = np.full(img.shape, np.inf, np.float64)

for i in f:
    # where v is list of all vertices and f is list of all poligons;

    ax = 0.4
    ay = -0.4
    firsttriangle = projective_transform(v[i[0] - 1][0], v[i[0] - 1][1], v[i[0] - 1][2], ax, ay, img)
    secondtriangle = projective_transform(v[i[1] - 1][0], v[i[1] - 1][1], v[i[1] - 1][2], ax, ay, img)
    thirdtriangle = projective_transform(v[i[2] - 1][0], v[i[2] - 1][1], v[i[2] - 1][2], ax, ay, img)
    normals = [ vt[i[0] - 1], vt[i[1] - 1], vt[i[2] - 1]]
    if (firsttriangle[0] > 0 and firsttriangle[1] > 0 and secondtriangle[0] > 0 and secondtriangle[1] > 0 and thirdtriangle[0] > 0 and thirdtriangle[1] > 0):
        draw_triangle_with_zbuffer3(firsttriangle, secondtriangle, thirdtriangle, v[i[0] - 1], v[i[1] - 1], v[i[2] - 1], img, zbuffer, normals)
    

image = Image.fromarray(img, 'L')
image.save('shadedddeer.png')