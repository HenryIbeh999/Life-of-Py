import sys

import pygame
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from scripts.utils import load_images, load_image
from scripts.entities import Player
from scripts.data import save_game,load_game,delete_save, query_save
from scripts.utils import Animation, load_images, load_image
from game import Game
from subclass.pop_up_panel import PopupPanel


class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Life of Py')
        self.window_surface = pygame.display.set_mode((1024, 768))

        self.background = pygame.Surface((1024, 768),pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1024, 768), theme_path="data/gui/themes/theme.json")
        self.game = Game
        self.is_save_panel = False
        self.load_mode = False
        self.delete_mode = False
        self.button_space = 0

        # ******************** UI **********************#

        self.menu_panel = UIPanel(relative_rect=pygame.Rect( 0, 0, 400, 400),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#menu_panel"))
        self.prompt_query = UITextEntryLine(relative_rect=pygame.Rect(0, 40, 600, 40), manager=self.manager,placeholder_text="Enter a name here", anchors={'centerx': 'centerx'},object_id=ObjectID(class_id="@input", object_id="#new_save_input"),visible=False)
        self.prompt_cancel = UIButton(relative_rect=pygame.Rect(830, 40, 100,40),text='Cancel',manager=self.manager,object_id = ObjectID(class_id='@small_button', object_id='#prompt_cancel_button'),visible=False)
        self.new_save_btn = UIButton(relative_rect=pygame.Rect(0,30, 200, 50),text='New Game',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#new_save_button'),container=self.menu_panel)
        self.load_btn = UIButton(relative_rect=pygame.Rect(0,100, 200, 50),text='Load',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#load_button'),container=self.menu_panel)
        self.delete_btn = UIButton(relative_rect=pygame.Rect(0,170, 200, 50),text='Delete',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#load_button'),container=self.menu_panel)
        self.quit_btn = UIButton(relative_rect=pygame.Rect(0,240, 200, 50),text='Quit',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#quit_button'),container=self.menu_panel)

        self.extra_label = UILabel(relative_rect=pygame.Rect(0, 350, -1, -1),text="Life Of Py",manager=self.manager,anchors={'centerx':'centerx'},container=self.menu_panel,object_id=ObjectID(class_id="@menu_text",object_id="#menu_text"))
        self.version_label = UILabel(relative_rect=pygame.Rect(0, 650, -1, -1),text="v1.00",manager=self.manager,anchors={'centerx':'centerx'},object_id=ObjectID(class_id="@menu_text",object_id="#version_text"))
        self.load_panel = UIPanel(relative_rect=pygame.Rect(0,0,450,500),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#load_panel"),visible=False)
        self.back_btn = UIButton(relative_rect=pygame.Rect(0,400,200,50),text="Back",manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#back_button'),container=self.load_panel)
        self.reload_save()

        # ******************** UI **********************#
        self.assets = {
            "menu" : load_image("menu.jpg"),
            "cursor": load_image("cursor/cursor.png"),
            'stone': load_images('tiles/stone'),
            'save': load_image('ui/save.png'),
            'player/front_idle': Animation(load_images('entities/player/front_idle'), img_dur=12),
            'player/back_idle': Animation(load_images('entities/player/back_idle'), img_dur=12),
            'player/front': Animation(load_images('entities/player/front'), img_dur=6),
            'player/left': Animation(load_images('entities/player/left'), img_dur=6),
            'player/back': Animation(load_images('entities/player/back'), img_dur=6),
            'player/hurt': Animation(load_images('entities/player/hurt'), img_dur=6,loop=False),
        }

        self.assets_sfx = {
            'ambience' : pygame.mixer.Sound('data/sfx/ambience.wav'),
            'click' : pygame.mixer.Sound('data/sfx/click.wav'),
        }

        self.assets_sfx['ambience'].set_volume(0.5)
        self.assets_sfx['click'].set_volume(0.8)


    def initialize_save(self,save_id):
        self.prompt_query.visible = False
        self.prompt_cancel.visible = False
        self.player = load_game(player=self.player, name=self.save_list[save_id].text)
        pygame.mixer.music.stop()
        Game(player=self.player, menu=self)

    def delete_menu_save(self,save_id):
        delete_save(name=self.save_list[save_id].text)

    def reload_save(self):
        self.is_save_panel = False
        self.save_list = query_save(self)
        try:
            for i in range(3):
                self.save_list[i].set_text(query_save(self)[i].text)
        except IndexError:
            pass



    def run(self):
        pygame.mixer.music.load('data/sfx/menu.mp3')
        pygame.mixer.music.set_volume(0)
        pygame.mixer.music.play(-1)
        self.player = Player(self, (431, 205), (20, 36))
        self.reload_save()
        is_running = True
        while is_running:
            pygame.mouse.set_visible(False)
            self.background.blit(self.assets['menu'],(0,0))
            mpos = self.manager.mouse_position

            if self.is_save_panel:
                self.menu_panel.visible = False
                self.new_save_btn.visible = False
                self.load_btn.visible = False
                self.delete_btn.visible = False
                self.quit_btn.visible = False
                self.extra_label.visible = False
                self.load_panel.visible = True
                self.back_btn.visible = True
                for item in self.save_list:
                    item.visible = True
            else:
                self.menu_panel.visible = True
                self.new_save_btn.visible = True
                self.load_btn.visible = True
                self.delete_btn.visible = True
                self.quit_btn.visible = True
                self.extra_label.visible = True
                self.load_panel.visible = False
                self.back_btn.visible = False
                for item in self.save_list:
                    item.visible = False


            time_delta = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                    sys.exit()

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.assets_sfx['click'].play()
                    if event.ui_element == self.quit_btn:
                        is_running = False
                        sys.exit()
                    if event.ui_element == self.new_save_btn:
                        self.prompt_query.visible = True
                        self.prompt_cancel.visible = True

                    if event.ui_element == self.prompt_cancel:
                        self.prompt_query.visible = False
                        self.prompt_cancel.visible = False
                    if event.ui_element == self.load_btn:
                        self.is_save_panel = True
                        self.delete_mode = False
                        self.load_mode = True


                    #*********** LOAD **********#

                    if self.load_mode is True:

                        try:
                            if event.ui_element == self.save_list[0]:
                                self.initialize_save(0)

                            elif event.ui_element == self.save_list[1]:
                                self.initialize_save(1)

                            elif event.ui_element == self.save_list[2]:
                                self.initialize_save(2)

                        except IndexError:
                            pass

                    if event.ui_element == self.delete_btn:
                        self.is_save_panel = True
                        for item in self.save_list:
                            item.visible = True
                        self.load_mode = False
                        self.delete_mode = True

                    #*********** DELETE **********#

                    if self.delete_mode is True:
                        try:
                            if event.ui_element == self.save_list[0]:
                                self.save_list[0].visible = False
                                self.delete_menu_save(0)
                                self.save_list.remove(self.save_list[0])


                            elif event.ui_element == self.save_list[1]:
                                self.save_list[1].visible = False
                                self.delete_menu_save(1)
                                self.save_list.remove(self.save_list[1])



                            elif event.ui_element == self.save_list[2]:
                                self.save_list[2].visible = False
                                self.delete_menu_save(2)
                                self.save_list.remove(self.save_list[2])

                        except IndexError:
                            pass



                    if event.ui_element == self.back_btn:
                        self.is_save_panel = False
                        self.menu_panel.visible = True
                        self.new_save_btn.visible = True
                        self.load_btn.visible = True
                        self.delete_btn.visible = True
                        self.quit_btn.visible = True
                        self.extra_label.visible = True
                        self.load_panel.visible = False
                        self.back_btn.visible = False
                        for item in self.save_list:
                            item.visible = False

                    #*********** SAVE **********#

                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if event.ui_element == self.prompt_query:
                        if event.text != "":
                            self.prompt_query.clear()
                            self.prompt_query.visible = False
                            self.prompt_cancel.visible = False
                            save_game(player=self.player,name=event.text,menu=self)
                            self.player = load_game(player=self.player, name=event.text)
                            pygame.mixer.music.stop()
                            Game(menu=self,player=self.player)

                            is_running = False
                        else:
                            PopupPanel.show_message(manager=self.manager, text="Enter a save name!",
                                                    screen_size=self.window_surface.get_size())

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            self.window_surface.blit(self.assets['cursor'],mpos)

            pygame.display.update()

menu =Menu()
menu.run()

