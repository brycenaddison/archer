####################################################################
####################################################################
##                                                                ##
##         █████╗ ██████╗  ██████╗██╗  ██╗███████╗██████╗         ##
##        ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗        ##
##        ███████║██████╔╝██║     ███████║█████╗  ██████╔╝        ##
##        ██╔══██║██╔══██╗██║     ██╔══██║██╔══╝  ██╔══██╗        ##
##        ██║  ██║██║  ██║╚██████╗██║  ██║███████╗██║  ██║        ##
##        ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝        ##
##                                                                ##
##        Coded by Brycen Addison                                 ##
##        Version 0.3d                                            ##
##                                                                ##
##        Changelog:                                              ##
##           Added menu animation function (not implemented)      ##
##           Added indicator for airstrike                        ##
##           Increased shot delay to make game less spammy        ##
##           Made enemy shooting not random and consistent        ##
##           Made exploding functions not take up 100 lines       ##
##           Fixed projectiles being in the top corner of         ##
##           the screen                                           ##
##                                                                ##
####################################################################
####################################################################
import pygame, sys, time, math, random, pygame.gfxdraw
from pygame.locals import *
pygame.init() # Initialize pygame
# Shorthands
clock = pygame.time.Clock()
# Classes
class game: # Game functions
    width = 360 # Width of screen
    height = int(width * 16/9) # Height of screen
    boundary = width / 18 # Margins of screen
    fps = 60 # Refresh rate of game
    def checkquit(): # Checks if the game should be closed due to input
        # Closes the game if the close button is pressed
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # Closes the game if the escape key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
    def checkpause(): # Checks if the game should be paused and then pauses the game
        global notPressed, paused, notPressed2 # Imports global variables fron init
        # Checks for pause key being pressed, activates pause if true
        key = pygame.key.get_pressed()
        if not key[pygame.K_TAB]:
            notPressed = True
        if key[pygame.K_TAB] and notPressed == True:
            paused = True
            notPressed = False
        # Pause loop
        if paused:
            # Displays pause text once
            game.textdisplay(int(game.width/4), "paused", (game.width/2), (game.height/3))
            game.textdisplay(int(game.width/20), "press tab to unpause", (game.width/2), (game.height/1.7))
            pygame.display.flip()
            # Refreshes screen with text then transfers to pause loop that will stay activated until tab key is pressed
            while paused:
                game.checkquit() # Allows the game to be quittable from pause menu
                clock.tick(60) # Sets framerate so game doesn't freeze
                # Checks for pause key being pressed, deactivates pause if true
                key = pygame.key.get_pressed()
                if key[pygame.K_TAB] == False:
                    notPressed2 = True
                if key[pygame.K_TAB] and notPressed2 == True:
                    paused = False
                    notPressed2 = False
    def text_render(text, font): # Renders text to a surface
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()
    def textdisplay(fontsize, text, centerx, centery): # Displays text on the screen
            Text = pygame.font.Font('freesansbold.ttf', fontsize)
            TextSurf, TextRect = game.text_render(text, Text)
            TextRect.center = (centerx, centery)
            window.blit(TextSurf, TextRect)
    class text:
        archerfont = 'archerfont.ttf'
        def moving(fontsize, text, centerx, centery, direction):
            t = game.text.object(fontsize, text, centerx, centery, direction)
            all_sprites.add(t)
            t.display(fontsize, text, centerx, centery)
        def still(fontsize, text, centerx, centery):
            game.textdisplay(fontsize, text, centerx, centery)
        class object(pygame.sprite.Sprite):
            def __init__(self, fontsize, text, centerx, centery, direction):
                pygame.sprite.Sprite.__init__(self)
                self.height = game.height
                self.width = game.width
                self.fontsize = fontsize
                self.text = text
                self.centerx = centerx
                self.centery = centery
                self.direction = direction
                self.tick = 0
                self.speed = game.height/640
                self.initspeed = self.speed
                self.completed = False
                self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
                self.image = self.image.convert_alpha()
                self.rect = self.image.get_rect()
                if self.direction == 'left':
                    self.rect.x = -game.height
                    self.rect.y = 0
                if self.direction == 'up':
                    self.rect.x = 0
                    self.rect.y = -game.height
                if self.direction == 'right':
                    self.rect.x = game.height
                    self.rect.y = 0
                if self.direction == 'down':
                    self.rect.x = 0
                    self.rect.y = game.height
            def update(self):
                if self.completed == False:
                    self.tick += self.initspeed
                    if self.direction == 'left':
                        self.rect.x += self.tick
                        if self.rect.x >= 0:
                            self.rect.x = 0
                            self.completed = True
                    if self.direction == 'up':
                        self.rect.y += self.tick
                        if self.rect.y >= 0:
                            self.rect.y = 0
                            self.completed = True
                    if self.direction == 'right':
                        self.rect.x -= self.tick
                        if self.rect.x <= 0:
                            self.rect.x = 0
                            self.completed = True
                    if self.direction == 'down':
                        self.rect.y -= self.tick
                        if self.rect.y <= 0:
                            self.rect.y = 0
                            self.completed = True
            def render(self, text, font): # Renders text to a surface
                textSurface = font.render(text, True, (0, 0, 0))
                return textSurface, textSurface.get_rect()
            def display(self, fontsize, text, centerx, centery): # Displays text on the screen
                Text = pygame.font.Font(game.text.archerfont, fontsize)
                TextSurf, TextRect = self.render(text, Text)
                TextRect.center = (centerx, centery)
                self.image.blit(TextSurf, TextRect)
    def init(): # Initializes global variables
        import highscore
        global all_sprites, arrows, targets, avoids, archer, highScore, spawnRate, milestone, cubes, bufftargets, paused, notPressed, notPressed2, movingtargets, healthPack, healthtargets, airstriketargets, bombtargets, buffbombtargets, airstriketargetindicators
        all_sprites = pygame.sprite.Group()
        arrows = pygame.sprite.Group()
        targets = pygame.sprite.Group()
        bufftargets = pygame.sprite.Group()
        movingtargets = pygame.sprite.Group()
        healthtargets = pygame.sprite.Group()
        airstriketargets = pygame.sprite.Group()
        airstriketargetindicators = pygame.sprite.Group()
        bombtargets = pygame.sprite.Group()
        buffbombtargets = pygame.sprite.Group()
        avoids = pygame.sprite.Group()
        archer = player()
        all_sprites.add(archer)
        highScore = highscore.v
        spawnRate = 1
        milestone = True
        cubes = 0
        notPressed = False
        paused = False
        notPressed2 = False
        healthPack = 0
    def saveValid(): # Checks if the save file can be imported
        global highscore
        while True:
            game.checkquit() # Allows the game to be quit if frozen here
            try:
                game.init() # Initializes game variables if save is valid
                break
            except Exception as e: # Prints error to console if save file is invalid then creates new one with a score of 0.
                print(e)
                highScore = 0
                with open("highscore.py", "w") as savefile:
                    print(f"v = {highScore}", file=savefile)
    def checkBest(): # Updates high score
        global highScore
        if archer.hits > highScore:
            highScore = archer.hits
            with open("highscore.py", "w") as savefile:
                print(f"v = {highScore}", file=savefile)
    def update(): # Runs all update functions
            updateDifficulty()
            all_sprites.update()
