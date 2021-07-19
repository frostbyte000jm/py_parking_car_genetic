import pygame, math

from classes.createBoard import createParkingSpots, createPlayerCar, createNPCCars
from classes.checkRect import isCollision, isParked

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

while bRunning:
    # Create Game Board
    rParkingSpot = createParkingSpots()
    playerCar = createPlayerCar()
    rNpcCar = createNPCCars(rParkingSpot)

    # declarations
    player_xpos_change = 0.0
    player_ypos_change = 0.0
    nTurn = 0
    nSpeed = 0
    clock = pygame.time.Clock()
    bGame = True
    bSolve = False
    rStack = [(0,0)]

    # Temporary until we get a system that fills rStack
    for i in range(1000):
        rStack.append((-1.5,-0.9))

    # Game Loop
    while bGame:

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bRunning = False
                bGame = False

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
                if event.key == pygame.K_r:
                    bGame = False
                if event.key == pygame.K_s:
                     bSolve = True

        # move player car
        if bSolve and len(rStack)>0:
            stack = rStack.pop()
            print('stack',stack)
            nSpeed = stack[0]
            nTurn = stack[1]
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
            bCrash = isCollision(nc, playerCar)
            if bCrash:
                bGame = False
        # print("playerCar", playerCar.rect, playerCar.angle)

        # Check for Parked
        # print("Player Car - x:", playerCar.goal_x, "y:", playerCar.goal_y)
        # print("Player Car - x: ", playerCar.x, "y: ", playerCar.y, "rect: ", playerCar.rect, "surface: ", playerCar.surface, "angle:", playerCar.angle, "height:",playerCar.height,"width:",playerCar.width)

        for ps in rParkingSpot:
            # print("Parking Spot - x:", ps.x, "y: ", ps.y, "rect: ",ps.rect, "surface: ",ps.surface)
            bParked = isParked(ps.rect, playerCar.rect)
            if bParked:
                bGame = False

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
