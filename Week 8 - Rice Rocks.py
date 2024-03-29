# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
in_game = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.speed = 1
        
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
        
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [130, 45], self.image_size, self.pos, self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        #Angle
        self.angle += self.angle_vel
        
        #Position and velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        #Friction
        pressed = 0.10 / 60
        unpressed = 0.03
        self.vel[0] *= (1 - pressed)
        self.vel[1] *= (1 - pressed)
        
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.vel[0] += unpressed * forward[0]
            self.vel[1] += unpressed * forward[1]
            
    #Missiles
    def shoot(self):
        moving_ahead = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * moving_ahead[0], self.pos[1] + self.radius * moving_ahead[1]]
        missile_vel = [self.vel[0] + 7 * moving_ahead[0], self.vel[1] + 7 * moving_ahead[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))
            
    #Thrust sound   
    def thrust_updates(self, thrusting):
        self.thrust = thrusting
        if thrusting:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
    #Anglevel Increase
    def increase_anglevel(self):
        self.angle_vel += .03
    #Anglevel Decrease
    def decrease_anglevel(self):
        self.angle_vel -= .03
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
    
    def get_position(self):
        return self.pos

    def get_radius(self):
        return self.radius
   
    def draw(self, canvas):
        if self.animated:
            image_tile = (self.age % 20) // 1
            self.image_center = [self.image_center[0] + image_tile * self.image_size[0], self.image_center[1]]
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        #Angle
        self.angle += self.angle_vel
        
        #Position and Velocity
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % WIDTH
        
        #Increment age of sprite
        if self.lifespan:
            if self.age > self.lifespan:
                return True
            else:
                self.age += 1
        return False
    
    def collide(self, other_object):
        if dist(self.pos, other_object.get_position()) < self.radius + other_object.get_radius():
            return True
        else:
            return False        
           
def draw(canvas):
    global time, lives, score, rock_group, in_game
    
    #Animate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    #Draw and update ship and sprites
    my_ship.draw(canvas)
    process_sprite_group(canvas, rock_group)
    process_sprite_group(canvas, missile_group)
    process_sprite_group(canvas, explosion_group)
    
    #Update ship and sprites
    my_ship.update()
    
    #Draw collision
    
    if group_collide(rock_group, my_ship) > 0:
        lives -= 1
    score += (group_group_collide(missile_group, rock_group)*10)
    
    #Reset game
    
    if lives < 1:
        in_game = False
        rock_group = set([])
        soundtrack.pause()
        timer.stop()
    
    #Splash
    if not in_game:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    
    #Text and score
    canvas.draw_text('Lives: '+ str(lives), (50, 50), 36, "White","monospace")
    canvas.draw_text('Score: '+ str(score), (575, 50), 36, "White", "monospace")

#Key Handlers

def down(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrease_anglevel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increase_anglevel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust_updates(True)
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()

def up(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.increase_anglevel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrease_anglevel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust_updates(False)

#Mouse click handler (Starts game)

def click(pos):
    global in_game, score, lives
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    width_splash = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    width_splash = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    height_splash = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not in_game) and width_splash and height_splash:
        in_game = True
        score = 0
        lives = 3
        timer.start()
        soundtrack.rewind()
        soundtrack.play()
                                                          
                                                          
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group, in_game
    if len(rock_group) > 12 or not in_game:
        return
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_angvel = random.random() * .2 - .1
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    #Distance
    while dist(rock_pos, my_ship.pos) < 60:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        
    # Add rock
    
    rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_angvel, asteroid_image, asteroid_info))
    
#Collide

def group_collide(group, other_object):
    num_collisions = 0
    for explosion in set(group):
        if explosion.collide(other_object):
            explosion_group.add(Sprite(explosion.get_position(), (0, 0), 0, 0, explosion_image, explosion_info, explosion_sound))
            group.remove(explosion)
            num_collisions += 1
    return num_collisions

#Sprite group

def process_sprite_group(canvas, group):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)

def group_group_collide(group, second_group):
    total = 0
    for collide in set(group):
        count = group_collide(second_group, collide)
        if count > 0:
            group.remove(collide)
        total += count
    return total
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(down)
frame.set_keyup_handler(up)
frame.set_mouseclick_handler(click)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()