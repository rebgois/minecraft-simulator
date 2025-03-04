from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()
window.borderless = False
mouse.locked = True  # Trava o mouse no centro da tela

# Carregando texturas
grass_texture = load_texture('textures/grass_block.png')
stone_texture = load_texture('textures/stone_block.png')
brick_texture = load_texture('textures/brick_block.png')
sky_texture = load_texture('textures/skybox.png')
arm_texture = load_texture('textures/arm_texture.png')
punch_sound = Audio('textures/punch_sound.wav', loop=False, autoplay=False)

# Classe para blocos
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture=texture,
            color=color.color(0,0,random.uniform(0.9,1)),
            scale=1,
            highlight_color=color.lime
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                destroy(self)
            elif key == 'right mouse down':
                punch_sound.play()
                voxel = Voxel(position=self.position + mouse.normal, texture=stone_texture)

# Classe para o projétil
class Bullet(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            color=color.yellow,
            scale=0.2,
            position=position,
            collider='sphere'
        )
        self.direction = direction
        self.speed = 30
        self.lifetime = 0
        self.max_lifetime = 2  # Destruir após 2 segundos

    def update(self):
        self.lifetime += time.dt
        if self.lifetime > self.max_lifetime:
            destroy(self)
            return

        self.position += self.direction * self.speed * time.dt
        hit_info = raycast(self.position, self.direction, distance=0.5)
        if hit_info.hit:
            if isinstance(hit_info.entity, Voxel):
                destroy(hit_info.entity)
                punch_sound.play()
            destroy(self)

# Classe para a arma
class Gun(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='cube',
            texture=arm_texture,
            scale=(0.2, 0.15, 1),
            position=(0.6, -0.5),
            rotation=(0, -5, 0),
            color=color.white
        )
        self.cooldown = 0
        self.cooldown_time = 0.2  # Tempo entre tiros

    def update(self):
        if self.cooldown > 0:
            self.cooldown -= time.dt

    def input(self, key):
        if key == 'left mouse down' and self.cooldown <= 0:
            self.shoot()
            self.cooldown = self.cooldown_time

    def shoot(self):
        bullet = Bullet(
            position=player.position + Vec3(0, 1.5, 0),
            direction=camera.forward
        )
        punch_sound.play()
        # Efeito de recuo
        self.animate_position(self.position + Vec3(0, 0, 0.1), duration=0.1)
        self.animate_position(self.position, duration=0.1, delay=0.1)

# Criando o cenário
for z in range(-20, 20):
    for x in range(-20, 20):
        voxel = Voxel(position=(x, 0, z))

# Adicionando algumas paredes para ter alvos
for x in range(-5, 6):
    for y in range(1, 4):
        voxel = Voxel(position=(x, y, 5), texture=brick_texture)

player = FirstPersonController(speed=10)
gun = Gun()
Sky(texture=sky_texture)

# Configurações da janela
window.fps_counter.enabled = True
window.exit_button.visible = False
window.fullscreen = True

def input(key):
    if key == 'escape':
        mouse.locked = not mouse.locked

def update():
    if held_keys['escape']:
        quit()

app.run() 