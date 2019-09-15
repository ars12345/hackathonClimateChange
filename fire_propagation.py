# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 11:47:59 2019

@author: Portable
"""

import pygame
import numpy as np
import random
import imageio

fire_started = False
white = (255,255,255)
black = pygame.Color('black')
red = pygame.Color('red')
mask = ((imageio.imread('./mask360.jpg')[:,:,0])/255)>0.9 # mask to define where the river is

#wind_filter = np.array([[0.3,0.8,0.3],[0.15,0,0.15],[0.05,0.1,0.05]])
#wind_filter = np.array([[0.25,0.5,0.25],[0.5,0,0.5],[0.25,0.5,0.25]]) 
wind_filter = np.array([[0.3,1.0,0.3],[0.15,0,0.15],[0.1,0.1,0.1]])

def prob_fire(surronding, wind_filter,mask_value):
    prob = int(mask_value)*np.sum((surronding==1)*wind_filter)/2
    return int(prob>random.random() and mask_value)

def pixel(surface, color, pos): 
    s = pygame.Surface((3,3))
    s.set_alpha(140) 
    s.fill(color)
    surface.blit(s, (pos[0]-1,pos[1]-1)) 
    
pygame.init()  
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#screen = pygame.display.set_mode((1080, 1080))
forest_state  = np.zeros((360,360))
screen.fill((white))
img = pygame.image.load('./landscape.jpg')
img = pygame.transform.scale(img, (1080, 1080))
screen.blit(img,(0,0))

pygame.display.flip()
running = 1
while running:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False        
            if event.key == pygame.K_SPACE:   
                wind_filter = wind_filter.transpose()
                print('Rotation de 90° du vent')
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            print(pos)
            forest_state[int(pos[0]/3)][int(pos[1]/3)] = 1
            pixel(screen, black, pos)
            fire_started = True

    if fire_started:
        new_forest_state = np.copy(forest_state)
        for i in range(1,len(forest_state)-1):
            for j in range(1,len(forest_state[0])-1):
                if forest_state[i,j]!=1:
                    new_forest_state[i,j] = min(1,prob_fire(forest_state[i-1:i+2,j-1:j+2],wind_filter,mask[i,j]))
                    if new_forest_state[i,j]==1:
                        pixel(screen,red,(i*3,j*3))          
        forest_state = new_forest_state

pygame.display.quit()
pygame.quit()    
    