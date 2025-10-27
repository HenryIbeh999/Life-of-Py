import math
import random
import pygame
import pygame_gui

from scripts.tilemap import TileMap
from subclass.pop_up_panel import PopupPanel


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size): # Initializes the entity class
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # checks collisions of all four sides of entity

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')



    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1]) # returns a rectangle rendered on the entity that collides with the rectangle rendered on the tiles

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f"{self.type}/{self.action}"].copy()

    def update(self,tile_map, movement=(0, 0)):
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} # resets the collision values after a frame
        frame_movement = (movement[0] ,movement[1] ) # handles entity movement

        self.pos[0] += frame_movement[0] # frame movement is added to the position of entity's X co-ordinate
        entity_rect = self.rect()
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect): #checks if entity's rectangle collided with the rectangle rendered in the tile_map.py passed as an argument in this update method
                if frame_movement[0]> 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0]< 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tile_map.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1]> 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1]< 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True






        self.animation.update()


    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),(self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))




class Player(PhysicsEntity):
    def __init__(self, game, pos , size):
        super().__init__(game,'player', pos, size)
        self.name = ""
        self.money = 0.0
        self.happiness = 100.0
        self.energy = 100.0
        self.hunger = 100.0
        self.job = None
        self.deposit = 0.0
        self.day = 1

    def update(self,tile_map, movement=(0, 0)):
        super().update(tile_map,movement=movement)
        if movement[0] > 0:
            self.flip = True
            self.set_action('left')
        elif movement[0] < 0:
            self.flip = False
            self.set_action('left')
        elif movement[1] > 0:
            self.set_action('front')
        elif movement[1] <0:
            self.set_action('back')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0,0)):
        super().render(surf,offset=offset)


    def work(self,game):
        if self.energy < self.job.energy_cost:
            PopupPanel.show_message(
                manager=game.manager,
                text="You are tired, get some sleep!",
                screen_size=game.screen.get_size()
            )
        elif self.hunger <= 0:
            PopupPanel.show_message(
                manager=game.manager,
                text="You look really hungry, bro!",
                screen_size=game.screen.get_size()
            )


        else:
            self.money += self.job.salary
            self.energy -= self.job.energy_cost
            self.energy = max(self.energy,0)
            self.hunger -= 25
            self.hunger = max(self.hunger,0)
            self.happiness -= self.job.happiness_cost
            self.happiness = max(self.happiness,0)

    def deposit_money(self,amount,game):
        if self.money >= amount:
            self.money -= amount
            self.deposit += amount
            PopupPanel.show_message(
                manager=game.manager,
                text=f"Successfully deposited ${amount} to your account!",
                screen_size=game.screen.get_size()
            )
        else:
            PopupPanel.show_message(
                manager=game.manager,
                text="Insufficient funds!",
                screen_size=game.screen.get_size()
            )

    def withdraw_money(self,amount,game):
        if amount <= self.deposit:
            self.money += amount
            self.deposit -= amount
            PopupPanel.show_message(
                manager=game.manager,
                text=f"Withdrawal of ${amount} successful!",
                screen_size=game.screen.get_size()
            )
        else:
            self.money += self.deposit
            self.deposit = 0
            PopupPanel.show_message(
                manager=game.manager,
                text=f"Withdrawal of ${self.deposit} successful!",
                screen_size=game.screen.get_size()
            )


class Item:
    def __init__(self, game, e_type, pos, size,item_name): # Initializes the entity class
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.item_name = item_name
        self.size = size

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action(f"{self.item_name}")


    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f"{self.type}/{self.action}"].copy()

    def update(self,tile_map, movement=(0, 0)):
        self.animation.update()

    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False),(self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))



class Coin(Item):
    def __init__(self,game,pos,size):
        super().__init__(game, 'item', pos, size,item_name='coin')

    def update(self,tile_map, movement=(0, 0)):
        super().update(tile_map,movement=movement)

        self.set_action('coin')







