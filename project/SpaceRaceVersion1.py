import pygame
import pygame as pg

import os
from os import path

import csv
from random import randint, randrange
import sys

#Character Sprites Source: https://secrethideout.itch.io/team-wars-platformer-battle
#Pause Button Source: https://www.seekpng.com/ipng/u2a9o0o0u2e6o0q8_pause-button-png-transparent-image-pause-button-orange/
#Space Level Screen Images Source (Including Level Beat Image) : https://wallpaperaccess.com/4k-space
#Countdown Screen Astronaut Image Source: https://wallpapersden.com/astronaut-lost-in-space-wallpaper/7680x4320/
#Game Beat Image Source: https://asd.gsfc.nasa.gov/blueshift/index.php/2015/07/04/cosmic-fireworks/

#Health Pack Source: http://pixelartmaker.com/art/2ede25037e61e96
#Ammo Pack Source: http://pixelartmaker.com/art/1ae0e10a611b08b
#Bomb Sprite Source: https://www.pngfind.com/mpng/bxJxxi_mario-bomb-enimey-pokemon-mega-stone-sprite-hd

#Level Background Music Source: https://www.youtube.com/watch?v=hufv8MFlRdE&ab_channel=VeyselAytekin
#Level Beat Victory Screen Music Source: https://www.youtube.com/watch?v=DzkklgSJf8o&ab_channel=PSC
#Game Beat Victory Screen Music Source: https://www.youtube.com/watch?v=nnfx4FKvSTY&ab_channel=Xleno
#Main Menu and Character Select Screen Music Source: https://www.youtube.com/watch?v=Q_JVEXDrJYg&t=70s&ab_channel=lilletor

SCREENWIDTH = 800
SCREENHEIGHT = int(SCREENWIDTH * 0.8)



pg.init()

pg.mixer.init()
  
SCREENWIDTH = 800
SCREENHEIGHT = int(SCREENWIDTH * 0.8)

screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pg.display.set_caption('Shooter')

#set framerate
clock = pg.time.Clock()
FPS = 30

#define some global game variables

#Gravity to be applied when jumping
GRAVITATIONALFORCE = 0.75
#How far from the edge of the screen the player should be before the screen scrolls
SCROLLTHRESHOLD = 200
#Row, column, and tile size for level processing and building
ROWS = 16
COLS = 150
TILESIZE = SCREENHEIGHT // ROWS
#The number of tile assets present for the levels
DISTINCTTILES = 21
#Number of levels the game will have
TOTALLEVELS = 2
#Setting some initial variables that should always be applied when the application is started
screenscrollstatus = 0
bgscrollstatus = 0
level = 1
startgame = False
startintro = True

#Some player action variables that should always intially be these values upon application start
movingleft = False
movingright = False
shoot = False
bomb = False
bombthrown = False

pg.time.set_timer(pg.USEREVENT, 1000)

#Creating the image directory folder to easily have access to some images in the image folder
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder,'Shooter-files','img')

#Images used for the buttons of the application
startbuttonimage = pg.image.load(path.join(img_folder,'startbuttonnew.png')).convert_alpha()

exitbuttonimage = pg.image.load(path.join(img_folder,'quitbuttonnew.png')).convert_alpha()

restartbuttonimage = pg.image.load(path.join(img_folder,'restartbuttonnew.png')).convert_alpha()
restartimagered = pg.image.load(path.join(img_folder,'restartbuttonnew2.png')).convert_alpha()

mainmenuimage = pg.image.load(path.join(img_folder,'mainmenubuttonnew.png')).convert_alpha()
mainmenuimagered = pg.image.load(path.join(img_folder,'mainmenubuttonnew2.png')).convert_alpha()

pausebuttonimage = pg.image.load(path.join(img_folder,'pause_btn.png')).convert_alpha()
unpausebuttonimage = pg.image.load(path.join(img_folder,'unpausebuttonnew.png')).convert_alpha()

gobuttonimage = pg.image.load(path.join(img_folder,'gobuttonnew.png')).convert_alpha()
continuebuttonimage = pg.image.load(path.join(img_folder,'continuebuttonnew.png')).convert_alpha()


#Level display and status screen images

level1img = pg.image.load(path.join(img_folder,'level1image.jpg')).convert_alpha()
level1img = pg.transform.scale(level1img, (SCREENWIDTH,SCREENHEIGHT))

level2img = pg.image.load(path.join(img_folder,'level2image.jpeg')).convert_alpha()
level2img = pg.transform.scale(level2img, (SCREENWIDTH,SCREENHEIGHT))

level3img = pg.image.load(path.join(img_folder,'level3image.png')).convert_alpha()
level3img = pg.transform.scale(level3img, (SCREENWIDTH,SCREENHEIGHT))

levelbeatimage = pg.image.load(path.join(img_folder, 'victoryimage.png'))
levelbeatimage = pg.transform.scale(levelbeatimage, (SCREENWIDTH,SCREENHEIGHT))

victoryimage = pg.image.load(path.join(img_folder, 'victoryimage2.jpg'))
victoryimage = pg.transform.scale(victoryimage, (SCREENWIDTH,SCREENHEIGHT))

deathscreenimage = pg.image.load(path.join(img_folder, 'deathscreen.jpg'))
deathscreenimage = pg.transform.scale(deathscreenimage, (SCREENWIDTH,SCREENHEIGHT))

countdownimage = pg.image.load(path.join(img_folder, 'countdownimage.jpg'))
countdownimage = pg.transform.scale(countdownimage, (SCREENWIDTH,SCREENHEIGHT))

#An image for the title on the main screen
titleimage = pg.image.load(path.join(img_folder,'titleimage2.png')).convert_alpha()
titlewidth = int(titleimage.get_width())
titleheight = int(titleimage.get_height())
titlescale = .6 #Allows flexibility for the scaling
titleimage = pg.transform.scale(titleimage, (int(titlewidth*titlescale),int(titleheight*titlescale)))

#Loading idle shooter pictures for different colors for the color select screens
#'Shooter-files/img/player/Black/Idle/0.png'
blackidle_shooter = pg.image.load('Shooter-files/img/player/Black/Idle/0.png').convert_alpha()
redidle_shooter = pg.image.load('Shooter-files/img/player/Red/Idle/0.png').convert_alpha()
greenidle_shooter = pg.image.load('Shooter-files/img/player/Green/Idle/0.png').convert_alpha()
yellowidle_shooter = pg.image.load('Shooter-files/img/player/Yellow/Idle/0.png').convert_alpha()
blueidle_shooter = pg.image.load('Shooter-files/img/player/Blue/Idle/0.png').convert_alpha()


#Loading scrolling space background for the games levels
spacesize = (SCREENWIDTH, SCREENHEIGHT)
spaceimage = pg.image.load('Shooter-files/img/Background/pixelspace2.png').convert_alpha()
spaceimage = pg.transform.scale(spaceimage, spacesize)

#Taking the separate tiles used for level building and placing them in a list to be
#accessed by the world processor.
#This method was inspired by the Tiled Level editor program
imagelist = []
for x in range(DISTINCTTILES):
    image = pg.image.load(f'Shooter-files/img/Tile/{x}.png')
    image = pg.transform.scale(image, (TILESIZE, TILESIZE))
    imagelist.append(image)

#Loading laser image
lasersize = (10,10)
laserimage = pg.image.load('Shooter-files/img/icons/laser (1).png').convert_alpha()
laserimage = pg.transform.scale(laserimage, lasersize)

#Loading bomb image
bombimage = pg.image.load('Shooter-files/img/icons/mariobomb2.png').convert_alpha()

#Loading support item images
#'Shooter-files/img/{self.character}/{self.herocolor}/{status}/{i}.png')
healthpickupimage = pg.image.load('Shooter-files/img/icons/newhealth_box.png').convert_alpha()
ammopickupimage = pg.image.load('Shooter-files/img/icons/newammo_box.png').convert_alpha()
bombpickupimage = pg.image.load('Shooter-files/img/icons/newgrenade_box.png').convert_alpha()

#Creating a dictionary with the separate support boxes to use when processing the world
#All in same dictionary as items that add to the players resevoirs
#Associating the item images with keys to be referenced in the world processing
items = {
    'Health'    : healthpickupimage,
    'Ammo'      : ammopickupimage,
    'Bomb'   : bombpickupimage
}