class player(pygame.sprite.Sprite): # Player class
    def __init__(self):
            pygame.sprite.Sprite.__init__(self) # Initialize sprite
            self.health = 5 # How many hits you take before dying
            self.hits = 0 # Amount of targets player has hit
            self.width = game.width / 9 # Player hitbox width
            self.height = game.height / 16 # Player hitbox height
            self.x = (game.width - self.width) / 2 # Player stating x position
            self.y = 7/8 * game.height # Player starting y position
            self.regularVelocity = 0 * game.width / 360 # Your base speed after changing directions
            self.velocityCap = 3 * game.width / 360 # Maximum regular player velocity
            self.velocityGain = 0.2 * game.width / 360 # How fast your velocity rises after moving in one continual direction
            self.velocityLoss = 0.25 * game.width / 360 # How fast the player loses speed and changes directions
            self.dashVelocity = 10 * game.width / 360 # What your speed changes to when you dash
            self.dashCooldown = 90 # How many frames after Dash is used Dash can be used again
            self.dashLength = 10 # How many frames Dash lasts
            self.shotCooldown = 8 # How many frames before the player can shoot again
            self.shotDelay = 10 # The amount of frames before a shot goes off after pressing space
            self.moveCooldown = 10 # The amount of frames after shooting you can move again
            self.drawInnerCircle = True # Draws inner circle if true
            self.image = pygame.Surface((self.width, self.height)) # Initializes player surface
            self.image.fill((255, 255, 255, 0)) # Makes player surface transparent
            self.rect = self.image.get_rect() # Creates hitbox for player surface
            self.circlex = int(0.5 * self.width) # Sets coordinate x for circle draw
            self.circley = int(0.5 * self.height) # Sets coordinate y for circle draw
            self.radius = int((self.width+self.height) / 4 - 1) # Sets radius for circle draw
            self.art = pygame.Surface((self.width, self.height)) # Creates surface to draw circle onto
            self.art.fill((255, 255, 255, 255)) # Makes surface white
            pygame.gfxdraw.aacircle(self.art, self.circlex, self.circley, self.radius, (50, 100, 255)) # Draws outer circle AA
            pygame.gfxdraw.filled_circle(self.art, self.circlex, self.circley, self.radius, (50, 100, 255)) # Draws outer circle
            if self.drawInnerCircle == True:
                    pygame.gfxdraw.aacircle(self.art, self.circlex, self.circley, int(self.radius * (3/4)), (0, 0, 0)) # Draws inner circle AA
                    pygame.gfxdraw.filled_circle(self.art, self.circlex, self.circley, int(self.radius * (3/4)), (0, 0, 0)) # Draws inner circle
            self.image.blit(self.art, (0, 0)) # Blits circles onto player surface
            self.dashUntilReset = 0 # Counts time left before next dash
            self.dashCount = 0 # Counts time since player dash
            self.velocity = self.regularVelocity # Sets velocity of dash
            self.isDash = False # Tells whether player is dashing
            self.movingLeft = 0 # Holds how long player has been moving left
            self.movingRight = 0 # Holds how long player has been moving right
            self.dashMove = '' # Holds which direction player dashed in
            self.shotCount = 0 # Frames since the last shot
            self.spaceValue = 0 # Frames since space bar was pressed
            self.shiftValue = 0 # Frames since shift was pressed
    def move(self):
        move = pygame.key.get_pressed()
        # Detects first press of shift, shiftValue = 1 on first press tick, 0 if yet to be pressed, and 2 if already pressed without being released. When released, resets to 0. This is in order to do a command once when shift is pressed, but not repeat it.
        if move[pygame.K_LSHIFT]:
            self.shiftValue += 1
            if self.shiftValue > 2:
                self.shiftValue = 2
        if not move[pygame.K_LSHIFT]:
                self.shiftValue = 0
        # Continues to dash player in a direction if already dashing unless they are finished dashing according to dashLength, where it will start the dash cooldown and stop dashing.
        if self.isDash:
            self.dashCount += 1
            if self.dashMove == 'left' and self.x > game.boundary:
                self.x -= self.velocity
            if self.dashMove == 'right' and self.x < game.width - game.boundary - self.width:
                self.x += self.velocity
            if self.dashCount == self.dashLength:
                self.isDash = False
                self.velocity = 0
                self.dashCount = 0
                self.dashUntilReset = self.dashCooldown

        else:
            # If dash is on cooldown, it counts down the cooldown.
            if self.dashUntilReset > 0:
                self.dashUntilReset -= 1
            # On the first tick of shift being pressed along with a movement key and if dash isn't on cooldown, initalizes dash.
            if self.shiftValue == 1 and (move[pygame.K_a] or move[pygame.K_LEFT] or move[pygame.K_d] or move[pygame.K_RIGHT]) and (self.dashUntilReset == 0):
                self.isDash = True
                self.velocity = self.dashVelocity
                self.dashCount = 0
                # Sets dash direction
                if (move[pygame.K_a] or move[pygame.K_LEFT]) and self.x > game.boundary:
                    self.x -= self.velocity
                    self.dashMove = 'left'
                if (move[pygame.K_d] or move[pygame.K_RIGHT]) and self.x < game.width - game.boundary - self.width:
                    self.x += self.velocity
                    self.dashMove = 'right'
            # Player moving functions, uses exponential velocity with a limit to simulate inertia.
            if (move[pygame.K_a] or move[pygame.K_LEFT]) and self.x > game.boundary and (self.isDash == False):
                if self.movingRight > 0:
                    self.movingRight -= self.velocityLoss
                    if self.x < game.width - game.boundary - self.width:
                        self.x += self.velocity + self.movingRight
                    if self.movingRight < 0:
                        self.movingRight = 0
                else:
                    self.x -= (self.velocity + self.movingLeft)
                    if self.movingLeft <= self.velocityCap:
                        self.movingLeft += self.velocityGain
            if (move[pygame.K_d] or move[pygame.K_RIGHT]) and self.x < game.width - game.boundary - self.width and (self.isDash == False):
                if self.movingLeft > 0:
                    self.movingLeft -= self.velocityLoss
                    if self.x > game.boundary:
                        self.x -= self.velocity + self.movingLeft
                    if self.movingLeft < 0:
                        self.movingLeft = 0
                else:
                    self.x += (self.velocity + self.movingRight)
                    if self.movingRight <= self.velocityCap:
                        self.movingRight += self.velocityGain
        # Slows the player down using the same inertia functions when they stop moving.
        if not (move[pygame.K_d] or move[pygame.K_RIGHT] or move[pygame.K_a] or move[pygame.K_LEFT]):
            if self.movingLeft > 0:
                self.movingLeft -= self.velocityLoss
                if self.x > game.boundary:
                    self.x -= self.velocity + self.movingLeft
                if self.movingLeft < 0:
                    self.movingLeft = 0
            if self.movingRight > 0:
                self.movingRight -= self.velocityLoss
                if self.x < game.width - game.boundary - self.width:
                    self.x += self.velocity + self.movingRight
                if self.movingRight < 0:
                    self.movingRight = 0 # Checks for keyboard inputs to make the player move
    def shoot(self): # Checks for keyboard inputs to make the player shoot
            # spaceValue is set to 1 on first tick after space is pressed
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                    self.spaceValue += 1
                    if self.spaceValue > 2:
                            self.spaceValue = 2
            if not key[pygame.K_SPACE]:
                    self.spaceValue = 0
            # Shoots an arrow on first tick after space is pressed and there is no cooldown
            if self.spaceValue == 1 and self.shotCount == 0:
                    arrow = Arrow(self.x + self.width/2, self.y, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    all_sprites.add(arrow)
                    arrows.add(arrow)
                    self.shotCount = 1
            # Resets shot cooldown when cooldown is over
            if (0 < self.shotCount) and (self.shotCount <= self.shotCooldown):
                    self.shotCount += 1
                    if self.shotCount == self.shotCooldown:
                            self.shotCount = 0
    def update(self): # Updates archer position and inputs every frame
            key = pygame.key.get_pressed()
            archer.shoot()
            archer.move()
            self.rect.x = self.x
            self.rect.y = self.y
    def render(self): # Displays player object on starting screend
        pygame.gfxdraw.aacircle(window, int(self.x + self.circlex), int(self.y + self.circley), self.radius, (50, 100, 255)) # Draws outer circle AA
        pygame.gfxdraw.filled_circle(window, int(self.x + self.circlex), int(self.y + self.circley), self.radius, (50, 100, 255)) # Draws outer circle
        pygame.gfxdraw.aacircle(window, int(self.x + self.circlex), int(self.y + self.circley), int(self.radius * (3/4)), (0, 0, 0)) # Draws inner circle AA
        pygame.gfxdraw.filled_circle(window, int(self.x + self.circlex), int(self.y + self.circley), int(self.radius * (3/4)), (0, 0, 0)) # Draws inner circle
class Arrow(pygame.sprite.Sprite): # Player Projectile
    def __init__(self, x, y, gotox, gotoy):
        pygame.sprite.Sprite.__init__(self)
        self.xsize = game.width / 36
        self.ysize = game.height / 64
        self.y = y
        self.x = x
        self.circlex = int(0.5 * self.xsize)
        self.circley = int(0.5 * self.ysize)
        self.radius = int((self.xsize+self.ysize) / 4 - 1)
        self.speed = 5/128 * game.height
        self.gotox = gotox
        self.gotoy = gotoy
        self.image = pygame.Surface((self.xsize, self.ysize))
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        if self.gotoy > archer.y:
                self.gotoy = archer.y
        self.gotox -= self.xsize / 2
        self.gotoy -= self.ysize / 2
        self.dx = self.gotox - self.x
        self.dy = self.gotoy - self.y
        self.slope = (self.dy / max(1, self.dx))
        self.gotox += self.gotox * self.slope
        self.gotoy += self.gotoy * self.slope
        self.dist = max(1, math.hypot(self.dx, self.dy))
    def update(self):
        pygame.gfxdraw.aacircle(self.image, self.circlex, self.circley, self.radius, (0,0,0))
        pygame.gfxdraw.filled_circle(self.image, self.circlex, self.circley, self.radius, (0,0,0))
        dist = max(1, math.hypot(self.dx, self.dy))
        self.vx = self.speed * (self.dx / self.dist)
        self.vy = self.speed * (self.dy / self.dist)
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        if self.x < -5:
            self.kill() # Player projectile class #
class Target(pygame.sprite.Sprite): # Basic enemy class
    def __init__(self): # Initial values of the object
        pygame.sprite.Sprite.__init__(self)
        self.fireRate = 120 # The frame cooldown between shots
        self.width = game.width / 8 # Enemy width
        self.height = self.width # Enemy height
        self.image = pygame.Surface((self.width, self.height)) # Creates pygame sprite surface
        self.image.fill((255, 0, 0)) # Makes the surface red
        self.oboxwidth = int(7/8 * self.width + 0.5) # Enemy inner box width
        self.oboxheight = int(7/8 * self.height + 0.5) # Enemy inner box height
        self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight)) # Creates the inner box surface
        self.outlinebox.fill((0, 0, 0)) # Makes the inner box black
        self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5))) # Blits inner box to pygame sprite surface
        self.rect = self.image.get_rect() # Creates a rect for pygame sprite
        self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary)) # The initial x value of the enemy
        self.rect.y = random.randint(int(-game.height), int(-self.height)) # The initial y value of the enemy
        self.speed = game.width / 64 # The speed that the enemy comes from the top of the screen
        self.nextShotTimer = 0 # Holds the number of frames since last shot
    def update(self): # Object commands to be parsed every frame
        self.rect.y += self.speed # Moves the enemy from the top of the room
        if self.rect.y >= (random.randint(10, 40)/100) * game.height: # The enemy stops at a random point 10 and 40 percent down the screen
            self.speed = 0
        if self.speed == 0: # Starts shooting when enemy is stopped
            if self.nextShotTimer == self.fireRate: # Shoots when shot cooldown is up
                avoid = Avoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64) # Creates projectile
                all_sprites.add(avoid) # Adds projectile to group of sprites to be refreshed every frame
                avoids.add(avoid) # Adds projectile to group of enemy projectiles
                self.nextShotTimer = 0 # Resets shot cooldown after shot
            self.nextShotTimer += 1 # Adds to shot cooldown
