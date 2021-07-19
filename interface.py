import pygame, math

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

class Car:
    def __init__(self, x, y, height, width, img):
        self.x = x - width / 2
        self.y = y - height / 2
        self.height = height
        self.width = width
        self.rect = pygame.Rect(x, y, height, width)
        self.surface = pygame.Surface((height, width))
        self.surface.blit(img, (0, 0))
        self.angle = 0
        self.turn = 0.9
        self.speed = 0
        self.accel = 1.5

    def draw(self):
        self.rect.topleft = (int(self.x), int(self.y))
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        screen.blit(rotated, new_rect.topleft)

class Parking:
    def __init__(self, x, y, height, width, img):
        self.x = x - width / 2
        self.y = y - height / 2
        self.height = height
        self.width = width
        self.rect = pygame.Rect(x, y, height, width)
        self.surface = pygame.Surface((height, width))
        self.surface.blit(img, (0, 0))
        self.angle = 0
        self.turn = 0.9
        self.speed = 0
        self.accel = 1.5

    def draw(self):
        self.rect.topleft = (int(self.x), int(self.y))
        rotated = pygame.transform.rotate(self.surface, self.angle)
        surface_rect = self.surface.get_rect(topleft=self.rect.topleft)
        new_rect = rotated.get_rect(center=surface_rect.center)
        screen.blit(rotated, new_rect.topleft)


# Create Main Car
playerCarImg = pygame.image.load('graphics/cars/car1.png')
playerCarImgW = 80
playerCarImgH = 80
player_xpos = 370
player_ypos = 480
playerCar = Car(player_xpos, player_ypos, playerCarImgH, playerCarImgW, playerCarImg)

# Create NPC1 Car
rnpcCarImg = [pygame.image.load('graphics/cars/car2.png'), pygame.image.load('graphics/cars/car3.png')]
npcCarImgW = 80
npcCarImgH = 80
npc_xpos = [150, 350]
npc_ypos = [100, 100]
npc_num = 2
rNpcCar = []

for i in range(npc_num):
    rNpcCar.append(Car(npc_xpos[i], npc_ypos[i], npcCarImgH, npcCarImgW, rnpcCarImg[i]))

# Create Parking Spot
rParkingSpotImg = [pygame.image.load('graphics/parking spot/parkingSpot.png')]
nParkingSpotW = 90
nParkingSpotH = 90
rParkSpot_xpos = [150, 350]
rParkSpot_ypos = [100, 100]
nParkSpot_count = 2
rParkingSpot = []

for i in range(nParkSpot_count):
    rParkingSpot.append(Parking(rParkSpot_xpos[i], rParkSpot_ypos[i], nParkingSpotH, nParkingSpotW, rParkingSpotImg[0]))


def isCollision(npcCar, playCar):
    # print("npcCar",npcCar.rect, npcCar.angle%45, "playCar", playCar.rect,playCar.angle%45)

    doCollide = npcCar.rect.colliderect(playCar.rect)
    # print("doCollide",doCollide)
    if doCollide:
        print("CRASH!!!")


def isParked(ps_rect, car_rect):
    print("ps_rect", ps_rect, "car_rect", car_rect)


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

                # if nSpeed != 0:
                #     nTurn = playerCar.turn
                # else:
                #     nTurn = 0
            if event.key == pygame.K_RIGHT:
                print("pressed Right")
                nTurn = -playerCar.turn

                # if nSpeed != 0:
                #     nTurn = -playerCar.turn
                # else:
                #     nTurn = 0

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

    # Check for collison
    for nc in rNpcCar:
        isCollision(nc, playerCar)

    # Check for Parked
    #isParked(imgParkingSpot_rect, playerCar.rect)

    # draw game
    screen.fill((0, 0, 0))
    for ps in rParkingSpot:
        ps.draw()
    playerCar.draw()
    for nc in rNpcCar:
        nc.draw()
    #screen.blit(imgParkingSpot,(imgParkingSpot_xpos,imgParkingSpot_ypos))
    pygame.display.flip()
    clock.tick(60)

    # player_xpos = min(max(player_xpos + player_xpos_change, 0), nScreenW - playerCarImgW)
    # player_ypos = min(max(player_ypos + player_ypos_change, 0), nScreenH - playerCarImgH)
    # player_pos(player_xpos, player_ypos)

    # Update Game
    # pygame.display.update()

# End Game
pygame.quit()