#Pathway to Load Audio Files For Easier Locating
audio_folder = path.join(game_folder,'Shooter-files','audio')

#Sound for when the player jumps
#Source: https://www.youtube.com/watch?v=_eqKyzxa0dM&t=15s&ab_channel=AllSounds
jumpsound = pg.mixer.Sound(path.join(audio_folder,'normaljump.wav'))
jumpsound.set_volume(.06)

#Sound for when shooting occurs in the game
#Source: https://www.youtube.com/watch?v=9M2FPuIADuI&ab_channel=AllSounds
shotsound = pg.mixer.Sound(path.join(audio_folder,'LaserSound.wav'))
shotsound.set_volume(.06)

#Explosion sound for the bomb
#Source: https://www.youtube.com/watch?v=EA4h8l2zZ1g&ab_channel=CreatorAssets
bombsound = pg.mixer.Sound(path.join(audio_folder,'grenadeexplosion.wav'))
bombsound.set_volume(.25)

#Loading sound for when land in water
#Source: https://www.youtube.com/watch?v=_eqKyzxa0dM&t=15s&ab_channel=AllSounds
watersplash = pg.mixer.Sound(path.join(audio_folder,'watersplash.wav'))
watersplash.set_volume(.8)

#Loading sound for when die
#Source: https://www.youtube.com/watch?v=ipJKjqmK_uU&t=74s&ab_channel=AllSounds
deathsound1 = pg.mixer.Sound(path.join(audio_folder,'DeathSound1.wav'))
deathsound1.set_volume(.5)

#Loading sound for when pickup items
#Source: https://www.youtube.com/watch?v=Q_4fGDa6f7Y
itempickupsound = pg.mixer.Sound(path.join(audio_folder,'itempickup.wav'))
itempickupsound.set_volume(.3)

#Loading short clip of music that plays when you die.
#Source: https://www.youtube.com/watch?v=j_nV2jcTFvA
deathmusic = pg.mixer.Sound(path.join(audio_folder,'darksoulsdeathmusic.wav'))
deathmusic.set_volume(.6)

#Loading in the colors to be used in the game
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
FUCHSIA = (255,0,255)
INDIGO = (75, 0, 130)
BLUE = (0,0,255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
PINK = (255, 20, 147)
YELLOW = (255,255,0)
#Setting background color
BG = GREEN



#Loading in the Universal Font for the Game
font = pg.font.SysFont('Robus', 30)



#Function to draw the background of the game
def drawbackground():
    screen.fill(GREEN)

    width = spaceimage.get_width()
    #Projecting the background of the game one after another 5 times to account for the size of the map a
    #and for how much the background has scrolled
    for x in range(5): 
        screen.blit(spaceimage, ((x * width)- bgscrollstatus * 0.2, SCREENHEIGHT- spaceimage.get_height() ))
#Simple function when want to draw text on the screen
def drawtext(text, font, textcolor, x, y):
    image = font.render(text, True, textcolor)
    screen.blit(image, (x, y))

   
#Referenced http://codingwithruss.com/pygame/shooter/player.html  for help with this.
#Guide was helpful for many of the in game mechanics. 
class Shooter(pg.sprite.Sprite):
    def __init__(self, character, x, y, scale, speed, ammo, bombs, herocolor):
        pg.sprite.Sprite.__init__(self)
        
        #Variables for all Shooters
        self.alive = True
        self.character = character
        self.ammo = ammo
        self.initammo = ammo
        self.speed = speed
        self.shotcooldown = 0
        self.bombs = bombs
        self.health = 1000
        self.maxhealth = self.health
        self.direction = 1
        self.yvel = 0
        self.jump = False
        self.airborne = True
        self.flip = False
        self.spriteanimationlist = []
        #Frame indices
        self.indexframe = 0
        #number to be changed based on action being taken
        self.action = 0
        self.timeupdate = pg.time.get_ticks()
        self.herocolor=herocolor
        
        #enemy variables
        self.movetotal = 0
        # "Vision" for the enemy/ the rectangle that the player has to move
        #into for the enemy to "see" them and attack them
        self.vision = pg.Rect(0, 0, 150, 20)
        #Variable for the status of the enemy. (If idling or not)
        self.idling = False

        #Used to track idle time
        self.idlingcounter = 0

        
        

        #setting up a list of the sprite folders for the different player and enemy statuses
        statustypes = ['Idle', 'Run', 'Jump', 'Death']
        
        #For every status, type access the images associated with them, and add them in order to a list to be animated
        #Strategy based off of what was learned from https://www.simplifiedpython.net/pygame-sprite-animation-tutorial/ and 
        #https://pythonprogramming.altervista.org/animation-with-pygame/
        for status in statustypes:
            #reset temporary list of images
            temporaryimagelist = []
            #count number of files in the sprite folder
            framenumber = len(os.listdir(f'Shooter-files/img/{self.character}/{self.herocolor}/{status}'))
            for i in range(framenumber):
                image = pg.image.load(f'Shooter-files/img/player/{self.herocolor}/{status}/{i}.png').convert_alpha()
                image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
                temporaryimagelist.append(image)
            self.spriteanimationlist.append(temporaryimagelist)

        self.image = self.spriteanimationlist[self.action][self.indexframe]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


    #updating the animations and checking if the player is alive repeatedly
    def update(self):
        
        self.updateanimation()
        self.checklifestatus()
        #continuously updating the cooldowns for shots
        if self.shotcooldown > 0:
            self.shotcooldown -= 1


    def move(self, movingleft2, movingright2):
        #Resetting the variables for movement
        screenscrollstatus = 0

        #Change in x for moving left or right
        xchange = 0
        #Change in y for moving up or down
        ychange = 0
        
        #If moving left
        if movingleft2 == True:
            #move in negative x direction at speed set
            xchange = -self.speed
            #flip the sprite so they are facing proper direction
            self.flip = True
            #Change this variable so that other items from enemies and players go in the proper direction (-x)
            self.direction = -1
        if movingright2 == True:
            #move in positive x direction at speed set
            xchange = self.speed
            #no need to flip the sprite
            self.flip = False
            self.direction = 1

        #If player trying to jump and they are on the ground propel them into the air
        #To prevent double and triple and even more jumps, making sure that the player is not in the air before
        #allowing a jump
        if self.jump == True and self.airborne == False:
            #Determines how high get off ground when jump
            self.yvel = -20
            #Resetting the variable for the next time they are on the ground so they can jump again
            #and so they do not continuously jump upon hitting the ground
            self.jump = False
            #Make this true since they are in the air.
            #As a result this conditional will not run until they hit the ground and this variable
            #is set to fals 
            self.airborne = True
            #playing the loaded sound for jumping
            jumpsound.play()

        #Applying gravity for when in the air
        self.yvel += GRAVITATIONALFORCE
        #Gravity and Jumping Mechanics Based on What Was Found Here:
        #https://opensource.com/article/19/11/simulate-gravity-python
        #https://stackoverflow.com/questions/16551009/gravity-in-pygame
        #https://coderslegacy.com/python/pygame-gravity-and-jumping/

        #Never letting the rate at which you slow down in the air and fall down pass 
        if self.yvel > 15:
            self.yvel
        ychange += self.yvel

        #Checking for collisions with the worlds obstacles
        for tile in world.obstacle_list:
            #Checks x direction collisions and stops the player if collide
            if tile[1].colliderect(self.rect.x + xchange, self.rect.y, self.width, self.height):
                xchange = 0
                
                #Turns the enemy in the opposite direction if they collide with an obstacle 
                #and resets their step total taken in a directions
                if self.character == 'enemy':
                    self.direction = self.direction * -1
                    self.movetotal = 0
            #Checks y direction collisions and stops vertical movement as such
            if tile[1].colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                
                #If the player is jumping and they collide, there ascent is halted
                if self.yvel < 0:
                    self.yvel = 0

                    # Initial distance that should be between the player and the tile when collide (so player not in the tile)
                    ychange = tile[1].bottom - self.rect.top

                #if the player is falling and they collide, their descent is halted
                elif self.yvel >= 0:
                    self.yvel = 0
                    #Since they would be on the ground, the should be allowed to jump again.
                    self.airborne = False
                    
                    # Initial distance that should be between the player and the tile when collide (so player not in the tile)
                    ychange = tile[1].top - self.rect.bottom
        #Checking for collision with the water obstacle
        
        if pg.sprite.spritecollide(self, watergroup, False):
            #plays the water splashing sound
            watersplash.play()
            #kills the player
            self.health = 0
            #plays the death sound
            deathsound1.play()
            #sets the death music back to normal since muted once player clicks off death screen
            deathmusic.set_volume(.6)
            #plays the death music
            deathmusic.play()

        #resetting the variable to false everytime the game is running nad a level is not complete
        levelcomplete = False
        #Checking for collision with the finish line marker
        if pg.sprite.spritecollide(self, finishlinegroup, False):
            #sets this variable to true to that game can update and move on from this level
            levelcomplete = True

        #Checking if below the screen/level
        if self.rect.bottom > SCREENHEIGHT:
            #kills player
            self.health = 0

            #plays death sound and music
            deathsound1.play()

            deathmusic.set_volume(.6)

            deathmusic.play()



        #Check if going off the edge of the level
        if self.character == 'player':
            if self.rect.left + xchange < 0 or self.rect.right + xchange > SCREENWIDTH:
                #Stops player movement if they are
                xchange = 0

        #Updates the players rectangle position used for collision detection
        self.rect.x += xchange
        self.rect.y += ychange
        #Scrolling implementation used https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame as reference
        #Tracks the location of the players soldier and scrolls the screen based on where they are
        if self.character == 'player':
            #if the player is close enough to the right edge of the screen and the level scrolling is not at the end scroll the level(tiles) right
            #or if the player is close enough to the left edge of the screen and the background has scrolled far enough from beginning scroll the level left 
            if (self.rect.right > SCREENWIDTH - SCROLLTHRESHOLD and bgscrollstatus < (world.levellength * TILESIZE) - SCREENWIDTH)\
                or (self.rect.left < SCROLLTHRESHOLD and bgscrollstatus > abs(xchange)):
                #move the player level position the same amount so it looks like the level is moving with the player
                self.rect.x -= xchange
                screenscrollstatus = -xchange
        #Returns how far the level is scrolled and if the player beat the level 
        return screenscrollstatus,levelcomplete



    def shoot(self):
        #allows the player to shoot if the cooldown is up and they have ammo
        if self.shotcooldown == 0 and self.ammo > 0:
            self.shotcooldown = 20 #resets the cooldown
            #adds a laser to the sprite group so will see it and ensures that it appears in right position
            laser = Laser(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            lasergroup.add(laser)
            #Takes one laser away
            self.ammo -= 1
            #Plays the shot sound
            shotsound.play()

            #flashes the Muzzle in the proper position (same position as bullet) to mimic a real gun
            muzzleflash= MuzzleFlash(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction), self.rect.centery, 0.3)
            muzzleflashgroup.add(muzzleflash)

    #An enemy only function
    def ai(self):
        if self.alive and player.alive:          
            #check if the enemy is close enough to the player they will face them and shoot at them.
            if self.vision.colliderect(player.rect):
                #Adapting the idle movement
                self.actionupdater(0)#0: idle
                #They start shooting
                self.shoot()
            #When not in view of the player
            else:
                #if not idling
                if self.idling == False:
                    #move in the direction they are facing (depending on where player is)
                    if self.direction == 1:
                        aimovingright = True
                    else:
                        aimovingright = False
                    #ensures that these two variables cannot be the same
                    #cant be moving left and right at the same time
                    aimovingleft = not aimovingright
                    #they move in the set direction
                    self.move(aimovingleft, aimovingright)
                    #Running Action (Proper Sprites)
                    self.actionupdater(1)
                    #Adds a move to their move total to track when they should turn around
                    self.movetotal += 1
                    #Changes the boundary that the player has to enter for them to stop as the enemy moves
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)

                    #if move more than a tile they should turn in the opposite direction
                    if self.movetotal > TILESIZE:
                        self.direction = self.direction * -1
                        self.movetotal = self.movetotal * -1
                #Counting down to when they should stop idling 
                else:
                    self.idlingcounter -= 1
                    if self.idlingcounter <= 0:
                        self.idling = False

        #moving enemy hitbox with the map
        self.rect.x += screenscrollstatus


    def updateanimation(self):
        #https://www.reddit.com/r/pygame/comments/g2eoqv/how_would_one_implement_a_cooldown_in_an_oop/
        #animation cooldown idea developed from here on
        #Preventing immediate awkward animation changes that make animating objects look odd
        animationcooldown = 130
        #updates the sprite to be displayed based on the action being taken
        self.image = self.spriteanimationlist[self.action][self.indexframe]
        #Checking if can update the animation or not based on time and does if can
        if pg.time.get_ticks() - self.timeupdate > animationcooldown:
            self.timeupdate = pg.time.get_ticks()
            self.indexframe += 1
        #If the sprite animations have been run through completely, restart them
        if self.indexframe >= len(self.spriteanimationlist[self.action]):
            #Except if it is for death, want it to stay on the last frame so it doesnt play the death animation again
            if self.action == 3:
                self.indexframe = len(self.spriteanimationlist[self.action]) - 1
            else:
                self.indexframe = 0



    def actionupdater(self, newaction):
        #Only actually change the sprites being animated if different action is taking place and not the same one. So can move on to other sprites in the sequence
        #instead of resetting every time the animation is triggered
        if newaction != self.action:
            self.action = newaction
            #if change sprites being referenced from, start from the first sprite in that sprite set every time.
            self.indexframe = 0
            self.timeupdate = pg.time.get_ticks()


    #check if the player is alive
    def checklifestatus(self):
        if self.health <= 0:
            #stop health from being negative and messing up health bar calculations
            self.health = 0
            #they shouldn't move
            self.speed = 0
            #makes sure the game knows they are dead
            self.alive = False

            #plays the death sprite sequence from the beginning
            self.actionupdater(3)
            

    #draw the players and enemies in the proper orientations and proper sprites
    def draw(self):
        screen.blit(pg.transform.flip(self.image, self.flip, False), self.rect)