class BuffTarget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.health = 3 # The numeber of times the enemy needs to be shot before dying
        self.fireRate = 90 # The number of frames between shots
        self.width = game.width / 8 # Enemy width
        self.height = self.width # Enemy height
        self.image = pygame.Surface((self.width, self.height)) # Creates pygame sprite surface
        if self.health == 1: # Surface is red if one shot from dying
            self.image.fill((255, 0, 0))
        if self.health == 2: # Surface is orange if two shots from dying
            self.image.fill((255, 165, 0))
        if self.health == 3: # Surface is yellow if three shots from dying
            self.image.fill((255, 255, 0))
        self.oboxwidth = int(7/8 * self.width + 0.5) # Enemy inner box width
        self.oboxheight = int(7/8 * self.height + 0.5) # Enemy inner box height
        self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight)) # Creates the inner box surface
        self.outlinebox.fill((0, 0, 0)) # Makes the inner box black
        self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5))) # Blits inner box to pygame sprite surface
        self.rect = self.image.get_rect() # Creates a rect for pygame sprite
        self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary)) # The initial x value of the enemy
        self.rect.y = random.randint(int(-game.height), int(-self.height)) # The initial y value of the enemy
        self.speed = game.width / 64 # The speed that the enemy comes from the top of the screen
        self.nextShotTimer = 0 # Holds the number of frames since last shot # Initial values of the object
    def update(self): # Object commands to be parsed every frame
        global cubes # Imports global "cube" variable to track the number of cubes on the screen
        self.rect.y += self.speed # Moves the enemy from the top of the screen
        if self.rect.y >= (random.randint(10, 40)/100) * game.height: # The enemy stops at a random point 10 and 40 percent down the screen
            self.speed = 0
        if self.speed == 0: # Starts shooting when enemy is stopped
            if self.nextShotTimer == self.fireRate: # Shoots when shot cooldown is up
                avoid = Avoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64) # Creates projectile
                all_sprites.add(avoid) # Adds projectile to group of sprites to be refreshed every frame
                avoids.add(avoid) # Adds projectile to group of enemy projectiles
                self.nextShotTimer = 0 # Resets shot cooldown after shot
            self.nextShotTimer += 1 # Adds to shot cooldown
        hits = pygame.sprite.groupcollide(bufftargets, arrows, False, True) # Detects hits between player shots and enemy
        for hit in hits:
            self.health -= 1 # Removes 1 from health when hit with player shot
        if self.health == 0:
            self.kill() # Kills enemy when enemy runs out of health
            cubes -= 1 # Takes 1 away from total cube number before spawning another cube
            spawn() # Spawns a new cube
            archer.hits += 1 # Adds one to player score
        if self.health == 1: # Enemy turns red when on 1 health
            self.image.fill((255, 0, 0))
        if self.health == 2: # Enemy turns orange when on 2 health
            self.image.fill((255, 165, 0))
        if self.health == 3: # Enemy turns yellow when on 3 health
            self.image.fill((255, 255, 0))
        self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5))) # Refreshes color of cube
