import torch
import random
import numpy as np
from catch_class_stable_03_09_2022 import CatchGame
from collections import deque

from model_stable_03_09_2022 import Linear_QNet, QTrainer

import time
MAX_MEMORY=100000
BATCH_SIZE=1000
LR=0.001

class Agent:
    def __init__(self):

        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(179, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        

    def get_state(self,game):

        # Choosing Features : feel free to choose your features as you want depending on your logic , 
        # think this way : if i was the player , what informations i need to achieve the goal ?
         

     
        distance_wall_x=(game.player.x)
        distance_wall_y=(game.player.y)
        distance_x=np.abs(game.player.x - game.opponent.x)
        distance_y=np.abs(game.player.y - game.opponent.y)
        distance_goal_y=np.abs(game.goal.y - game.player.y)
        distance_goal_x=np.abs(game.goal.x - game.player.x)
        
        move=game.move
        state=[distance_x>game.screen_width/i for i in range(2,30)]+[distance_y>game.screen_height/i for i in range(2,30)]+[distance_goal_x>game.screen_width/i for i in range(2,30)]+[distance_goal_y>game.screen_height/i for i in range(2,30)]+[distance_wall_y>game.screen_height/i for i in range(2,30)]+[distance_wall_x>game.screen_width/i for i in range(2,30)]+[move[0]==1,move[1]==1,move[2]==1,move[3]==1]+[game.up,game.down,game.right,game.left]+[game.player.x>game.opponent.x,game.player.y>game.goal.y,game.opponent.y>game.screen_height/2]
        return np.array(state,dtype=int)

    def remember(self, state, action, reward, next_state, done):

        # store long term memory ( it will be used for the long term training )

        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):

        # long term training : ( example :  training on n=10000 previous game data  )

        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):

        # short term training : training on each step data ( data = state + action + reward taken )

        self.trainer.train_step(state, action, reward, next_state, done)


    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            # action predicted by model
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            print(torch.tensor(prediction, dtype=torch.float),'-----------------------------pred')
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move




def train():
   
    record = 0
    agent = Agent()
    game = CatchGame()
    ii=0
    while True:
        ii=ii+1
        print(ii,'---------------------')
        # get old state
        state_old = agent.get_state(game)
        print('state is : --- ',state_old)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if score > record:
            record = score
            agent.model.save()

        if done:
            
            # train long memory
            
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record,' -------------------------------------------------')



if __name__ == '__main__':
    train()