class Water(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        #water location
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self):
        #move hitbox with the screen/level 
        self.rect.x += screenscrollstatus

#Class for game aesthetics and the obstacles
class Aesthetic(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        #location of decorations in a tile based on the top middle of the rectangle
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self):
        #move their hitboxes with the screen
        self.rect.x += screenscrollstatus


class FinishLine(pg.sprite.Sprite):
    def __init__(self, image, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))

    def update(self):
        #move hitbox with the screen/level
        self.rect.x += screenscrollstatus


#Class for the different in game items
class ItemBox(pg.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pg.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = items[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILESIZE // 2, y + (TILESIZE - self.image.get_height()))


    def update(self):
        #Move item hitboxes with the scrolling status of the screen
        self.rect.x += screenscrollstatus
        #Checks if player has collided with the item
        if pg.sprite.collide_rect(self, player):
            itempickupsound.play()
            #Different effects based on the type of item in the item dictionary
            #Adds health if touch health item
            if self.item_type == 'Health':
                player.health += 1000000
                if player.health > player.maxhealth:
                    player.health = player.maxhealth
            #Adds ammo and bombs if touch those items
            elif self.item_type == 'Ammo':
                player.ammo += 15
            elif self.item_type == 'Bomb':
                player.bombs += 3
            #deletes the item from the map once the player touches it
            self.kill()

#Bomb class
class Bomb(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.timer = 100
        self.yvel = -11
        self.speed = 7
        self.image = bombimage
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.direction = direction

    def update(self):
        #Makes sure that bombs fall when thrown just like the player when jumps
        self.yvel += GRAVITATIONALFORCE
        #Creating parabolic trajectory for the bomb
        xchange = self.direction * self.speed
        ychange = self.yvel

        #Checks if the bomb collides with the level
        for tile in world.obstacle_list:
            #If collides with walls bounces back in opposite direction
            if tile[1].colliderect(self.rect.x + xchange, self.rect.y, self.width, self.height):
                self.direction =self.direction * -1
                xchange = self.direction * self.speed
            #If collides with ground stops moving
            if tile[1].colliderect(self.rect.x, self.rect.y + ychange, self.width, self.height):
                self.speed = 0
                #If collides with platform above it when thrown up stops and maintains minimum distance to prevent clipping
                if self.yvel < 0:
                    self.yvel = 0
                    ychange = tile[1].bottom - self.rect.top
                #if collides with platform below it when falling it stops and maintains a minimum distance to prevent clipping
                elif self.yvel >= 0:
                    self.yvel = 0
                    ychange = tile[1].top - self.rect.bottom 


        #Changing the bombs position and hitbox position while accounting for scroll of the level
        self.rect.x += xchange + screenscrollstatus
        self.rect.y += ychange

        #How long it takes the bomb to explode upon being thrown
        self.timer -= 1
        if self.timer <= 0:
            #blows the bomb up and removes it from the game
            self.kill()
            #plays the explosion sound
            bombsound.play()
            #runs the explosion animation
            explosion = Explosion(self.rect.x, self.rect.y, 0.5)
            explosion_group.add(explosion)
            #Damages both players and enemies in the vicinity upon exploding
            if abs(self.rect.centerx - player.rect.centerx) < TILESIZE * 2 and \
                abs(self.rect.centery - player.rect.centery) < TILESIZE * 2:
                player.health -= 50
            for enemy in enemygroup:
                if abs(self.rect.centerx - enemy.rect.centerx) < TILESIZE * 2 and \
                    abs(self.rect.centery - enemy.rect.centery) < TILESIZE * 2:
                    enemy.health -= 50


#Button Class with design inspiration from PSET 8 Javascript
#For the many buttons in the game
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pg.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        #So all buttons do not think they are clicked upon being drawn
        self.clicked = False 

    def draw(self, surface):
        #Default variable to return.
        #Always false unless clicked
        isclicked= False

        #Gets mouse position
        mousepos = pg.mouse.get_pos()
        #Checks if mouse has been cliccked
        click=pg.mouse.get_pressed()
        
        
        if self.rect.collidepoint(mousepos):
            #if clicked and currently is not clicked provides feedback
            if click[0] == 1 and self.clicked == False:
                #returns true if clciked so conditional statement where button is will run
                isclicked = True
                self.clicked = True
                
                #self.clicked=False

        #If unclicked or not clicked the button doesnt do anything
        if click[0] == 0:
            self.clicked = False

        #drawing the button in the desired position
        surface.blit(self.image, (self.rect.x, self.rect.y))
        
        #returning isclicked and will run whatever button is supposed to if true
        return isclicked

#Class for the displayed health bar
class HealthBar():
    def __init__(self, x, y, health, maxhealth):
        self.x = x
        self.y = y
        self.health = health
        self.maxhealth = maxhealth
    def draw(self, health):
        global healthcolor

        #Updates the health bar based on the player's health
        self.health = health
        
        #calculate health ratio
        percent = self.health / self.maxhealth

        #Changes health bar color based on percentage of health left
        if percent >  .60:
            healthcolor = FUCHSIA
        elif percent > .30:
            healthcolor = CYAN
        else:
            healthcolor = RED
##        if option == 1:
            
        #print(percent)

        #pg.draw.rect(screen, BLACK, (self.x - 2, self.y - 2, 404, 24))
            #pg.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        #Draws health bar at the top of the screen and decreases its size based on health left.
        pg.draw.rect(screen, healthcolor, (self.x, self.y, 400 * percent, 20))

#Laser class 
class Laser(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        pos=(x,y)
        self.speed = 20
        self.image = laserimage
        self.rect = self.image.get_rect()
        self.direction = direction
        self.vel=(self.direction* self.speed)
        self.rect.center = pos
    def update(self):
        #Moving the laser and adjusting for map scrolling
        self.rect.x += self.vel + screenscrollstatus
        #Kill the laser if it is off the screen
        if self.rect.right < 0 or self.rect.left > SCREENWIDTH:
            self.kill()
        #If laser hits a tile, kill it
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()

        #If laser hits a player, take off health and kill it
        if pg.sprite.spritecollide(player, lasergroup, False):
            if player.alive:
                player.health -= 3
                self.kill()
            #Play the death sound if a laser hits and the player is dead
            if player.health == 0:
                deathsound1.play()
                deathmusic.set_volume(.6)
                deathmusic.play()
        #If hits an enemy, the laser takes health away from it and disappears
        for enemy in enemygroup:
            if pg.sprite.spritecollide(enemy, lasergroup, False):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()



class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y, scale):
        pg.sprite.Sprite.__init__(self)
        self.images = []
        #Sprite animation for the explosions
        for num in range(0, 15):
            image = pg.image.load(f'Shooter-files/img/explosion/tile0{num}.png').convert_alpha()
            #scaling the explosion pictures to the proper size for the animation
            image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            self.images.append(image)
        self.indexframe = 0
        self.image = self.images[self.indexframe]
        self.rect = self.image.get_rect()
        pos= (x,y)
        self.rect.center = pos
        self.counter = 0


    def update(self):
        #scroll
        self.rect.x += screenscrollstatus

        
        #variable for how fast the explosion progresses
        #Higher it is the slower
        explosionvelocity = 4
        #update explosion amimation
        self.counter += 1
        #
        if self.counter >= explosionvelocity:
            self.counter = 0
            self.indexframe += 1
            #Once the explosion has completed it disappears
            if self.indexframe >= len(self.images):
                self.kill()
            #If not it runs through the explosion
            else:
                self.image = self.images[self.indexframe]

#CLass for Muzzle Flashing upon shooting
class MuzzleFlash (pg.sprite.Sprite):
    def __init__(self, x, y, scale):
        pg.sprite.Sprite.__init__(self)
        size = randint(20,50)
        self.pos = (x,y)
        
        #same sprite animation used for player to animate the muzzle flashing
        self.images = []
        for num in range (12,17):
            image = pg.image.load(f'Shooter-files/img/icons/MuzzleFlashing/tile0{num}.png').convert_alpha()
            image = pg.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
            self.images.append(image)
        self.indexframe = 0
        self.image = self.images[self.indexframe]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0
    def update(self):
        self.rect.x += screenscrollstatus
        #instantaneous flash speed but can change variable to make it slower
        #higher it is the slower
        flashspeed = 0
        self.counter += 1
        if self.counter >= flashspeed:
            self.counter = 0
            self.indexframe += 1
            #stops the muzzle flash after one run through
            if self.indexframe >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.indexframe]
#class to fade the screen for more seamless transitions
class screenfader():
	def __init__(self, direction, color, speed):
		self.direction = direction
		self.color = color
		self.speed = speed
		self.fadetracker = 0


	def fade(self):
        #so nothing proceeds until the fade has completed
		fadecomplete = False
		self.fadetracker += self.speed
        #a whole screen fade in
		if self.direction == 1:
            #brings in rectabgles from the left right top and bottom to slowly uncover the screen 
			pg.draw.rect(screen, self.color, (0 - self.fadetracker, 0, SCREENWIDTH // 2, SCREENHEIGHT))
			pg.draw.rect(screen, self.color, (SCREENWIDTH // 2 + self.fadetracker, 0, SCREENWIDTH, SCREENHEIGHT))
			pg.draw.rect(screen, self.color, (0, 0 - self.fadetracker, SCREENWIDTH, SCREENHEIGHT // 2))
			pg.draw.rect(screen, self.color, (0, SCREENHEIGHT // 2 +self.fadetracker, SCREENWIDTH, SCREENHEIGHT))
        #A top screen fade out
		if self.direction == 2:
            #Draws a rectangle that only gets larger in the y direction
			pg.draw.rect(screen, self.color, (0, 0, SCREENWIDTH, 0 + self.fadetracker))
        #Once done a
		if self.fadetracker >= SCREENWIDTH:
			fadecomplete = True

		return fadecomplete

#World processor based on experience with Tiled map building and how to get tiled maps into Pygame
#Referenced and Used https://www.pygame.org/project/5513 to build the map by searching Pygame Level Editor
#Data processor made to work with this.
#Understood using KidsCanCode Youtube Channel
class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data):
        global colhero
        global colvillain
        global player
        global water
        global aesthetic
        global enemy
        global itembox
        global health_bar
        

        
        self.levellength = len(data[0])
        #Iterate through all of the values in the Level Data CSV file 
        #All objects being applied to their classes
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    image = imagelist[tile]
                    image_rect = image.get_rect()
                    image_rect.x = x * TILESIZE
                    image_rect.y = y * TILESIZE
                    tile_data = (image, image_rect)
                    #Creating world/wall tiles if tiles have png name within these values
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                   #Water class objects
                    elif tile >= 9 and tile <= 10:
                        water = Water(image, x * TILESIZE, y * TILESIZE)
                        watergroup.add(water)
                    #Decoration Onjects
                    elif tile >= 11 and tile <= 14:
                        aesthetic = Aesthetic(image, x * TILESIZE, y * TILESIZE)
                        aestheticsgroup.add(aesthetic)
                    #The Player Object
                    elif tile == 15:
                        player = Shooter('player', x * TILESIZE, y * TILESIZE, 1.65, 8, 10000, 30, colhero)
                        health_bar = HealthBar(10, 10, player.health, player.health)
                    #The Enemy Object
                    elif tile == 16:
                        enemy = Shooter('enemy', x * TILESIZE, y * TILESIZE, 1.65, 2, 1000000000, 40,colvillain)
                        enemygroup.add(enemy)
                    #The Ammo Object
                    elif tile == 17:
                        itembox = ItemBox('Ammo', x * TILESIZE, y * TILESIZE)
                        itemgroup.add(itembox)
                    #The bomb object
                    elif tile == 18:
                        itembox = ItemBox('Bomb', x * TILESIZE, y * TILESIZE)
                        itemgroup.add(itembox)
                    #The health object
                    elif tile == 19:
                        itembox = ItemBox('Health', x * TILESIZE, y * TILESIZE)
                        itemgroup.add(itembox)
                    #the finish line object
                    elif tile == 20:
                        finish = FinishLine(image, x * TILESIZE, y * TILESIZE)
                        finishlinegroup.add(finish)

        return player, health_bar
    #Drawing the tiles for the game
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screenscrollstatus
            screen.blit(tile[0], tile[1])
#Creating the Screen Fades
introfade = screenfader(1, BLACK, 1)
deathfade = screenfader(2, RED, 4)
victoryfade = screenfader(2, BLUE, .5)
winfade = screenfader(2, GREEN, .3)



class Game:
    def __init__(self):
        global level
        global SCREENWIDTH
        global SCREENHEIGHT
        global showselect
        global showenemyselect
        global counter


        pg.init()
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        pg.display.set_caption('CS50 Shooter Sidescroller')
        self.clock = pg.time.Clock()
        FPS = 30
        #Initial Colors for the player and enemy as backups just in case the select screens are bypassed
        colhero='Yellow'
        colvillain='Black'
        
        #Set to false as to not show the select screens until the program sets them to true
        showselect=False
        showenemyselect=False
        
        #pg.time.set_timer(pg.USEREVENT, 500)
        
        #Defines these variables as false to be modified to true later in the program to trigger certain game screens
        self.levelshow=False
        self.levelbeatmusic = False
        self.mainmenumusic = False
        
        self.obstacle_list = []

    #Creating and loading in all the sprite groups for the first time.
    def new(self):
        global aestheticsgroup
        global enemygroup
        global lasergroup
        global bombgroup
        global explosion_group

        global itemgroup
        global muzzleflashgroup
        global watergroup
        global finishlinegroup
        global world
        global colhero
        global colvillain
        global level
        level=1
        #with open('savefile.dat', 'rb') as f:
            #level=pickle.load(f)
        #Will show the level the person is on upon them choosing characters and starting the game
        self.levelshow = True
        
        #More variables that will be set to true to show certain screens
        self.levelbeat = False
        self.gamebeat = False
        self.trueorfalse = False

        #Creating the Sprite Groupsthat get added to in the functions and classes above as the game runs.
        #These groups are created right at the start of the application running
        enemygroup = pg.sprite.Group()
        lasergroup = pg.sprite.Group()
        bombgroup = pg.sprite.Group()
        explosion_group = pg.sprite.Group()
        muzzleflashgroup = pg.sprite.Group()
        itemgroup = pg.sprite.Group()
        aestheticsgroup = pg.sprite.Group()
        watergroup = pg.sprite.Group()
        finishlinegroup = pg.sprite.Group()
        
        #Empty list to contain the world data
        worldinfo = []
        for row in range(ROWS):
            r = [-1] * COLS
            worldinfo.append(r)
        #Loading in the level data created from the CSV file from the level editor to load in the world
        with open(f'Shooter-files/level{level}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    worldinfo[x][y] = int(tile)
        world = World()
        player, health_bar = world.process_data(worldinfo)

        self.paused = False
        #self.draw_debug = False
    def run(self):
        #globalizing variable used outside game class
        global colhero
        global colvillain
        global startgame
        global levelshow
        global startintro

        #Set true so that whenever this function is called, the game is running
        self.playing = True
        

        while self.playing:
            #If the game is not paused and the level is not beat, sprites will update and the game will run
            if not self.paused and self.levelbeat == False:
                #checks if music is playing and if it isnt it unpauses the music that is called to play
                if pg.mixer.music.get_busy()==False:
                
                    pg.mixer.music.unpause()
                
                self.update()
                self.events()

                self.draw() 

            #if this variable is true it shows the level about to be played
            if self.levelshow == True:
                self.showlevelscreen()
            #Congratulatory screen for beating the level is showed
            if self.levelbeat == True:
                self.showlevelbeatscreen()
            #Congratulatory screen for beating the game is showed
            if self.gamebeat ==  True:
                self.showwinscreen ()
            #shows the fade out of the blocks when the game starts
            if startintro == True:
                #pg.display.update()
                if introfade.fade():
                        startintro = False
                        introfade.fadetracker = 0 
            
            #Pauses playing music upon calling the pause screen
            if self.paused:
                
                pg.mixer.music.pause()
                self.showpausescreen()
            
            #Shows the losing screen
            #Only triggers when die
            if self.exitvar==True:
                self.showdeathscreen()

            #Always looking for key input while game running
            self.get_keys()
            
            #So that updates actually displayed on screen
            pg.display.update()




    #Function for properly quitting the game and closing the pygame window 
    def quit(self):
        pg.quit()
        sys.exit()
    def update(self):
        #Updating all sprite classes as game variables change
        lasergroup.update()
        bombgroup.update()
        explosion_group.update()
        muzzleflashgroup.update()
        itemgroup.update()
        aestheticsgroup.update()
        watergroup.update()
        finishlinegroup.update()
    
    #Drawing objects to display while the game is running
    def draw(self):
        global colhero
        global colvillain

        #Initializing the font to be used for text shown while the game is running
        gamefont = pg.font.SysFont('cooperblack', 20)
        
        #Draws the background
        drawbackground()
        
        #Draws the tiles for the world
        world.draw()
        #Draws the health bar
        health_bar.draw(player.health)
        #Defining the Pause Button and drawing it right after
        pausebutton = Button(SCREENWIDTH-45, SCREENHEIGHT // 2 -315, pausebuttonimage, .04)
        if pausebutton.draw(screen):
            self.paused = True
        
        #Drawing Text and displaying the number of lasers and bombs left
        drawtext('LASERS: ', gamefont, WHITE, 8, 33)
        drawtext(f'{player.ammo}', gamefont, RED, 105, 33)

        
        drawtext('BOMBS: ', gamefont, WHITE, 8, 57)
        drawtext(f'{player.bombs}',gamefont, BLUE, 100, 57)

        drawtext('HEALTH: ', gamefont, WHITE, 8, 81 )
        drawtext(f'{player.health}', gamefont, healthcolor, 105, 81)

        
        #Updating the players animations and drawing it
        player.update()
        player.draw()            
        
        #Drawing and loading in the enemy will all its data
        for enemy in enemygroup:
            enemy.ai()
            enemy.update()
            enemy.draw()
        
        #Drawing all the sprite groups on the screen
        lasergroup.draw(screen)
        bombgroup.draw(screen)
        explosion_group.draw(screen)
        muzzleflashgroup.draw(screen)
        itemgroup.draw(screen)
        aestheticsgroup.draw(screen)
        watergroup.draw(screen)
        finishlinegroup.draw(screen)
    
    #Function that checks for main changes in status as the game runs
    def events(self):
        global startintro
        global player
        global laser
        global bomb
        global bombthrown
        global explosion
        global muzzleflash
        global bgscrollstatus
        global screenscrollstatus
        global level
        global bombgroup
        global world

        #So death screen is not shown until set true
        self.exitvar=False
        #Shows the intro fade in
        if startintro == True:
            if introfade.fade():
                startintro = False
                introfade.fadetracker = 0 
        restartbutton = Button(SCREENWIDTH // 2 - 100, SCREENHEIGHT // 2 - 50, restartbuttonimage, 2)
        
        #Allows players actions to be updated if he is alive 
        if player.alive:
            #Shoots when space is pressed
            if shoot:
                player.shoot()
            #Throws bombs when variables are set true by a button press
            elif bomb and bombthrown == False and player.bombs > 0:
                #bomb to be thrown is created using the defined Bomb Class
                bomb = Bomb(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),\
                            player.rect.top, player.direction)
                #Adds to sprite group so will be shown
                bombgroup.add(bomb)
                #decreases bomb amount
                player.bombs -= 1
                bombthrown = True
            
            #If airborne changes the sprite to the jump sprite by going to that directory using the index number
            if player.airborne:
                player.actionupdater(2)
            
            #Running Sprite  
            elif movingleft or movingright:
                player.actionupdater(1)
            
            #If not those it must be idling sprite
            else:
                player.actionupdater(0)

            #Level scrolling status changes as player moves
            #Checks if player came across end of level while alive
            screenscrollstatus,levelcomplete = player.move(movingleft, movingright)
            bgscrollstatus -= screenscrollstatus
            if levelcomplete:
                    #startintro = True
                    self.levelbeat=True

       #If the player is dead
        else:
            
            #Stops the Music
            if pg.mixer.music.get_busy()==True:
                pg.mixer.music.stop()
            
            #Sets this to True to trigger the death screen and the music that follows
            self.exitvar=True

    #Function for the death screen
    def showdeathscreen(self):
        global startgame
        global startintro
        global itembox
        global bgscrollstatus
        global screenscrollstatus
        global level
        global world
        
        #Buttons to be shown on this screen
        deathrestartbutton = Button(SCREENWIDTH // 2 - 190, SCREENHEIGHT // 2 -70, restartimagered, 1)
        deathmainmenubutton = Button(SCREENWIDTH // 2 - 230, SCREENHEIGHT // 2 +50, mainmenuimagered, 1)
        #Font for this screen
        deathfont1 = pg.font.SysFont('Chiller', 80, bold = True)

        #Set to 0 since will be starting at the beginning of a level
        screenscrollstatus = 0
        #Resets the background scroll status back to initial value since restarting game
        bgscrollstatus = 0

        #Background for the screen
        self.screen.fill(RED)
        self.screen.blit(deathscreenimage,(0,0))

        #Text for screen being drawn
        drawtext('You Died', deathfont1, WHITE, SCREENWIDTH // 2 -115, SCREENHEIGHT // 2-250)
        
        #Drawing the restart button for the death screen and setting what is done if it pressed
        if deathrestartbutton.draw(screen):
                #shows a new level
                self.levelshow=True
                #lowers the volume of the death sound if still playign so does not interfere with game background music
                deathmusic.set_volume(0)

                #starts playing the game background music
                self.playbgmusic()
                
                #Set to true so that the intro fade can show
                startintro = True


                #Clears the sprite groups and loads a new world based on the level (as will pick that CSV file to extract data from)
                worldinfo = self.resetlevel()
                with open(f'Shooter-files/level{level}.csv', newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate(row):
                            worldinfo[x][y] = int(tile)
                world = World()
                player, health_bar = world.process_data(worldinfo)
                
        if deathmainmenubutton.draw(screen):
            #ends the run loop and fully restarts the game as if were just starting the application up
            startgame=False
            self.playing=False
            #Stops playing of death music if still playing
            deathmusic.set_volume(0)
            #startgame=False
    #Function for playing the level background music
    def playbgmusic(self):
        bgmusic='BGMUSIC.mp3'            
        pg.mixer.init()
        #accessing file from audio folder
        pg.mixer.music.load(path.join(audio_folder,bgmusic))
        pg.mixer.music.set_volume(0.05)
        #play infinitely
        pg.mixer.music.play(-1)
    #Function for playing music when beat the game
    def playvictorymusic(self):
        victorymusic='victorymusic.mp3'
        pg.mixer.init()
        pg.mixer.music.load(path.join(audio_folder,victorymusic))
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)
    #Function for playing music when beat a level
    def playlevelbeatmusic(self):
        levelbeatmusic='levelbeatmusic.mp3'
        pg.mixer.init()
        pg.mixer.music.load(path.join(audio_folder,levelbeatmusic))
        pg.mixer.music.set_volume(0.05)
        pg.mixer.music.play(-1)
    #Function for playing music on the main menu 
    def playmainmenumusic(self):
        mainmenumusic='mainmenumusic.mp3'
        pg.mixer.init()
        pg.mixer.music.load(path.join(audio_folder,mainmenumusic))
        pg.mixer.music.set_volume(0.1)
        pg.mixer.music.play(-1)
    
    #Function for countdown screen upon starting the game
    def showcountdown(self):

        countdowntimer=1
        dt= 0
        done = False
        #Fonts used on the countdown screen
        countdownfont = pg.font.SysFont('cooperblack', 50)
        countdownfont2 = pg.font.SysFont('cooperblack', 60)
        #gamefont = pg.font.SysFont('cooperblack', 20)

        #Runs until done (so when done is set to true)
        while not done:
            countdowntimer -=dt

            #Once to display once the timer is done
            if round(countdowntimer) <=0:
                #Shows new screen background and text
                self.screen.fill(PINK)
                self.screen.blit(countdownimage,(0,0))

                drawtext('START!!!', countdownfont2, WHITE, SCREENWIDTH // 2 -130, SCREENHEIGHT // 2-30)
                pg.display.flip()
                #So the player can see what is displayed
                pg.time.delay(2000)
                done=True
                
                #done=True
            else:
                
                self.screen.fill(PINK)
                
                #Rounding so only see the whole number during countdown
                timertext=str(round(countdowntimer))

                self.screen.blit(countdownimage,(0,0))

                #Text to be displayed for the countdown screen
                drawtext('Your Game Will Begin In', countdownfont, WHITE, SCREENWIDTH // 2-320, SCREENHEIGHT // 2-100)
                drawtext(timertext,countdownfont2,CYAN,SCREENWIDTH // 2-20, SCREENHEIGHT // 2)
                drawtext('Seconds', countdownfont, WHITE, SCREENWIDTH // 2-100, SCREENHEIGHT // 2+100)
                #Allows it to be shown
                pg.display.flip()
                #Counting down in seconds based on time passed since last time this was displayed. 
                #Since looping continousuly will lead to accurate time
                dt = clock.tick(30) / 1000  

    #Function for the screen that shows what level the player is about to start.
    def showlevelscreen(self):
        global level
        global startintro

        #Fonts
        levelfont = pg.font.SysFont('Bangers', 80, bold=True)
        levelfont = pg.font.SysFont('cooperblack', 70)


        dt=0

        #Based on how fast game loops/refreshes leads to accurate amount of time looking at level screen
        leveltimer=170

        done = False
        
        levelcolor=None

        #Runs this while done is false
        while not done:
            leveltimer -= dt

            if round(leveltimer) <= 0:
                
                done=True
                self.levelshow=False
                #done=True
            self.screen.fill(YELLOW)
            #Determines what image and color font is chosen based on level about to be played
            if level == 1:
                self.screen.blit(level1img,(0,0))
                levelcolor = RED
            if level == 2:
                self.screen.blit(level2img,(0,0))
                levelcolor = CYAN
            if level == 3:
                self.screen.blit(level3img,(0,0))
                levelcolor = GREEN


            drawtext(f'Level {level}',levelfont,levelcolor,SCREENWIDTH // 2-350, SCREENHEIGHT // 2-210)
            
            pg.display.flip()

            #What decreasing timer by every loop
            dt = .033
        
        #After done sets this to true so the fade in is run right before starting the level
        startintro=True
     
    def showstartscreen(self):
        global startgame
        global showselect
        global showenemyselect



        pg.display.set_caption('CS50 Sidescrolling Shooter')
        clock = pg.time.Clock()

        #Empty Lists to add Star Location Data to for Dynamic Background
        slowstars = []
        intermediatestars = []
        faststars = []

        
        #Creating slow stars and adding there random locations to a list to be displayed
        for nothing in range(100): 
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            slowstars.append([xstarlocation, ystarlocation]) 

        #Creating medium paced stars
        for nothing in range(50):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            intermediatestars.append([xstarlocation, ystarlocation])

        #Creating fast paced stars
        for nothing in range(35):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            faststars.append([xstarlocation, ystarlocation])


        #Run until a button is pressed as buttons on this screen change one of these values
        while startgame==False and showselect==False:
            #Establishing quit buttons in the main menu alongside the normal one
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.quit()

            self.screen.fill(BLACK)

            for stars in slowstars:
                stars[1] += 1 #Adding To the Y Locations Slowly
                #If star goes off the screen it brings it back to the top in a random location
                #off the screen so it appears on screen again
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                #Star attributes
                pg.draw.circle(screen, FUCHSIA, stars, 5)

            for stars in intermediatestars:
                stars[1] += 5 #Adding to the Y Locations Moderately
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, WHITE, stars, 3)

            for stars in faststars:
                stars[1] += 8 #Adding to the Y Locations Fast
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, CYAN, stars, 2)
            
            #defining the main menu buttons
            startbutton = Button(SCREENWIDTH // 2 - 200, SCREENHEIGHT // 2+175, startbuttonimage, .8)
            exitbutton = Button(SCREENWIDTH // 2 +50, SCREENHEIGHT // 2 +175, exitbuttonimage, .8)

            #Commands the playing of the main menu music once so doesnt eternally loop and never actually play
            if self.mainmenumusic == False:
                self.playmainmenumusic()
                self.mainmenumusic = True 
            
            #Drawing Buttons
            if startbutton.draw(screen):  
                showselect=True
            if exitbutton.draw(screen):
                self.quit()
            
            #Blitting the title words which is an image rather than text
            self.screen.blit(titleimage,(SCREENWIDTH //2 -317, SCREENHEIGHT // 2 -50))

            #redraw everything we've asked pygame to draw
            pg.display.flip()

            #set frames per second
            clock.tick(30)

        #Moves game to select screen if true
        if showselect==True:
            self.showselectscreen()
            #self.mainmenumusic = True
        #Moves game to enemy select screen if true
        if showenemyselect==True:
            
            self.showenemyselectscreen()
            #self.mainmenumusic = False
            #pg.display.update()

    def showselectscreen(self):
        global colhero
        global startgame
        global showenemyselect
        
        pg.event.get()
        
        #Displacement Variable for all character select images
        selectdisplacement=200
        

        clock = pg.time.Clock()
        
        #Defining buttons for the select screen
        redidle_button = Button(SCREENWIDTH // 2 - 365, SCREENHEIGHT // 2 -selectdisplacement, redidle_shooter, 5)
        blueidle_button = Button(SCREENWIDTH // 2 - 215, SCREENHEIGHT // 2 - selectdisplacement, blueidle_shooter, 5)
        greenidle_button = Button(SCREENWIDTH // 2 -65, SCREENHEIGHT // 2 - selectdisplacement, greenidle_shooter, 5)
        yellowidle_button = Button(SCREENWIDTH // 2 +85, SCREENHEIGHT // 2 - selectdisplacement, yellowidle_shooter, 5)
        blackidle_button = Button(SCREENWIDTH // 2 +235 , SCREENHEIGHT // 2 - selectdisplacement, blackidle_shooter, 5)

        select1font=pg.font.SysFont("algerian",40,bold=True)

        ##Same Dynamic Background So Comments For Main Menu Dynamic Background Apply Here##

        #Empty Lists to add Star Location Data to for Dynamic Background
        slowstars = []
        intermediatestars = []
        faststars = []

        for nothing in range(100):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            slowstars.append([xstarlocation, ystarlocation])

        for nothing in range(50):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            intermediatestars.append([xstarlocation, ystarlocation])

        for nothing in range(15):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            faststars.append([xstarlocation, ystarlocation])

        #Runs until a character color is chosen
        while showenemyselect==False:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.quit()

            self.screen.fill(BLACK)

            for stars in slowstars:
                stars[1] += 1
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, FUCHSIA, stars, 5)

            for stars in intermediatestars:
                stars[1] += 4
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, WHITE, stars, 3)

            for stars in faststars:
                stars[1] += 8
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, YELLOW, stars, 2)

            
            drawtext("Choose the Hero's (Your) Color", select1font, WHITE, SCREENWIDTH // 2 -375, SCREENHEIGHT // 2 - 250)

            #Buttons for selecting a character color
            #Upon pressing set a color for the hero character
            if redidle_button.draw(screen):
                colhero='Red'

                showenemyselect=True
                
            if blueidle_button.draw(screen):
                colhero='Blue'

                showenemyselect=True            
               
            if greenidle_button.draw(screen):
                colhero='Green'
                
                showenemyselect=True            
                
            if yellowidle_button.draw(screen):
                colhero='Yellow'
                
                showenemyselect=True            
                
            if blackidle_button.draw(screen):
                colhero='Black'
                
                showenemyselect=True
            pg.display.flip()

            #set frames per second
            clock.tick(30)
  
            
    def showenemyselectscreen(self):
        global colvillain
        global startgame
        global bgscrollstatus
        
        
        #Vertical Displacement for pictures
        selectdisplacement=0

        #Defining Buttons and Fonts
        redidle2_button = Button(SCREENWIDTH // 2 - 365, SCREENHEIGHT // 2 -selectdisplacement, redidle_shooter, 5)
        blueidle2_button = Button(SCREENWIDTH // 2 - 215, SCREENHEIGHT // 2 - selectdisplacement, blueidle_shooter, 5)
        greenidle2_button = Button(SCREENWIDTH // 2 -65, SCREENHEIGHT // 2 - selectdisplacement, greenidle_shooter, 5)
        yellowidle2_button = Button(SCREENWIDTH // 2 +85, SCREENHEIGHT // 2 - selectdisplacement, yellowidle_shooter, 5)
        blackidle2_button = Button(SCREENWIDTH // 2 +235 , SCREENHEIGHT // 2 - selectdisplacement, blackidle_shooter, 5)
        select1font=pg.font.SysFont("algerian",40,bold=True)

        ##Same Dynamic Background So Comments For Main Menu Dynamic Background Apply Here##

        slowstars = []
        intermediatestars = []
        faststars = []

        for nothing in range(100): 
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            slowstars.append([xstarlocation, ystarlocation])

        for nothing in range(50):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            intermediatestars.append([xstarlocation, ystarlocation])

        for nothing in range(35):
            xstarlocation = randrange(0, SCREENWIDTH)
            ystarlocation = randrange(0, SCREENHEIGHT)
            faststars.append([xstarlocation, ystarlocation])
                      
        #Shows until the game is started
        while startgame==False:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self.quit()

            self.screen.fill(BLACK)

            for stars in slowstars:
                stars[1] += 1
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, FUCHSIA, stars, 5)

            for stars in intermediatestars:
                stars[1] += 4
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, WHITE, stars, 3)

            for stars in faststars:
                stars[1] += 8
                if stars[1] > SCREENHEIGHT:
                    stars[0] = randrange(0, SCREENWIDTH)
                    stars[1] = randrange(-15, -3)
                pg.draw.circle(screen, RED, stars, 2)
            
            #Draws text and buttons for this screen
            drawtext("Choose the Enemy Color", select1font, WHITE, SCREENWIDTH // 2 -300, SCREENHEIGHT // 2 - 250)

            if redidle2_button.draw(screen):
                colvillain='Red'
                startgame=True
                
            if blueidle2_button.draw(screen):
                colvillain='Blue'
                startgame=True
                
            if greenidle2_button.draw(screen):
                colvillain='Green'
                startgame=True
                
            if yellowidle2_button.draw(screen):
                colvillain='Yellow'
                startgame=True
                
            if blackidle2_button.draw(screen):
                colvillain='Black'
                startgame=True


            pg.display.flip()

            #set frames per second
            clock.tick(30)

    #Function for showing the pause screen
    def showpausescreen(self):
        global startgame
        global bgscrollstatus
        global screenscrollstatus

        #Defining and displaying the buttons for the screen
        unpausebutton = Button(SCREENWIDTH//2-188, SCREENHEIGHT // 2 -80, unpausebuttonimage, 1)
        mainmenu2_button = Button(SCREENWIDTH // 2 - 235, SCREENHEIGHT // 2 +50, mainmenuimage, 1)
        #unpauses game
        if unpausebutton.draw(screen):
            self.paused=False
        #Resets game as if first started it up
        if mainmenu2_button.draw(screen):
            bgscrollstatus = 0
            screenscrollstatus=0
            startgame=False
            self.playing=False
    
    #Function for screen that shows up when beat a level
    def showlevelbeatscreen(self):
        global level
        global startgame
        global bgscrollstatus
        global screenscrollstatus
        global world
        global player
        global colhero

        #Defining fonts and buttons for the screen
        levelbeatfont=pg.font.SysFont("algerian",30,bold=True)
        levelbeatfont2=pg.font.SysFont("algerian",25,bold=True)
        levelbeatmainmenubutton = Button(SCREENWIDTH // 2 - 235, SCREENHEIGHT // 2 +45, mainmenuimage, 1)
        continuelevelbeatbutton = Button(SCREENWIDTH // 2 - 222, SCREENHEIGHT // 2 +180, continuebuttonimage, 1)
        
        #If have not beat the game actually shows the level beat screen
        if level < TOTALLEVELS:
            #stops the music that is playing if the level beat music isn't playing
            if self.levelbeatmusic == False:
                pg.mixer.music.stop()
            #Does the victory fade and then shows the victory screen
            #alongside playing the victory music
            if victoryfade.fade():
                if self.levelbeatmusic == False:
                    self.playlevelbeatmusic()
                    self.levelbeatmusic = True

                #Text and background for level beat screen
                self.screen.fill(BLUE)
                self.screen.blit(levelbeatimage,(0,0))
                                

                drawtext(f'You Beat Level {level}', levelbeatfont,WHITE,SCREENWIDTH // 2 -160, SCREENHEIGHT // 2 - 250)
                drawtext ('Congrats!!!',levelbeatfont,WHITE, SCREENWIDTH // 2 -110, SCREENHEIGHT // 2 - 150)
                drawtext('Select Below To Continue or Return to Main Menu', levelbeatfont2, WHITE, SCREENWIDTH // 2 -370,SCREENHEIGHT // 2 - 50)

                #Main Menu Button for the Screen
                if levelbeatmainmenubutton.draw(screen):
                    bgscrollstatus = 0
                    pg.mixer.music.stop()
                    self.levelbeat = False
                    self.levelbeatmusic=False
                    startgame=False
                    self.playing=False
                    #fadetracker set to 0 so can run from start next time it is triggered
                    victoryfade.fadetracker = 0
                    
                #Continue to next level button
                if continuelevelbeatbutton.draw(screen):
                    
                    #Changing the Level so can load a different map
                    level += 1
                    #with open('savefile.dat', 'wb') as f:
                        #pickle.dump([level, colhero], f, protocol=2)

                    #Shows the level
                    self.levelshow=True

                    #Starts playing the background music
                    self.playbgmusic()
                    #Makes sure the background has no scroll
                    bgscrollstatus = 0

                    #resets the level
                    worldinfo = self.resetlevel()

                    #Since starting a new level, changes these back to false so not displayed and 
                    #so can be triggered at the appropriate time
                    self.levelbeat = False
                    self.levelbeatmusic = False
                    victoryfade.fadetracker = 0
                    #Loads a new world
                    #if level < TOTALLEVELS:
                        #self.dt = self.clock.tick(FPS) / 1000.0 
                        #load in level data and create world
                    with open(f'Shooter-files/level{level}.csv', newline='') as csvfile:
                        reader = csv.reader(csvfile, delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                worldinfo[x][y] = int(tile)
                    world = World()
                    player, health_bar = world.process_data(worldinfo)

        #Transfers to the win screen rather than showing the level beat one
        else:
            self.gamebeat = True
                
    #Function for the win screen of the game  
    def showwinscreen(self):
        global level
        global startgame
        global bgscrollstatus
        global screenscrollstatus
        global counter

        #Defining the button and font for the screen
        winmainmenubutton = Button(SCREENWIDTH // 2 - 235, SCREENHEIGHT // 2 -20, mainmenuimage, 1)
        winfont = pg.font.SysFont('cooperblack', 20)

        #stops music playing
        if self.trueorfalse == False:
            pg.mixer.music.stop()
        #Shows the win fade and then shows the screen
        if winfade.fade():
            self.screen.fill(GREEN)
            self.screen.blit(victoryimage,(0,0))
            drawtext('CONGRATULATIONS!!! YOU BEAT THE GAME!!!', winfont,WHITE,SCREENWIDTH // 2 -240, SCREENHEIGHT // 2 - 250)
            drawtext('THANK YOU FOR PLAYING THE GAME!!!',winfont, WHITE,SCREENWIDTH // 2 -220, SCREENHEIGHT // 2 - 150)

            #Runs command to play victory music once (since conditional variable changed) to prevent
            #an infinite loop that will cause the song to never play
            if self.trueorfalse == False:
                
                self.playvictorymusic()
                self.trueorfalse=True
                
            #Displaying the Win Button
            if winmainmenubutton.draw(screen):
                #Resets the status of the fade blocks for next time
                winfade.fadetracker = 0
                #Resets how far the game background scrolled since done with level and won game
                bgscrollstatus = 0


                #Halts music
                pg.mixer.music.stop()
                #Resets these variables as to stop the game from running and to display the start screen again
                startgame=False
                self.playing=False
                #Resets this variable so can be set to true and the level beat screen can be displayed another time when right
                self.levelbeat = False
                

            
        
    #Getting the keys to be used in the game    
    def get_keys(self):
        #Globalizing Variables that Appear Outside of the Class
        global movingleft
        global movingright
        global shoot
        global bomb
        global bombthrown
        
        #Pygames event catalog is being searched through
        events2=pg.event.get()
        for event in events2:
            
            #Does these actions below when that key is pressed down
            if event.type == pg.KEYDOWN:
                #Sets the variable ture when pressed so that player will move left 
                if event.key == pg.K_LEFT:
                    movingleft = True
                #Sets the variable true when pressed so that player will move right
                if event.key == pg.K_RIGHT:
                    movingright = True
                #Sets variable true so that the player will shoot
                if event.key == pg.K_SPACE:
                    shoot = True
                #Sets the variable true so that player throws a bomb
                if event.key == pg.K_q:
                    bomb = True
                #Sets the variable as true so that the game propels the player into the air
                if event.key == pg.K_UP and player.alive:
                    player.jump = True
                #Also quits the game    
                if event.key == pg.K_ESCAPE:
                    self.quit()
            #quits the game if the X Window Button is pressed
            if event.type == pg.QUIT:
                self.quit()


            #Does these actions below when that key is pressed up.
            #Variables are set to false so the actions are halted
            if event.type == pg.KEYUP:
                #Stops leftward movement 
                if event.key == pg.K_LEFT:
                    movingleft = False
                #Stops rightward movement
                if event.key == pg.K_RIGHT:
                    movingright = False
                #Stops shooting
                if event.key == pg.K_SPACE:
                    shoot = False
                #Stops bomb throwing
                if event.key == pg.K_q:
                    bomb = False
                    bombthrown = False
    
    #Returns empty world data to reset the world and load in new level data
    def resetlevel(self):
        enemygroup.empty()
        lasergroup.empty()
        bombgroup.empty()
        explosion_group.empty()
        muzzleflashgroup.empty()
        itemgroup.empty()
        aestheticsgroup.empty()
        watergroup.empty()
        finishlinegroup.empty()

        
        #create empty tile list
        tiledata = []
        for row in range(ROWS):
            #accounting for negatives in CSV for tile data
            r = [-1] * COLS
            tiledata.append(r)

        return tiledata

#Short hand for calling the game
g=Game()

while True:
    pg.event.get()
    clock.tick(FPS)
    
    #Shows the start screen when false
    #Usually coupled with a full reset
    if startgame==False:
        g.showstartscreen()
    
    #When changed after the start screen starts running the game contents including the other screens
    else:
              
        g.showcountdown()
        g.playbgmusic()
        g.new()

        g.run()
        #ensures that these variables are reset upon the stopping of the game being run and return to the main menu
        showselect=False
        showenemyselect=False
        g.mainmenumusic = False
        g.trueorfalse=False

    #updates screen
    pg.display.update()

        
            

                



            
            

        

        