class MovingTarget(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fireRate = 60 # The number of frames between shots
        self.width = game.width / 8 # Enemy width
        self.height = self.width # Enemy height
        self.image = pygame.Surface((self.width, self.height)) # Creates pygame sprite surface
        self.image.fill((128, 0, 128)) # Makes the surface purple
        self.oboxwidth = int(7/8 * self.width + 0.5) # Enemy inner box width
        self.oboxheight = int(7/8 * self.height + 0.5) # Enemy inner box height
        self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight)) # Creates the inner box surface
        self.outlinebox.fill((0, 0, 0)) # Makes the inner box black
        self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5))) # Blits inner box to pygame sprite surface
        self.rect = self.image.get_rect() # Creates a rect for pygame sprite
        self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary)) # The initial x value of the enemy
        self.rect.y = random.randint(int(-game.height), int(-self.height)) # The initial y value of the enemy
        self.speed = game.width / 64 # The speed that the enemy comes from the top of the screen
        self.speedx = self.speed # The speed that the object moves from side to side
        self.movingMaxLeft = random.randint(game.boundary, game.width/4) # Initial boundary that a moving target can move to the left
        self.movingMaxRight = random.randint(game.width*0.75, (game.width-game.boundary)) # Initial boundary that a moving target can move t the right
        self.nextShotTimer = 0
        if random.randint(0,1) == 1: # Randomly determines whether the cube should start moving towards the left or the right
            self.leftTrueRightFalse = True
        else:
            self.leftTrueRightFalse = False
    def update(self):
        # The cube changes directions when it reaches a boundary
        if self.rect.x <= self.movingMaxLeft:
            self.leftTrueRightFalse = False
        if self.rect.x >= self.movingMaxRight:
            self.leftTrueRightFalse = True
        if self.leftTrueRightFalse:
            self.movingValue = -self.speedx
        if not self.leftTrueRightFalse:
            self.movingValue = self.speedx
        # Refreshes the cube's position
        self.rect.y += self.speed
        self.rect.x += self.movingValue
        # The enemy stops moving at a random point 10 to 40 percent down the screen
        if self.rect.y >= (random.randint(10, 40)/100) * game.height:
            self.speed = 0
        if self.speed == 0: # Starts shooting when enemy is stopped
            if self.nextShotTimer == self.fireRate: # Shoots when shot cooldown is up
                avoid = Avoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64) # Creates projectile
                all_sprites.add(avoid) # Adds projectile to group of sprites to be refreshed every frame
                avoids.add(avoid) # Adds projectile to group of enemy projectiles
                self.nextShotTimer = 0 # Resets shot cooldown after shot
            self.nextShotTimer += 1 # Adds to shot cooldown
