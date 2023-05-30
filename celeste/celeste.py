import pygame
import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)

image = 'level1.png'
hitbox_color = (0,255,0,255)
bg_color = (0,0,0,255)


def get_hitbox_upper_corner(image) -> tuple:
    for x in range(0, image.get_width()):
        for y in range(0, image.get_height()):
            if image.get_at((x,y)) == hitbox_color:
                return (x,y)
    return (0,0)

# return tuple
def get_character_hitbox_dims(image) -> tuple:
    start_pos = get_hitbox_upper_corner(image)
    width = 0
    height = 0
    for x in range(start_pos[0], start_pos[0]+100):
        if image.get_at((x,start_pos[1])) != image.get_at((x+1,start_pos[1])):
            width = x - start_pos[0]
    
    for y in range(start_pos[1], start_pos[1]+200):
        if image.get_at((start_pos[0],y)) != image.get_at((start_pos[0],y+1)):
            height = y - start_pos[1]

    return(width, height)

def get_available_pixels(bg) -> np.ndarray:
    char_pos = get_hitbox_upper_corner(bg)
    char_dims = get_character_hitbox_dims(bg)
    
    mx = np.eye(bg.get_height(), bg.get_width())
    for y in range(bg.get_height()):
        for x in range(bg.get_width()):
            cur_color = bg.get_at((x,y))
            mx[y, x] = int(cur_color == bg_color)
            
    for y in range(char_pos[0]-2, char_pos[0]+char_dims[0]+3):
        for x in range(char_pos[1]-2, char_pos[1]+char_dims[1]+3):
            mx[y, x] = 1
            
    return mx 

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((1094,590))
    bg = pygame.image.load(image).convert()
    # bg_width = bg.get_width()
    # bg_height = bg.get_height()

    # test()
    # print(bg.get_width())
    # print(bg.get_height())
    # char_pos = get_hitbox_upper_corner(bg)
    # character_hitbox_dims = get_character_hitbox_dims(image=bg)
    # print(character_hitbox_dims)
    # print(character_hitbox_dims[0]/bg_width)
    # print(character_hitbox_dims[1]/bg_height)
    print(get_hitbox_upper_corner(bg))
    
    # grid = create_world_grid(char_pos, character_hitbox_dims, bg)
    # print(grid[:, char_pos[1]])
    # print(grid[0:5, 0:5])

    # matrix = get_available_pixels(bg)
    # print(matrix[:, char_pos[1]])
    # print(matrix[10,:])
    # print(type(matrix))
    # print(get_hitbox_upper_corner(bg))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg,(0,0))
        pygame.display.update()
        # print(pygame.mouse.get_pos())

if __name__ == '__main__':
    main()
