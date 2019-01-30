
import pygame, sys,random
import pygame.freetype
from pygame.locals import Color

pygame.init()
screen_width = 500
screen_height = 500
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("opruien")
keys = pygame.key.get_pressed()
tux_im = pygame.image.load ("tux.png")
achtergrond = pygame.image.load ('achtergrond.png')
back_music =  pygame.mixer.music.load("StereoMadness (1).mp3")
jump_music = pygame.mixer.Sound ("jump_01.WAV")
pygame.mixer.music.set_volume(0.2)
GAME_FONT = pygame.freetype.Font("Georgia.ttf", 24)




class Player (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255,0,0)
        self.width = 45
        self.height = 78
        self.x = screen_width - 400 
        self.y = screen_height - 60
        self.rect =  pygame.Rect (self.x, self.y, self.width, self.height)
        self.isJump = False #Als de player aan het springen is
        self.fall_velocity = 0 
        self.jump_velocity = 10
        self.isDead = False
        

    def show(self, group):
        self.rect = pygame.Rect(self.x, self.y , self.width, self.height)
        win.blit(tux_im,(self.x,self.y-2,self.width, self.height ))
        #pygame.draw.rect(win, self.color,(self.x , self.y, self.width, self.height))
        
    def jump (self):
        if keys[pygame.K_SPACE]:
            if self.isJump == False: # Als er op spatie wordt gedrukt en isJump is is False zeg dat hij wel aanhet springen is
                self.isJump = True
                jump_music.play()
                self.fall_velocity =-self.jump_velocity # Als de player springt maak je de val snelheid -10
        if self.isJump == True:
            self.y = self.y + self.fall_velocity   # Dus als hij springt maakt hij ook automatisch een daling           
            self.fall_velocity = self.fall_velocity + 0.75 # Die dalen gaat steeds niet iets sneller zodat je iets meer een echt spring gevoelt hebt
            
            
    def update (self, group):
        self.show(group)
        hits = pygame.sprite.spritecollide(self,group,False)
        if hits != []: # Als hits niet leeg is 
            for hit in hits: # Doe dan voor iedere hit in de hits het hier onderstaande
                if type (hit) == Bottom:
                    self.isJump = False
                    self.fall_velocity = 0
                    self.y = 400   #Dit doe ik omdat hij anders een klein beetje in de grond zakt
        self.jump() # Hier wordt de jump functie aangeroepen

class Enemy(pygame.sprite.Sprite):
    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 30
        self.height = 30
        self.x = screen_width - 100
        self.y = screen_height - 60
        self.rect =  pygame.Rect (self.x, self.y, self.width, self.height)
        self.speed = -8
        
        #Bepaal random type object
        randomGetal = random.randrange(0,2)
        if randomGetal == 0:
            self.color = (0,255,0)
            self.isEnemy = False         
        else:
            self.color = (255,0,0)
            self.isEnemy = True

    def setspeed(self,extraspeed):
        self.speed = self.speed + extraspeed
        
    def show (self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect( win, self.color,(self.x , self.y, self.width, self.height))

    def update(self,group):    
        hits = pygame.sprite.spritecollide(self,group,False) #check hit met Player
        if hits != []:
            for hit in hits:
                if not type (hit) == Enemy:
                    if type (hit) == Player:  
                        if self.isEnemy == True:
                            tux.isDead = True
                            del self
                            enemyList.pop()
                            return
                            
                        else:
                            board.addscore()     
                            del self
                            enemyList.pop()
                            return
                            
                                               
        
        if self.x <= 0:
            if self.isEnemy == True:
                board.addscore()
            else:
                board.minscore()
                
            #del self
            del self
            enemyList.pop()
            return
        
        self.x = self.x + self.speed
        self.show()

class Bottom(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255,255,255)
        self.width = screen_width
        self.height = 30
        self.x = screen_width-screen_width
        self.y = screen_height-30
        self.rect =  pygame.Rect (self.x, self.y, self.width, self.height)

    def show (self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect( win, self.color,(self.x , self.y, self.width, self.height))

    def update(self):
        self.show()

class Scoreboard (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.score = 0
        

    def addscore (self):
        self.score = self.score + 1
        print (self.score)

    def minscore (self):
        self.score = self.score - 1
        print (self.score)
        

        
balk = Bottom()       
#red_square = Enemy()
tux = Player()
board = Scoreboard ()
group = pygame.sprite.Group()
group.add(tux) #Doe bij de groep
group.add(balk) # ''
enemyList = []
#def sound_maker ():
tegenstanderTeller = 0

pygame.mixer.music.play(-1)        
run = True


while run:
    if tux.isDead:
        5*5
    else:
        text = str("Oke")
        c = pygame.Color(1,2,3)
        text = GAME_FONT.render(text, False )
        screen.blit(text, (50, 50))
        tegenstanderTeller = tegenstanderTeller +1  
        #counter or teller to not make enemy a every loop
        if (tegenstanderTeller  > 60):
            newEnemy = Enemy()
            group.add(newEnemy) # ''
            enemyList.append(newEnemy)
            tegenstanderTeller = 0

    
        win.fill((193, 103, 34))
        win.blit(achtergrond,(0,10))
        tux.update(group)
        balk.update()
        
        
    
   
        #Update alle enemy blokjes uit de lijst
        for oneEnemy in enemyList:
            oneEnemy.update(group)
    
    for event in pygame.event.get():   
        if event.type == pygame.QUIT:
            run = False
    keys = pygame.key.get_pressed()

    pygame.time.delay(10)
    pygame.display.update()

pygame.quit()
sys.exit()       
        