class HealthTarget(pygame.sprite.Sprite):
    def __init__(self): # Initial values of the object
        pygame.sprite.Sprite.__init__(self)
        self.fireRate = 150 # The frame cooldown between shots
        self.width = game.width / 8 # Enemy width
        self.height = self.width # Enemy height
        self.image = pygame.Surface((self.width, self.height)) # Creates pygame sprite surface
        self.image.fill((0, 255, 0)) # Makes the surface green
        self.oboxwidth = int(7/8 * self.width + 0.5) # Enemy inner box width
        self.oboxheight = int(7/8 * self.height + 0.5) # Enemy inner box height
        self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight)) # Creates the inner box surface
        self.outlinebox.fill((0, 0, 0)) # Makes the inner box black
        self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5))) # Blits inner box to pygame sprite surface
        self.rect = self.image.get_rect() # Creates a rect for pygame sprite
        self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary)) # The initial x value of the enemy
        self.rect.y = random.randint(int(-game.height), int(-self.height)) # The initial y value of the enemy
        self.speed = game.width / 64 # The speed that the enemy comes from the top of the screen
        self.nextShotTimer = 0 # Holds the number of frames since last shot
    def update(self): # Object commands to be parsed every frame
        self.rect.y += self.speed # Moves the enemy from the top of the room
        if self.rect.y >= (random.randint(10, 40)/100) * game.height: # The enemy stops at a random point 10 and 40 percent down the screen
            self.speed = 0
        if self.speed == 0: # Starts shooting when enemy is stopped
            if self.nextShotTimer == self.fireRate: # Shoots when shot cooldown is up
                avoid = Avoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64) # Creates projectile
                all_sprites.add(avoid) # Adds projectile to group of sprites to be refreshed every frame
                avoids.add(avoid) # Adds projectile to group of enemy projectiles
                self.nextShotTimer = 0 # Resets shot cooldown after shot
            self.nextShotTimer += 1 # Adds to shot cooldown
class Avoid(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xsize = game.width / 36
        self.ysize = game.height / 64
        self.y = y
        self.x = x
        self.circlex = int(0.5 * self.xsize)
        self.circley = int(0.5 * self.ysize)
        self.radius = int((self.xsize+self.ysize) / 4 - 1)
        self.speed = 5/512 * game.height
        self.gotox = archer.x + archer.width / 2
        self.gotoy = archer.y + archer.height / 2
        self.image = pygame.Surface((self.xsize, self.ysize))
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        self.gotox -= self.xsize / 2
        self.gotoy -= self.ysize / 2
        self.dx = self.gotox - self.x
        self.dy = self.gotoy - self.y
        self.slope = (self.dy / max(1, self.dx))
        self.gotox += self.gotox * self.slope
        self.gotoy += self.gotoy * self.slope
        self.dist = max(1, math.hypot(self.dx, self.dy))
    def update(self):
        pygame.gfxdraw.aacircle(self.image, self.circlex, self.circley, self.radius, (255, 0, 0))
        pygame.gfxdraw.filled_circle(self.image, self.circlex, self.circley, self.radius, (255, 0, 0))
        dist = max(1, math.hypot(self.dx, self.dy))
        self.vx = self.speed * (self.dx / self.dist)
        self.vy = self.speed * (self.dy / self.dist)
        self.x += self.vx
        self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
        if self.y > game.height + 10:
            self.kill()
class AirstrikeTarget(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos):
            pygame.sprite.Sprite.__init__(self)
            self.fireRate = 10
            self.width = game.width / 8
            self.height = self.width
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 255, 0))
            self.oboxwidth = int(7/8 * self.width + 0.5)
            self.oboxheight = int(7/8 * self.height + 0.5)
            self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight))
            self.outlinebox.fill((30, 30, 30))
            self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5)))
            self.rect = self.image.get_rect()
            self.rect.x = xpos
            self.rect.y = ypos
            self.speed = game.width / 24
            self.minigunCounter = 9
    def update(self):
            global cubes
            self.rect.y += self.speed
            if self.rect.y >= 2*game.height:
                    self.kill()
                    mob.airstrikeTarget()
            self.minigunCounter += 1
            if self.minigunCounter == self.fireRate:
                    self.minigunCounter = 0
                    avoid = MinigunShot(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64)
                    all_sprites.add(avoid)
                    avoids.add(avoid)
