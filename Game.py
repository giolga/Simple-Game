import pygame
from pygame.locals import *
import random

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame")


pygame.init()


#creating window
width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car game')


#colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)


#game settings
gameOver = False
speed = 2
score = 0


#markers size
marker_width = 10
marker_height = 50


#road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)


#x coordinates of lane
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]


#for animating movement of the Lane markers
lane_marker_move_y = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        #scaling img down so it fits in the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale    
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('Games/images/Car.png')
        super().__init__(image, x, y)


#player's starting coordinates
player_x = 250
player_y = 400

#create a player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)


#load other vehicles
image_filenames = ['Ambulance.png', 'Audi.png', 'Black_viper.png', 'Mini_truck.png' ,'Mini_van.png', 'Police.png', 'taxi.png', 'truck.png']
vehicle_images = []

for image_filename in image_filenames:
    image = pygame.image.load(f"Games/images/{image_filename}")
    vehicle_images.append(image)


#sprite gorup for vehicles
vehicle_group = pygame.sprite.Group()


#game loop
clock = pygame.time.Clock()
fps = 120
running = True

while running:
    clock.tick(fps)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        #moving player's car using left/right arrow keys
        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100


    pygame.display.update()

    #draw grass
    screen.fill(green)

    #drawing road
    pygame.draw.rect(screen, gray, road)

    #draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    #drawing lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0

    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
    
    #draw the player's car
    player_group.draw(screen)

    #add up to two vehicles
    if len(vehicle_group ) < 2:
        #ensure there's enoguh gap between cars
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.heigth * 1.5:
                add_vehicle = False
            
            if add_vehicle:
                #select a random Lane
                lane = random.choice(lanes)

                #select a random vehicla img
                image = random.choice(vehicle_images)
                vehicle = Vehicle(image, lane, height / 2)
                vehicle_group.add(vehicle)

    #make vehicle move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed

        #remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()

            #add a score
            score += 1

            #speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 1

    #draw the vehicle
    vehicle_group.draw(screen)

    pygame.display.update()

pygame.quit()