import sys

import pygame
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from scripts.utils import load_images, load_image
from scripts.entities import Player
from scripts.data import save_game,load_game,delete_save, query_save
from scripts.utils import Animation, load_images, load_image
from scripts.economy import delete_economy
from game import Game
from subclass.pop_up_panel import PopupPanel
from scripts.path_utils import get_resource_path, get_save_path
import os

class Menu:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Life of Py')
        pygame_icon = pygame.image.load('life_of_py.png')
        pygame.display.set_icon(pygame_icon)
        self.window_surface = pygame.display.set_mode((1024, 768))
        self.background = pygame.Surface((1024, 768),pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.manager = pygame_gui.UIManager((1024, 768), theme_path=get_resource_path("data/gui/themes/theme.json"))
        self.game = Game
        self.is_save_panel = False
        self.load_mode = False
        self.delete_mode = False
        self.button_space = 0


        # ******************** UI **********************#

        self.menu_panel = UIPanel(relative_rect=pygame.Rect( 0, 0, 400, 400),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#menu_panel"))
        self.prompt_query = UITextEntryLine(relative_rect=pygame.Rect(0, 40, 600, 40), manager=self.manager,placeholder_text="Enter a name here", anchors={'centerx': 'centerx'},object_id=ObjectID(class_id="@input", object_id="#new_save_input"),visible=False)
        self.prompt_cancel = UIButton(relative_rect=pygame.Rect(95, 40, 100,40),text='Cancel',manager=self.manager,object_id = ObjectID(class_id='@small_button', object_id='#prompt_cancel_button'),visible=False)
        self.prompt_confirm = UIButton(relative_rect=pygame.Rect(830, 40, 100,40),text='Start',manager=self.manager,object_id = ObjectID(class_id='@small_button', object_id='#prompt_start_button'),visible=False)
        self.male_check = UICheckBox(relative_rect=pygame.Rect(220, 100, 40,40),text='Male',manager=self.manager,object_id = ObjectID(class_id='@check_box', object_id='#check'),visible=False)
        self.female_check = UICheckBox(relative_rect=pygame.Rect(320, 100, 40,40),text='Female',manager=self.manager,object_id = ObjectID(class_id='@check_box', object_id='#check'),visible=False)

        self.new_save_btn = UIButton(relative_rect=pygame.Rect(0,30, 200, 50),text='New Game',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#new_save_button'),container=self.menu_panel)
        self.load_btn = UIButton(relative_rect=pygame.Rect(0,100, 200, 50),text='Load',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#load_button'),container=self.menu_panel)
        self.delete_btn = UIButton(relative_rect=pygame.Rect(0,170, 200, 50),text='Delete',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#load_button'),container=self.menu_panel)
        self.quit_btn = UIButton(relative_rect=pygame.Rect(0,240, 200, 50),text='Quit',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#quit_button'),container=self.menu_panel)

        self.extra_label = UILabel(relative_rect=pygame.Rect(0, 350, -1, -1),text="Life Of Py",manager=self.manager,anchors={'centerx':'centerx'},container=self.menu_panel,object_id=ObjectID(class_id="@menu_text",object_id="#menu_text"))
        self.version_label = UILabel(relative_rect=pygame.Rect(0, 630, -1, -1),text="v1.00",manager=self.manager,anchors={'centerx':'centerx'},object_id=ObjectID(class_id="@menu_text",object_id="#version_text"))
        self.load_panel = UIPanel(relative_rect=pygame.Rect(0,0,450,500),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#load_panel"),visible=False)
        self.back_btn = UIButton(relative_rect=pygame.Rect(0,400,200,50),text="Back",manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#back_button'),container=self.load_panel)
        self.reload_save()

        # ******************** UI **********************#
        self.assets = {
            "menu" : load_image("menu.jpg"),
            "cursor": load_image("cursor/cursor.png"),
            'stone': load_images('tiles/stone'),
            'save': load_image('ui/save.png'),
            'player/male/front_idle': Animation(load_images('entities/player/male/front_idle'), img_dur=12),
            'player/male/back_idle': Animation(load_images('entities/player/male/back_idle'), img_dur=12),
            'player/male/front': Animation(load_images('entities/player/male/front'), img_dur=6),
            'player/male/right': Animation(load_images('entities/player/male/right'), img_dur=6),
            'player/male/back': Animation(load_images('entities/player/male/back'), img_dur=6),
            'player/male/hurt': Animation(load_images('entities/player/male/hurt'), img_dur=6,loop=False),
            'player/male/right_idle': Animation(load_images('entities/player/male/right_idle'), img_dur=12),
            'player/female/front_idle': Animation(load_images('entities/player/female/front_idle'), img_dur=12),
            'player/female/back_idle': Animation(load_images('entities/player/female/back_idle'), img_dur=12),
            'player/female/front': Animation(load_images('entities/player/female/front'), img_dur=6),
            'player/female/right': Animation(load_images('entities/player/female/right'), img_dur=6),
            'player/female/back': Animation(load_images('entities/player/female/back'), img_dur=6),
            'player/female/hurt': Animation(load_images('entities/player/female/hurt'), img_dur=6, loop=False),
            'player/female/right_idle': Animation(load_images('entities/player/female/right_idle'), img_dur=12),

        }

        self.assets_sfx = {
            'click' : pygame.mixer.Sound('data/sfx/click.wav'),
            'hard_click' : pygame.mixer.Sound('data/sfx/hard_click.wav'),
        }

        self.assets_sfx['click'].set_volume(0.8)
        self.assets_sfx['hard_click'].set_volume(0.8)


    def initialize_save(self,save_id):
        self.prompt_query.hide()
        self.prompt_cancel.hide()
        self.prompt_confirm.hide()
        self.male_check.set_state(False)
        self.female_check.set_state(False)
        self.male_check.hide()
        self.female_check.hide()
        self.player = load_game(player=self.player, name=self.save_list[save_id].text)
        pygame.mixer.music.stop()
        Game(player=self.player, menu=self)

    def delete_menu_save(self,save_id):
        try:
            csv_path = os.path.join(get_save_path(), f"{self.save_list[save_id].text.split()[0]}_economy.csv")
            os.remove(csv_path)
        except (WindowsError, FileNotFoundError):
            pass
        delete_economy(name=self.save_list[save_id].text)
        delete_save(name=self.save_list[save_id].text)

    def _get_save_index(self, ui_element):
        try:
            if ui_element in self.save_list:
                return self.save_list.index(ui_element)
            # fallback: compare visible text attributes
            elem_text = getattr(ui_element, 'text', None) or getattr(ui_element, 'get_text', lambda: None)()
            for i, btn in enumerate(self.save_list):
                btn_text = getattr(btn, 'text', None) or getattr(btn, 'get_text', lambda: None)()
                if btn_text == elem_text:
                    return i
        except Exception:
            pass
        return None

    def show_save_buttons(self):
        for item in self.save_list:
            try:
                item.show()
            except Exception:
                # fallback if element doesn't implement show()
                try:
                    item.visible = True
                except Exception:
                    pass

    def hide_save_buttons(self):
        for item in self.save_list:
            try:
                item.hide()
            except Exception:
                try:
                    item.visible = False
                except Exception:
                    pass

    def reload_save(self):
        # remove any existing UI elements returned by previous query_save
        if hasattr(self, 'save_list'):
            for item in list(self.save_list):
                try:
                    item.kill()
                except Exception:
                    try:
                        item.hide()
                    except Exception:
                        pass
        # recreate save buttons
        self.is_save_panel = False
        self.save_list = query_save(self)
        self.hide_save_buttons()



    def run(self):
        pygame.mixer.music.load('data/sfx/menu.mp3')
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play(-1)
        self.player = Player(self, (431, 205), (20, 36))
        self.reload_save()
        is_running = True
        while is_running:
            time_delta = self.clock.tick(60) / 1000.0
            pygame.mouse.set_visible(False)
            self.background.blit(self.assets['menu'],(0,0))
            mpos = self.manager.mouse_position

            if self.is_save_panel:
                self.menu_panel.hide()
                self.new_save_btn.hide()
                self.load_btn.hide()
                self.delete_btn.hide()
                self.quit_btn.hide()
                self.extra_label.hide()
                self.prompt_query.hide()
                self.prompt_cancel.hide()
                self.prompt_confirm.hide()
                self.male_check.set_state(False)
                self.female_check.set_state(False)
                self.male_check.hide()
                self.female_check.hide()
                self.load_panel.show()
                self.back_btn.show()
                self.show_save_buttons()
            else:
                self.menu_panel.show()
                self.new_save_btn.show()
                self.load_btn.show()
                self.delete_btn.show()
                self.quit_btn.show()
                self.extra_label.show()
                self.load_panel.hide()
                self.back_btn.hide()
                self.hide_save_buttons()

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
                        self.prompt_query.show()
                        self.prompt_cancel.show()
                        self.prompt_confirm.show()
                        self.male_check.show()
                        self.female_check.show()

                    if event.ui_element == self.prompt_cancel:
                        self.prompt_query.hide()
                        self.prompt_cancel.hide()
                        self.prompt_confirm.hide()
                        self.male_check.set_state(False)
                        self.female_check.set_state(False)
                        self.male_check.hide()
                        self.female_check.hide()
                    if event.ui_element == self.load_btn:
                        self.is_save_panel = True
                        self.delete_mode = False
                        self.load_mode = True


                    #*********** LOAD **********#
                    if self.load_mode:
                        idx = self._get_save_index(event.ui_element)
                        if idx is not None:
                            self.initialize_save(idx)

                    if event.ui_element == self.delete_btn:
                        self.is_save_panel = True
                        for item in self.save_list:
                            item.visible = True
                        self.load_mode = False
                        self.delete_mode = True

                    #*********** DELETE **********#
                    if self.delete_mode:
                        idx = self._get_save_index(event.ui_element)
                        try:
                            if idx is not None:
                                self.delete_menu_save(idx)

                                btn = self.save_list.pop(idx)
                                try:
                                    btn.kill()
                                except Exception:
                                    try:
                                        btn.hide()
                                    except Exception:
                                        pass
                        except Exception as e:
                            print(e)

                    if event.ui_element == self.back_btn:
                        self.is_save_panel = False
                        self.menu_panel.show()
                        self.new_save_btn.show()
                        self.load_btn.show()
                        self.delete_btn.show()
                        self.quit_btn.show()
                        self.extra_label.show()
                        self.load_panel.hide()
                        self.back_btn.hide()
                        for item in self.save_list:
                            item.visible= False

                    if event.ui_element == self.prompt_confirm:
                        if len(self.prompt_query.text) > 4:
                            if self.male_check.is_checked or self.female_check.is_checked:
                                if save_game(player=self.player,name=self.prompt_query.text,menu=self):
                                    self.player = load_game(player=self.player, name=self.prompt_query.text)
                                    self.prompt_query.clear()
                                    self.prompt_query.hide()
                                    self.prompt_cancel.hide()
                                    self.prompt_confirm.hide()
                                    self.male_check.set_state(False)
                                    self.female_check.set_state(False)
                                    self.male_check.hide()
                                    self.female_check.hide()
                                    pygame.mixer.music.stop()
                                    Game(menu=self,player=self.player)
                                    is_running = False
                            else:
                                PopupPanel.show_message(manager=self.manager, text="Confirm the gender of your character!",
                                                        screen_size=self.window_surface.get_size(), positive=False)

                        else:
                            PopupPanel.show_message(manager=self.manager, text="Enter a save name!",
                                                    screen_size=self.window_surface.get_size(),positive=False)

                    #*********** SAVE **********#


                if event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
                    self.assets_sfx['hard_click'].play()
                    if event.ui_element == self.male_check:
                        self.female_check.set_state(False)
                        self.player.gender = 0

                    elif event.ui_element == self.female_check:
                        self.male_check.set_state(False)
                        self.player.gender = 1



                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.window_surface.blit(self.background, (0, 0))
            self.manager.draw_ui(self.window_surface)
            self.window_surface.blit(self.assets['cursor'],mpos)

            pygame.display.update()

menu =Menu()
menu.run()