class AirstrikeTargetIndicator(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = -5
        self.inity = y
        self.tick = 0
        self.ylist = [-1]
        self.image = pygame.Surface((1, 1))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = -1
        self.rect.y = -1
        self.spawnedUnit = False
        self.nukerY = -2 * game.height
        self.nukerSpeed = game.height/12
    def update(self):
        self.tick += 1
        self.y += 15
        if (game.height >= self.y >= 0):
            self.ylist.append(self.y)
        for x in self.ylist:
            if x >= 0:
                ais = AirstrikeIndicatorSprite(self.x + game.width/16, x)
                all_sprites.add(ais)
        if (self.y >= game.height) and (len(self.ylist) > 0):
            self.nukerY += self.nukerSpeed
            if self.ylist[0] <= self.nukerY:
                self.ylist.pop(0)
        if (self.y >= game.height) and (self.spawnedUnit == False):
            at = AirstrikeTarget(self.x, self.inity)
            all_sprites.add(at)
            airstriketargets.add(at)
            self.spawnedUnit = True
        if len(self.ylist) == 0:
            self.kill()
class AirstrikeIndicatorSprite(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.width = 5
        self.height = 5
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x + 2.5
        self.rect.y = y + 2.5
        self.tick = 0
    def update(self):
        if self.tick == 1:
            self.kill()
        self.tick += 1
class MinigunShot(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.xsize = game.width / 36
        self.ysize = game.height / 64
        self.y = y
        self.x = x
        self.circlex = int(0.5 * self.xsize)
        self.circley = int(0.5 * self.ysize)
        self.radius = int((self.xsize+self.ysize) / 4 - 1)
        self.speed = game.width / 12
        self.image = pygame.Surface((self.xsize, self.ysize))
        self.image.fill((0, 0, 0, 0))
        self.rect = self.image.get_rect()
        pygame.gfxdraw.aacircle(self.image, self.circlex, self.circley, self.radius, (0, 0, 0))
        pygame.gfxdraw.filled_circle(self.image, self.circlex, self.circley, self.radius, (0, 0, 0))
        pygame.gfxdraw.aacircle(self.image, self.circlex, self.circley, self.radius, (255, 255, 0))
        pygame.gfxdraw.filled_circle(self.image, int(1/8+self.circlex), int(1/8+self.circley), int(7/8*self.radius), (255, 255, 0))
    def update(self):
        self.y += self.speed
        self.rect.x = self.x
        self.rect.y = self.y
        if self.rect.y > game.height + 10:
            self.kill()
class BombTarget(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.tickValue = 0
            self.width = game.width / 8
            self.height = self.width
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))
            self.oboxwidth = int(7/8 * self.width + 0.5)
            self.oboxheight = int(7/8 * self.height + 0.5)
            self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight))
            self.outlinebox.fill((0, 0, 0))
            self.tickboxwidth = int(1/2 * self.width + 0.5)
            self.tickboxheight = int(1/2 * self.height + 0.5)
            self.tickbox = pygame.Surface((self.tickboxwidth, self.tickboxheight))
            self.tickbox.fill((0, 0, 0))
            self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5)))
            self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary))
            self.rect.y = random.randint(int(-game.height), int(-self.height))
            self.speed = game.width / 64
            self.tick = False
            self.exploded = False
            self.shotTimer = 0
    def update(self):
            self.rect.y += self.speed
            if self.rect.y >= (random.randint(10, 40)/100) * game.height:
                    self.speed = 0
            if self.speed == 0:
                self.tickValue += 1
                if self.tickValue <= 64:
                    if (self.tickValue % 16) <= 7:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue <= 128:
                    if (self.tickValue % 8) <= 3:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue <= 192:
                    if (self.tickValue % 4) <= 1:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue < 256:
                    if (self.tickValue % 2) == 0:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue == 256:
                    self.exploded = True
                if self.tick:
                    self.tickbox.fill((255, 0, 0))
                    self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
                else:
                    self.tickbox.fill((0, 0, 0))
                    self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
                if self.exploded == True:
                    if (self.shotTimer % 5) == 1:
                        avoid1 = SeekingAvoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64, 'down')
                        all_sprites.add(avoid1)
                        avoids.add(avoid1)
                        avoid2 = SeekingAvoid(self.rect.x - game.height / 64, self.rect.y + self.height / 2, 'left')
                        all_sprites.add(avoid2)
                        avoids.add(avoid2)
                        avoid3 = SeekingAvoid(self.rect.x + self.width / 2, self.rect.y - game.height / 64, 'up')
                        all_sprites.add(avoid3)
                        avoids.add(avoid3)
                        avoid4 = SeekingAvoid(self.rect.x + self.width + game.height / 64, self.rect.y + self.height / 2, 'right')
                        all_sprites.add(avoid4)
                        avoids.add(avoid4)
                    if self.shotTimer == 5:
                        self.kill()
                        spawn()
                    self.shotTimer += 1
