import pygame, sys, random
import numpy as np
import time
from math import pi
class CatchGame:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        # Main Window
        self.screen_width = 1000
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption('Catch Game')

        # Colors
        self.light_grey = (200,200,200)
        self.bg_color = pygame.Color('#1A4D2E')
        self.player_color=pygame.Color('#d19402')
        self.opponent_color=pygame.Color('black')
        self.goal_color=pygame.Color('white')
        

        # Game Rectangles
        self.down=False
        self.up=False
        self.right=False
        self.left=False
        
        self.player = pygame.Rect(self.screen_width - 100, self.screen_height / 2 - 70, 50,50)
        self.opponent = pygame.Rect(400, self.screen_height / 2 - 70, 50,50)
        self.goal = pygame.Rect(10, self.screen_height / 2 - 70, 40, 40)
        self.pointt = pygame.Rect(self.screen_width / 2 - 5 , self.screen_height / 2 -27, 10, 10)

        # Game Variables
       
        self.player_speed_x=0

        self.opponent_speed_x=7

        self.player_speed = 20
        self.player_speed_x=20
        self.opponent_speed = 0
        self.opponent_speed_x=0
        self.opponent_speed2 = 6
        self.opponent_speed2_x = 6
        self.move=[0,0,0,0]
        self.move1=[0,0,0,0]
        self.last_colliderect_with=''

        # Score variables
        self.player_score = 0
        self.opponent_score = 0
        self.score=0
        self.basic_font = pygame.font.Font('freesansbold.ttf', 32)
        self.font1 = pygame.font.Font('freesansbold.ttf', 15)
        




    # Function for player movements 

    def _move(self, action):

        if action==[1,0,0,0]:
            self.move=[1,0,0,0]
            self.player.y += self.player_speed #([1,0,0,0] means go down)
        elif action==[0,1,0,0]:
            self.move=[0,1,0,0]
            self.player.y -= self.player_speed

        elif action==[0,0,1,0]:
            self.move=[0,0,1,0]
            self.player.x -= self.player_speed_x

        elif action==[0,0,0,1]:
            self.move=[0,0,0,1]
            self.player.x += self.player_speed_x
            
        if self.player.top <= 0:
            self.player.top = 0
        if self.player.bottom >= self.screen_height:
            self.player.bottom = self.screen_height

        if self.player.right>=self.screen_width:
            self.player.right=self.screen_width
        if self.player.left<=0:
            self.player.left=0
            

    def opponent_ai2(self):
        
        if self.opponent.x< self.player.x:
            self.opponent.x+=self.opponent_speed2_x
            self.down=False
            self.up=False
            self.right=True
            self.left=False
        
        if self.opponent.x> self.player.x:
            self.opponent.x-=self.opponent_speed2_x
            self.down=False
            self.up=False
            self.right=False
            self.left=True

        if self.opponent.y< self.player.y:
            self.opponent.y+=self.opponent_speed2
            self.down=True
            self.up=False
            self.right=False
            self.left=False

        
        if self.opponent.y> self.player.y:
            self.opponent.y-=self.opponent_speed2
            self.down=False
            self.up=True
            self.right=False
            self.left=False
    
        if self.opponent.top <= 0:
            self.opponent.top = 0
        if self.opponent.bottom >= self.screen_height:
            self.opponent.bottom = self.screen_height
        
        if self.opponent.right>=self.screen_width:
            self.opponent.right=self.screen_width
        if self.opponent.left<=0:
            self.opponent.left=0

    
    def game_start(self):
        

        self.player.center = (self.screen_width - 100, self.screen_height / 2 - 70)
        h=random.randint(100,600)
        self.opponent.center = (400, h)

   

    def play_step(self, action):
        
     
     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        # opponent move
        self.opponent_ai2()
       
        
        # player move
        self._move(action) 
        
        
        # check if game over
        reward = 0
        game_over = False

        if self.goal.colliderect(self.player):
            self.game_start()
            self.player_score += 1
            self.score+=self.score
           
            game_over=True
            reward=+10
            return reward, game_over, self.score	
        
        if self.opponent.colliderect(self.player):
            self.game_start()
            self.opponent_score += 1
            
            self.score=0
            game_over=True
            reward=-10
            return reward, game_over, self.score
        
        if self.player.top <= 0 or self.player.bottom >= self.screen_height or self.player.right>=self.screen_width or self.player.left<=0 :
            self.game_start()
            self.opponent_score += 1
            self.score=0
           
            game_over=True
            reward=-10
            return reward, game_over, self.score

        
        self.screen.fill(self.bg_color)

        # draw stadium

        pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width / 2, 12),(self.screen_width / 2, self.screen_height-12))

        pygame.draw.arc(self.screen, self.light_grey,[self.screen_width / 2 -110, 230, 220, 195], 0, pi/2, 2)
        pygame.draw.arc(self.screen, self.light_grey,[self.screen_width / 2 -110, 230, 220, 195], pi/2, pi, 2)
        pygame.draw.arc(self.screen, self.light_grey, [self.screen_width / 2 -110, 230, 220, 195], pi,3*pi/2, 2)
        pygame.draw.arc(self.screen, self.light_grey,  [self.screen_width / 2 -110, 230, 220, 195], 3*pi/2, 2*pi, 2)
        pygame.draw.ellipse(self.screen, self.light_grey, self.pointt)

        pygame.draw.aaline(self.screen, self.light_grey, (self.screen_width-12, 12),(self.screen_width-12, self.screen_height-12))
        pygame.draw.aaline(self.screen, self.light_grey, (12, 12),(self.screen_width-12, 12))
        pygame.draw.aaline(self.screen, self.light_grey, (12, self.screen_height-12),(self.screen_width-12, self.screen_height-12))
        pygame.draw.aaline(self.screen, self.light_grey, (12, 12),(12, self.screen_height / 2 -80))
        pygame.draw.aaline(self.screen, self.light_grey, (12, self.screen_height / 2 - 20),(12, self.screen_height-12))
        pygame.draw.arc(self.screen, self.light_grey,  [-86, 180, 200, 250], 3*pi/2, pi/2)

        
        # draw player - opponent - goal
        
        pygame.draw.rect(self.screen, self.player_color, self.player)
        pygame.draw.rect(self.screen, self.opponent_color, self.opponent)
        pygame.draw.rect(self.screen, self.goal_color, self.goal)
       

        # text score

        player_text = self.basic_font.render(f'{self.player_score}',False,self.light_grey)
        self.screen.blit(player_text,(self.screen_width-110,50))

        opponent_text = self.basic_font.render(f'{self.opponent_score}',False,self.light_grey)
        self.screen.blit(opponent_text,(110,50))

        

        pygame.display.flip()
        self.clock.tick(40)	


        
        #  score = distance between player and opponent ( greater distance equal greater score ) + distance between player and goal ( lower distance equal greater score )
        self.distance_x=np.abs(self.player.x - self.opponent.x)
        self.distance_y=np.abs(self.player.y - self.opponent.y)
        self.distance_goal_y=np.abs(self.goal.y - self.player.y)
        self.distance_goal_x=np.abs(self.goal.x - self.player.x)
        self.goal_score=np.abs((self.screen_width-(self.distance_goal_x)))+np.abs((self.screen_height-(self.distance_goal_y)))
        self.run_score=(self.distance_x+self.distance_y)/2
      
        self.score=self.goal_score+self.run_score
        print(self.score)
        
        
        return reward, game_over, self.score






