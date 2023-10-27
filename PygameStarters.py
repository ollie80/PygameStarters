import pygame
import pyautogui

class CameraGroup(pygame.sprite.Group):
    def __init__(self, display_surf, screen):
        super().__init__()
        self.screen = screen
        self.display_surface = display_surf
        self.offset = vector()


    def custom_draw(self, player, mouse_rect):

        self.offset.x = player.rect.centerx - DISPLAY_WIDTH / 2
        self.offset.y = player.rect.centery - DISPLAY_HEIGHT / 2

        range_x = range(player.rect.centerx - WINDOW_WIDTH, player.rect.centerx + WINDOW_WIDTH)
        range_y = range(player.rect.centery - WINDOW_HEIGHT, player.rect.centery + WINDOW_HEIGHT)


        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.z):

            if sprite.rect.centerx in range_x and sprite.rect.centery in range_y:
                offset_rect = sprite.rect.copy()
                offset_rect.center -= self.offset
                self.display_surface.blit(sprite.image, offset_rect)


            self.screen.blit(pygame.transform.scale(self.display_surface, (self.screen.get_size())), (0, 0))

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group ,  z = LEVEL_LAYERS['main']):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Animated(Generic):
    def __init__(self, assets, pos, group, z = LEVEL_LAYERS['main']):
        self.animation_frames = assets
        self.frame_index = 0
        self.z = z
        super().__init__(pos, self.animation_frames[self.frame_index], group, z)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        self.frame_index = 0 if self.frame_index >= len(self.animation_frames) else self.frame_index
        self.image = self.animation_frames[int(self.frame_index)]


    def update(self, dt):
        self.animate(dt)

class Particle(Animated):
    def __init__(self, assets, pos, group):
        super().__init__(assets, pos, group, z = LEVEL_LAYERS['particles'])
        self.rect = self.image.get_rect(center = pos)

    def animate(self, dt):
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.animation_frames):
            self.image = self.animation_frames[int(self.frame_index)]
        else:
            self.kill()


def import_folder(path):
    surface_list = []

    for folder_name, sub_folders, img_files in walk(path):
        for image_name in img_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for folder_name, sub_folders, img_files in walk(path):
        for image_name in img_files:
            full_path = path + '/' + image_name
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image_name.split('.')[0]] = image_surf

    return surface_dict


def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.active = False
        self.start_time = 0

    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration:
            self.deactivate()

# settings
ZOOM = 4
TILE_SIZE = 32
WINDOW_WIDTH = size()[0]
WINDOW_HEIGHT = size()[1]
DISPLAY_WIDTH = WINDOW_WIDTH / ZOOM
DISPLAY_HEIGHT = WINDOW_HEIGHT / ZOOM

ANIMATION_SPEED = 8

LEVEL_LAYERS = {
	'main': 0
}