class BuffBombTarget(pygame.sprite.Sprite):
    def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.health =  3
            self.tickValue = 0
            self.width = game.width / 8
            self.height = self.width
            self.image = pygame.Surface((self.width, self.height))
            if self.health == 1:
                self.image.fill((255, 0, 0))
            if self.health == 2:
                self.image.fill((255, 165, 0))
            if self.health == 3:
                self.image.fill((255, 255, 0))
            self.oboxwidth = int(7/8 * self.width + 0.5)
            self.oboxheight = int(7/8 * self.height + 0.5)
            self.outlinebox = pygame.Surface((self.oboxwidth, self.oboxheight))
            self.outlinebox.fill((0, 0, 0))
            self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5)))
            self.tickboxwidth = int(1/2 * self.width + 0.5)
            self.tickboxheight = int(1/2 * self.height + 0.5)
            self.tickbox = pygame.Surface((self.tickboxwidth, self.tickboxheight))
            self.tickbox.fill((0, 0, 0))
            self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(int(game.boundary), int(game.width - self.width - game.boundary))
            self.rect.y = random.randint(int(-game.height), int(-self.height))
            self.speed = game.width / 64
            self.tick = False
            self.exploded = False
            self.shotTimer = 0
    def update(self):
            global cubes
            self.rect.y += self.speed
            if self.rect.y >= (random.randint(10, 40)/100) * game.height:
                    self.speed = 0
            hits = pygame.sprite.groupcollide(buffbombtargets, arrows, False, True)
            for hit in hits:
                    self.health -= 1
            if self.health == 0:
                    self.kill()
                    cubes -= 1
                    spawn()
                    archer.hits += 1
            if self.health == 1:
                self.image.fill((255, 0, 0))
            if self.health == 2:
                self.image.fill((255, 165, 0))
            if self.health == 3:
                self.image.fill((255, 255, 0))
            self.image.blit(self.outlinebox, (int(self.width/16 + 0.5), int(self.height/16 + 0.5)))
            if self.speed == 0:
                self.tickValue += 1
                if self.tickValue <= 64:
                    if (self.tickValue % 32) <= 15:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue <= 128:
                    if (self.tickValue % 16) <= 7:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue <= 192:
                    if (self.tickValue % 8) <= 3:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue < 256:
                    if (self.tickValue % 4) <= 1:
                        self.tick = True
                    else:
                        self.tick = False
                elif self.tickValue == 256:
                    self.exploded = True
                if self.tick:
                    self.tickbox.fill((255, 0, 0))
                    self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
                else:
                    self.tickbox.fill((0, 0, 0))
                    self.image.blit(self.tickbox, (int(self.width/4 + 0.5), int(self.height/4 + 0.5)))
                if self.exploded == True:
                    if (self.shotTimer % 5) == 1:
                        avoid1 = SeekingAvoid(self.rect.x + self.width / 2, self.rect.y + self.height + game.height / 64, 'down')
                        all_sprites.add(avoid1)
                        avoids.add(avoid1)
                        avoid2 = SeekingAvoid(self.rect.x - game.height / 64, self.rect.y + self.height / 2, 'left')
                        all_sprites.add(avoid2)
                        avoids.add(avoid2)
                        avoid3 = SeekingAvoid(self.rect.x + self.width / 2, self.rect.y - game.height / 64, 'up')
                        all_sprites.add(avoid3)
                        avoids.add(avoid3)
                        avoid4 = SeekingAvoid(self.rect.x + self.width + game.height / 64, self.rect.y + self.height / 2, 'right')
                        all_sprites.add(avoid4)
                        avoids.add(avoid4)
                    if self.shotTimer == 5:
                        self.kill()
                        spawn()
                    self.shotTimer += 1
