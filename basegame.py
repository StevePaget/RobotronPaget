from pygame_functions import *

setAutoUpdate(False)


class Player():
    def __init__(self):
        self.xpos = 400
        self.ypos = 400
        self.speed = 3
        self.health = 100
        self.xdir = 0
        self.ydir = 0
        self.sprite = makeSprite("smalllinks.gif",32)
        showSprite(self.sprite)
        self.frame = 0
        self.timeOfNextFrame = clock()
        self.lastBulletTime = clock()
        self.score = 0

    def move(self):
        if clock() > self.timeOfNextFrame:  # We only animate our character every 80ms.
            self.frame = (self.frame + 1) % 8  # There are 8 frames of animation in each direction
            self.timeOfNextFrame += 80  # so the modulus 8 allows it to loop

        if keyPressed("a"):
            self.xpos -= self.speed
            changeSpriteImage(self.sprite,  2*8+self.frame)
            self.xdir = -1
        elif keyPressed("d"):
            self.xpos += self.speed
            changeSpriteImage(self.sprite,  0*8+self.frame)
            self.xdir = 1
        else:
            self.xdir = 0

        if keyPressed("w"):
            self.ypos -= self.speed
            changeSpriteImage(self.sprite, 3*8+self.frame)
            self.ydir = -1
        elif keyPressed("s"):
            self.ypos += self.speed
            changeSpriteImage(self.sprite, 1*8+self.frame)
            self.ydir = 1
        else:
            self.ydir = 0

        moveSprite(self.sprite, self.xpos, self.ypos)

    def update(self):
        self.move()
        if keyPressed("z"):
            if clock() > self.lastBulletTime + 30:
                # add a new bullet to the list of bullets
                if self.xdir == 0 and self.ydir == 0:
                    self.ydir=-1
                bullets.append(Projectile(self.xpos + 20, self.ypos + 20, self.xdir * 10, self.ydir * 10, 0))
                self.lastBulletTime = clock()


class Projectile():
    def __init__(self, xpos, ypos, xspeed, yspeed, damage):
        self.xpos = xpos
        self.ypos = ypos
        self.xspeed = xspeed
        self.yspeed = yspeed

        self.sprite = makeSprite("greendot.png")
        self.move()
        showSprite(self.sprite)

    def move(self):
        self.xpos += self.xspeed
        self.ypos += self.yspeed
        if self.xpos < 0 or self.xpos > 800 or self.ypos < 0 or self.ypos > 800:
            return False
        moveSprite(self.sprite, self.xpos, self.ypos)
        return True


screenSize(800, 800)
setBackgroundColour([10,40,40])
p = Player()

scoreLabel= makeLabel("Score: 0", 22, 10, 10, fontColour='green', 
                     font='consolas')
showLabel(scoreLabel)

enemies = []

bullets = []  # make an empty list of bullets
while True:
    p.update()
    for e in enemies:
        e.move(p)
        if e.checkHits(bullets, p) == True:
            enemies.remove(e)
            
    for bullet in bullets:  # ask each bullet in the list to move
        if bullet.move() == False:
            hideSprite(bullet.sprite)
            bullets.remove(bullet)
    updateDisplay()
    tick(60)
endWait()
