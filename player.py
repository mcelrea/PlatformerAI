import pygame

class Player:

    # empty constructor
    def __init__(self, color=(255,0,0)):
        self.x = 400
        self.y = 400
        self.width = 30
        self.height = 30
        self.color = color
        self.isJumping = False
        self.currentJumpVel = 40
        self.maxJumpVel = 40
        self.speed = 10
        self.score = 0

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def jump(self):
        if not self.isJumping:
            self.isJumping = True

    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x

    def move_left(self):
        self.x += self.speed

    def move_right(self):
        self.x -= self.speed

    def handle_key_presses(self):
        if pygame.key.get_pressed()[pygame.K_SPACE] and not self.isJumping:
            self.isJumping = True
        if pygame.key.get_pressed()[pygame.K_d]:
            self.x += self.speed
        if pygame.key.get_pressed()[pygame.K_a]:
            self.x -= self.speed

    def act(self):
        oldx = self.x
        oldy = self.y

        self.handle_key_presses()
        self.handleJump()
        self.y -= self.map.get_gravity()
        if self.is_map_bottom_collision():
            self.y = oldy
            self.isJumping = False
            self.currentJumpVel = self.maxJumpVel
        if self.is_map_right_collision():
            self.x = oldx

        self.check_coin_collision()

        return (self.x, self.y)

    def check_coin_collision(self):
        coins = self.map.get_coins()
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        for c in coins:
            if myHitBox.colliderect(c.getCollisionRect()):
                coins.remove(c)
                self.score += 1

    def get_score(self):
        return self.score

    def handleJump(self):
        if self.isJumping:
            self.y -= self.currentJumpVel
            self.currentJumpVel += self.map.get_gravity()
            # terminal velocity
            if self.currentJumpVel < -self.maxJumpVel:
                self.currentJumpVel = -self.maxJumpVel


    def setMap(self, map):
        self.map = map

    def is_map_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                return True

        return False

    def is_map_bottom_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        myBottomY = myHitBox.y + myHitBox.height
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                if myBottomY > box.y: # I am hitting and BELOW this platform
                    return True;

        return False

    def is_map_right_collision(self):
        myHitBox = pygame.Rect(self.x, self.y, self.width, self.height)
        myRightX = myHitBox.x + myHitBox.width
        mapHitBoxes = self.map.get_hit_box_list()
        for box in mapHitBoxes:
            if myHitBox.colliderect(box):
                if myRightX > box.x: # I am hitting and to the RIGHT this platform
                    return True;

        return False


class Platform:

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    #used for drawing and used for collision detection
    def getRect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.getRect());

class Map:

    def __init__(self, gravity=-0.5):
        self.platforms = []
        self.gravity = gravity
        self.coins = []

    def add_coin(self, coin):
        self.coins.append(coin)

    def get_gravity(self):
        return self.gravity

    def set_gravity(self, gravity):
        self.gravity = gravity

    def add(self, platform):
        self.platforms.append(platform)

    def get_hit_box_list(self):
        hitBoxes = []
        for p in self.platforms:
            hitBoxes.append(p.getRect())

        return hitBoxes

    def get_coins(self):
        return self.coins

    # Precondition: the platforms list is a homogeneous list of Platform objects
    def draw(self, screen):
        for p in self.platforms:
            p.draw(screen)
        for c in self.coins:
            c.draw(screen)

class Coin:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.color = (255,255,0)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def getCollisionRect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)