class SeekingAvoid(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.xsize = game.width / 36
        self.ysize = game.height / 64
        self.y = y
        self.x = x
        self.circlex = int(0.5 * self.xsize)
        self.circley = int(0.5 * self.ysize)
        self.radius = int((self.xsize+self.ysize) / 4 - 1)
        self.speed = 5/512 * game.height
        self.image = pygame.Surface((self.xsize, self.ysize))
        self.image.fill((255, 255, 255, 0))
        self.rect = self.image.get_rect()
        self.tick = 0
        self.direction = direction
        pygame.gfxdraw.aacircle(self.image, self.circlex, self.circley, self.radius, (255, 0, 255))
        pygame.gfxdraw.filled_circle(self.image, self.circlex, self.circley, self.radius, (255, 0, 255))
    def update(self):
        if not self.tick >= 21:
            self.tick += 1
            if self.direction == 'left':
                self.x -= self.speed * 1.1 ** (-self.tick)
            if self.direction == 'right':
                self.x += self.speed * 1.1 ** (-self.tick)
            if self.direction == 'up':
                self.y -= self.speed * 1.1 ** (-self.tick)
            if self.direction == 'down':
                self.y += self.speed * 1.1 ** (-self.tick)
        else:
            if self.tick >= 40:
                self.speedVar = self.speed
            else:
                self.tick += 1
                self.speedVar = self.speed * 1.1 ** (-40 + self.tick)
            self.gotox = archer.x + archer.width / 2
            self.gotoy = archer.y + archer.height / 2
            self.gotox -= self.xsize / 2
            self.gotoy -= self.ysize / 2
            self.dx = self.gotox - self.x
            self.dy = self.gotoy - self.y
            self.slope = (self.dy / max(1, self.dx))
            self.gotox += self.gotox * self.slope
            self.gotoy += self.gotoy * self.slope
            self.dist = max(1, math.hypot(self.dx, self.dy))
            dist = max(1, math.hypot(self.dx, self.dy))
            self.vx = self.speedVar * (self.dx / self.dist)
            self.vy = self.speedVar * (self.dy / self.dist)
            self.x += self.vx
            self.y += self.vy
        self.rect.x = self.x
        self.rect.y = self.y
# Displays framerate
def display():
    global spawnRate, highScore, Cubes
    font = pygame.font.Font("archerfont.ttf", int(game.height / 64))
    counter = font.render(f"Health: {archer.health} Hits: {archer.hits} Best: {highScore} Cubes: {cubes} FPS: {int(100*clock.get_fps())/100}", True, (0, 0, 0))
    window.blit(counter, (game.width / 18, game.height / 32))
# Detects hits
def hitDetect():
    global alive, cubes
    hits = pygame.sprite.groupcollide(targets, arrows, True, True)
    for hit in hits:
            cubes -= 1
            spawn()
            archer.hits += 1
    hits = pygame.sprite.groupcollide(movingtargets, arrows, True, True)
    for hit in hits:
            cubes -= 1
            spawn()
            archer.hits += 1
    hits = pygame.sprite.groupcollide(healthtargets, arrows, True, True)
    for hit in hits:
            cubes -= 1
            spawn()
            archer.hits += 1
            archer.health += 1
    hits = pygame.sprite.groupcollide(airstriketargets, arrows, True, True)
    for hit in hits:
            cubes -= 1
            spawn()
            archer.hits += 1
    hits = pygame.sprite.groupcollide(bombtargets, arrows, True, True)
    for hit in hits:
            cubes -= 1
            spawn()
            archer.hits += 1
    hits = pygame.sprite.spritecollide(archer, airstriketargets, False)
    for hit in hits:
            archer.health = 0
    hits = pygame.sprite.spritecollide(archer, avoids, True)
    if hits:
            archer.health -= 1
    if archer.health <= 0:
            alive = False
def intro():
    # Intro loop
    all_sprites.empty()
    intro = True
    while intro:
            game.checkquit()
            window.fill((255, 255, 255))
            game.text.still(int(game.width/4), "archer", (game.width/2), (game.height/3))
            game.text.still(int(game.width/36), "alpha arcade v0.3d", (game.width/7), (game.height/1.01))
            game.text.still(int(game.width/16), "press enter to start", (game.width/2), (game.height/1.5))
            archer.render()
            all_sprites.update()
            all_sprites.draw(window)
            pygame.display.update()
            clock.tick(60)
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                    intro = False
                    all_sprites.empty()
                    game.init()
                    spawn()
class mob:
    def target():
        t = Target()
        all_sprites.add(t)
        targets.add(t)
    def healthTarget():
        ht = HealthTarget()
        all_sprites.add(ht)
        healthtargets.add(ht)
    def buffTarget():
        bt = BuffTarget()
        all_sprites.add(bt)
        bufftargets.add(bt)
    def movingTarget():
        mt = MovingTarget()
        all_sprites.add(mt)
        movingtargets.add(mt)
    def airstrikeTarget():
        x = random.randint(int(game.boundary), int(game.width - game.width / 8))
        y = -2 * game.height
        ati = AirstrikeTargetIndicator(x, y)
        all_sprites.add(ati)
    def bombTarget():
        et = BombTarget()
        all_sprites.add(et)
        bombtargets.add(et)
    def buffBombTarget():
        bbt = BuffBombTarget()
        all_sprites.add(bbt)
        buffbombtargets.add(bbt)
def spawn():
    global cubes, healthPack
    cubes += 1
    healthPack += 1
    roll = random.randint(0, 99)
    if healthPack == 10:
        healthPack = 0
        mob.healthTarget()
    elif (0 <= archer.hits < 20):
        mob.target()
    elif (50 > archer.hits >= 20):
        if roll <= 20:
            mob.buffTarget()
        elif roll <= 25:
            mob.bombTarget()
        else:
            mob.target()
    elif (100 > archer.hits >= 50):
        if roll <= 25:
            mob.movingTarget()
        elif roll <= 50:
            mob.buffTarget()
        elif roll <= 75:
            mob.bombTarget()
        elif roll <= 85:
            mob.buffBombTarget()
        else:
            mob.target()
    elif (150 > archer.hits >= 100):
        if roll <= 5:
            mob.airstrikeTarget()
        elif roll <= 25:
            mob.buffBombTarget()
        elif roll <= 50:
            mob.bombTarget()
        elif roll <= 75:
            mob.movingTarget()
        elif roll <= 95:
            mob.buffTarget()
        else:
            mob.target()
    else:
        if roll <= 5:
            mob.airstrikeTarget()
        elif roll <= 45:
            mob.buffBombTarget()
        elif roll <= 75:
            mob.movingTarget()
        elif roll <= 85:
            mob.buffTarget()
        elif roll <= 100:
            mob.bombTarget()
        else:
            mob.buffTarget()
def updateDifficulty():
    global spawnRate, milestone, cubes
    if (archer.hits == 5) and milestone == True:
        milestone = False
        spawn()
    if archer.hits == 6:
        milestone = True
    if (archer.hits % 20 == 0) and (archer.hits != 0)and milestone and (archer.hits < 70):
        spawn()
        milestone = False
    if (archer.hits % 10 == 0) and milestone and (archer.hits != 0) and (archer.hits < 15):
        spawn()
        milestone = False
    if (archer.hits % 10 == 1):
        milestone = True
def loop():
    global alive
    global spawnRate
    # Main game loop
    running = True
    alive = True
    while running:
            clock.tick(game.fps)
            game.checkquit() # Checks if game is being quit, will close game if true.
            game.checkpause()
            game.update()
            hitDetect()
            window.fill((255,255,255))
            display()
            all_sprites.draw(window)
            pygame.display.flip()
            game.checkBest()
            if alive == False:
                    game.text.still(int(game.width/4), "you lost", (game.width/2), (game.height/3))
                    game.text.still(int(game.width/16), f"your score: {archer.hits}", (game.width/2), (game.height/2.2))
                    game.text.still(int(game.width/16), f"best score: {highScore}", (game.width/2), (game.height/2))
                    game.text.still(int(game.width/20), "press enter to play again", (game.width/2), (game.height/1.7))
                    game.text.still(int(game.width/20), "or escape to quit", (game.width/2), (game.height/1.6))
                    pygame.display.flip()
                    while alive == False:
                        clock.tick(60)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()
                            key = pygame.key.get_pressed()
                            if key[pygame.K_RETURN]:
                                    archer.health = 5
                                    archer.hits = 0
                                    all_sprites.empty()
                                    game.init()
                                    spawn()
                                    alive = True
                            if key[pygame.K_ESCAPE]:
                                    pygame.quit()
                                    quit()
# Set game caption/resolution
pygame.display.set_caption('archer 0.3d')
window = pygame.display.set_mode((game.width, game.height))
# Game functions
game.saveValid()
intro()
loop()
pygame.quit()
quit()
