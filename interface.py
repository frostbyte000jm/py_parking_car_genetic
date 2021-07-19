import pygame, math, random

from classes.sprites import Sprite
from classes.createBoard import createParkingSpots, createPlayerCar, createNPCCars

# initialize game
pygame.init()
bRunning = True

# set Screen Size
nScreenW = 800
nScreenH = 600
screen = pygame.display.set_mode((nScreenW, nScreenH))

# Title and Icon
pygame.display.set_caption("Parking A Car")

# background
background = pygame.image.load('graphics/parking spot/parkingLot.png')

# Create Game Board
rParkingSpot = createParkingSpots()
playerCar = createPlayerCar()
rNpcCar = createNPCCars(rParkingSpot)


def isCollision(npcCar, playCar):
    # print("npcCar",npcCar.rect, npcCar.angle%45, "playCar", playCar.rect,playCar.angle%45)

    doCollide = npcCar.rect.colliderect(playCar.rect)
    # print("doCollide",doCollide)
    if doCollide:
        npcCar.x += playCar.speed
        print("CRASH!!!")


def isParked(ps_rect, car_rect):
    # print("ps_rect", ps_rect, "car_rect", car_rect)
    doParked = ps_rect.contains(car_rect)
    if doParked:
        print("Parked!!!")


# declarations
player_xpos_change = 0.0
player_ypos_change = 0.0
nTurn = 0
nSpeed = 0
clock = pygame.time.Clock()

# Game Loop
while bRunning:

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            bRunning = False

        # key down
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("pressed escape")
                bRunning = False
            if event.key == pygame.K_UP:
                print("pressed Up")
                nSpeed = -playerCar.accel
                # playerCar.speed += playerCar.accel
            if event.key == pygame.K_DOWN:
                print("pressed Down")
                nSpeed = playerCar.accel
            if event.key == pygame.K_LEFT:
                print("pressed Left")
                nTurn = playerCar.turn

            if event.key == pygame.K_RIGHT:
                print("pressed Right")
                nTurn = -playerCar.turn

        # key up
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                nTurn = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                nSpeed = 0

    # move player car
    playerCar.speed = nSpeed
    nTurnVal = 0
    if nSpeed != 0:
        nTurnVal = nTurn
    else:
        nTurnVal = 0
    playerCar.angle += nTurnVal
    playerCar.x += playerCar.speed * math.sin(math.radians(playerCar.angle))
    playerCar.y += playerCar.speed * math.cos(math.radians(-playerCar.angle))
    # print("speed", playerCar.speed, "angle", playerCar.angle)

    # Check for collision
    for nc in rNpcCar:
        isCollision(nc, playerCar)

    # Check for Parked
    # print("Player Car - x:", playerCar.goal_x, "y:", playerCar.goal_y)
    # print("Player Car - x: ", playerCar.x, "y: ", playerCar.y, "rect: ", playerCar.rect, "surface: ", playerCar.surface, "angle:", playerCar.angle)

    for ps in rParkingSpot:
        # print("Parking Spot - x:", ps.x, "y: ", ps.y, "rect: ",ps.rect, "surface: ",ps.surface)
        isParked(ps.rect, playerCar.rect)

    # draw game
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for ps in rParkingSpot:
        rotated, topleft = ps.draw()
        screen.blit(rotated, topleft)
    rotated, topleft = playerCar.draw()
    screen.blit(rotated, topleft)
    for nc in rNpcCar:
        rotated, topleft = nc.draw()
        screen.blit(rotated, topleft)
    # screen.blit(imgParkingSpot,(imgParkingSpot_xpos,imgParkingSpot_ypos))
    pygame.display.flip()
    clock.tick(60)

    # player_xpos = min(max(player_xpos + player_xpos_change, 0), nScreenW - playerCarImgW)
    # player_ypos = min(max(player_ypos + player_ypos_change, 0), nScreenH - playerCarImgH)
    # player_pos(player_xpos, player_ypos)

    # Update Game
    # pygame.display.update()

# End Game
pygame.quit()
