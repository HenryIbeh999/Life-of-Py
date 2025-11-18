from scripts.entities import *
from scripts.utils import Animation, load_images, load_image
from scripts.tilemap import TileMap
import pygame
import sys
import pygame_gui
from pygame_gui.elements import *
from pygame_gui.core import ObjectID
from scripts.data import save_game, load_game, query_save, overwrite_save
from scripts.jobs import load_jobs
from scripts.actions import *
from subclass.ui_panel import AnimatedPanel
from subclass.pop_up_panel import PopupPanel
from subclass.ui_label import MoneyAnimator
from subclass.ui_progress_bar import SmoothProgressBar
from scripts.economy import *

class Game:
    def __init__(self,menu,player):
        pygame.init()
        # Screen setup
        pygame.display.set_caption("Life of Py")
        self.screen = pygame.display.set_mode((1024, 768))
        self.display = pygame.Surface((512, 384), pygame.SRCALPHA)  # Internal display for scaling
        self.display_2 = pygame.Surface((512, 384)).convert()  # Secondary display
        self.clock = pygame.time.Clock()
        self.movement = [False,False,False,False] #Movement flags for left , right, top, bottom
        self.manager = pygame_gui.UIManager((1024, 768), theme_path="data/gui/themes/theme.json")
        self.player = player
        self.menu = menu
        self.old_name = self.player.name
        self.saved_name = self.player.name
        self.economy = load_economy(self)
        self.player.energy = 0


        #-----------------------------Indicators ----------------------------- #
        self.location = ""
        self.is_paused = False
        self.is_action_panel = False
        self.is_change_name_panel = False
        self.is_rate_panel = False
        self.is_home = True
        self.clickable = False
        self.in_drug_store = False
        self.in_burgershop = False
        self.in_office = False
        self.in_bank = False
        self.deposit_mode = False
        self.withdraw_mode = False
        self.mute = False
        self.is_night = False
        #-----------------------------Indicators ----------------------------- #

        if self.is_home:
            self.location = "home"


        self.assets = {
            'npc/1/idle': Animation(load_images('entities/npc/npc-1/idle'), img_dur=12),
            'npc/2/idle': Animation(load_images('entities/npc/npc-2/idle'), img_dur=12),
            'npc/3/idle': Animation(load_images('entities/npc/npc-3/idle'), img_dur=12),
            'npc/4/idle': Animation(load_images('entities/npc/npc-4/idle'), img_dur=12),
            'npc/5/idle': Animation(load_images('entities/npc/npc-5/idle'), img_dur=24),
            'npc/6/idle': Animation(load_images('entities/npc/npc-6/idle'), img_dur=12),
            'npc/7/idle': Animation(load_images('entities/npc/npc-7/idle'), img_dur=12),
            'npc/8/idle': Animation(load_images('entities/npc/npc-8/idle'), img_dur=12),
            'npc/9/idle': Animation(load_images('entities/npc/npc-9/idle'), img_dur=12),
            'npc/10/idle': Animation(load_images('entities/npc/npc-10/idle'), img_dur=12),
            'stone': load_images('tiles/stone'),
            'location' : load_image(f'{self.location}.png'),
            'item/coin' : Animation(load_images('coins')),
            'job' : load_image('ui/job.png'),
            'energy' : load_image('ui/energy.png'),
            'health' : load_image('ui/health.png'),
            'hunger' : load_image('ui/hunger.png'),
            'x_button' : load_image('ui/x_button.png'),
            "cursor": load_image("cursor/cursor.png"),
            "ui_character": load_image(f"ui/ui_character.png"),
            "level": load_image(f"ui/level.png"),
            "metrics": load_image(f"ui/metrics.png"),

        }

        self.assets_sfx = {
            'ambience' : pygame.mixer.Sound('data/sfx/ambience.wav'),
            'click' : pygame.mixer.Sound('data/sfx/click.wav'),
            'game_over' : pygame.mixer.Sound('data/sfx/game_over.wav'),
            'walk' : pygame.mixer.Sound('data/sfx/walk.wav'),
            'coins' : pygame.mixer.Sound('data/sfx/coins.mp3'),
            'pause' : pygame.mixer.Sound('data/sfx/pause.mp3'),
        }

        self.assets_sfx['ambience'].set_volume(0.2)
        self.assets_sfx['click'].set_volume(1.0)


#******************** UI **********************#

        self.status_panel = UIPanel(relative_rect=pygame.Rect(0,0, 300, 350),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#status_panel"))
        self.name_status_panel = UIPanel(relative_rect=pygame.Rect(0,0, 300, 50),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#player_status_panel"))
        self.player_name_label = UILabel(relative_rect=pygame.Rect(50,10,-1,-1),text=f"{self.player.name}",manager=self.manager,container=self.name_status_panel, object_id=ObjectID(class_id="@text",object_id="#name_text"))
        self.player_level_label = UILabel(relative_rect=pygame.Rect(200,10,-1,-1),text=f"LVL {self.player.level}",manager=self.manager,container=self.name_status_panel, object_id=ObjectID(class_id="@text",object_id="#lvl_text"))
        self.character_image = UIImage(relative_rect=pygame.Rect(10,5,30,30),image_surface=self.assets['ui_character'],manager=self.manager,container=self.name_status_panel)
        self.job_image = UIImage(relative_rect=pygame.Rect(20,60,24,24),image_surface=self.assets['job'],manager=self.manager,container=self.status_panel)
        self.player_job_label = UILabel(relative_rect=pygame.Rect(48,60,-1,-1),text=f"{self.player.job}",manager=self.manager,container=self.status_panel, object_id=ObjectID(class_id="@text",object_id="#job_text"))
        self.money_image = Coin(self,(165,70),(16,16))
        self.player_money_label = UILabel(relative_rect=pygame.Rect(180,60,-1,-1),text=f"${self.player.money}",manager=self.manager,container=self.status_panel, object_id=ObjectID(class_id="@text",object_id="#money_text"))
        self.money_animator = MoneyAnimator(self.player_money_label)
        self.money_animator.current_value = round((float(self.player.money)),2)

        self.energy_image = UIImage(relative_rect=pygame.Rect(20,100,28,28),image_surface=self.assets['energy'],manager=self.manager,container=self.status_panel)
        self.energy_bar = UIProgressBar(relative_rect=pygame.Rect(0,100,190,35),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#hunger_bar"),anchors={"centerx":"centerx"})
        self.smooth_energy_bar = SmoothProgressBar(self.energy_bar)

        self.hunger_image = UIImage(relative_rect=pygame.Rect(20,140,28,28),image_surface=self.assets['hunger'],manager=self.manager,container=self.status_panel)
        self.hunger_bar = UIProgressBar(relative_rect=pygame.Rect(0,140,190,35),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#hunger_bar"),anchors={"centerx":"centerx"})
        self.smooth_hunger_bar = SmoothProgressBar(self.hunger_bar)

        self.health_image = UIImage(relative_rect=pygame.Rect(20,180,28,28),image_surface=self.assets['health'],manager=self.manager,container=self.status_panel)
        self.health_bar = UIProgressBar(relative_rect=pygame.Rect(0,180,190,35),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#health_bar"),anchors={"centerx":"centerx"})
        self.smooth_health_bar = SmoothProgressBar(self.health_bar)

        self.lvl_image = UIImage(relative_rect=pygame.Rect(20,220,28,28),image_surface=pygame.image.load('data/images/ui/level.png'),manager=self.manager,container=self.status_panel)
        self.lvl_bar = UIProgressBar(relative_rect=pygame.Rect(0,220,190,35),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#lvl_bar"),anchors={"centerx":"centerx"})
        self.smooth_lvl_bar = SmoothProgressBar(self.lvl_bar)


        self.rate_btn = UIButton(relative_rect=pygame.Rect(0,300,62,30),text="",manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@misc_button",object_id="#rate_button"),anchors={"centerx":"centerx"})


        #******************* MISC ****************************#
        self.misc_status_panel = UIPanel(relative_rect=pygame.Rect(50,0,500,80),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#misc_status_panel"),anchors={"centerx":"centerx"})
        self.pause_btn = UIButton(relative_rect=pygame.Rect(20,0,30,30),text="",manager=self.manager,container=self.misc_status_panel,object_id=ObjectID(class_id="@misc_button",object_id="#pause_button"),anchors={"centery":"centery"})
        self.sound_btn = UIButton(relative_rect=pygame.Rect(70,0,30,30),text="",manager=self.manager,container=self.misc_status_panel,object_id=ObjectID(class_id="@misc_button",object_id="#sound_button"),anchors={"centery":"centery"})
        self.day_label = UILabel(relative_rect=pygame.Rect(0, 0, -1, -1), text=f"Day {player.day}", manager=self.manager, container=self.misc_status_panel, object_id=ObjectID(class_id="@text", object_id="#day_text"), anchors={"center": "center"})
        self.save_btn = UIButton(relative_rect=pygame.Rect(400,0,62,30),text="",manager=self.manager,container=self.misc_status_panel,object_id=ObjectID(class_id="@misc_button",object_id="#save_button"),anchors={"centery":"centery"})
        #******************* MISC ****************************#

        #******************* PAUSED ****************************#
        self.pause_panel = AnimatedPanel(relative_rect=pygame.Rect(0,0,400,400),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#pause_panel"),visible=False)
        self.pause_load_btn = UIButton(relative_rect=pygame.Rect(0,40,200,50),text='Load Game',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#pause_load_button'),container=self.pause_panel)
        self.pause_menu_btn = UIButton(relative_rect=pygame.Rect(0,120,200,50),text='Back To Menu',manager=self.manager,anchors={'centerx':'centerx'},object_id = ObjectID(class_id='@small_button', object_id='#pause_menu_button'),container=self.pause_panel)
        self.credit_head_label = UILabel(relative_rect=pygame.Rect(0, 240, -1, -1), text="Credit:", manager=self.manager, container=self.pause_panel, object_id=ObjectID(class_id="@text", object_id="#credit_head"), anchors={"centerx": "centerx"})
        self.credit_sub_1_label = UILabel(relative_rect=pygame.Rect(0, 270, -1, -1), text="This was made by Henry,", manager=self.manager, container=self.pause_panel, object_id=ObjectID(class_id="@text", object_id="#credit_sub1"), anchors={"centerx": "centerx"})
        self.credit_sub_2_label = UILabel(relative_rect=pygame.Rect(0, 290, -1, -1), text="using pygame and whatnot's", manager=self.manager, container=self.pause_panel, object_id=ObjectID(class_id="@text", object_id="#credit_sub2"), anchors={"centerx": "centerx"})
        self.credit_sub_3_label = UILabel(relative_rect=pygame.Rect(0, 310, -1, -1), text="while he was bored at home.", manager=self.manager, container=self.pause_panel, object_id=ObjectID(class_id="@text", object_id="#credit_sub2"), anchors={"centerx": "centerx"})
        #******************* PAUSED ****************************#

        #*******************ACTIONS SECTION********************#
        self.action_panel = AnimatedPanel(relative_rect=(0, 0, 400, 400), anchors={"center": "center"}, manager=self.manager, object_id=ObjectID(class_id="@panel", object_id="#action_panel"), visible=False)
        self.small_action_panel = AnimatedPanel(relative_rect=(0,0, 400, 70),anchors={"center": "center"},manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#small_action_panel"),visible=False)
        self.ui_action_image = UIImage(relative_rect=(0,0,50,50),image_surface=load_image("ui/ui_doctor.png"),manager=self.manager,container=self.small_action_panel,anchors={"center": "center"})
        self.primary_job_button = UIButton(relative_rect=(-120,70,50,50), text="", manager=self.manager, anchors={"centerx":"centerx"}, container=self.action_panel, object_id = ObjectID(class_id='@ui_button', object_id='#primary_job_button'))
        self.primary_job_label = UILabel(relative_rect=(110,80,-1,-1), text="", manager=self.manager, container=self.action_panel, object_id = ObjectID(class_id='@action_text', object_id='#primary_job_text'))
        self.secondary_job_button = UIButton(relative_rect=(-120, 140, 50, 50), text="", manager=self.manager,anchors={"centerx": "centerx"}, container=self.action_panel,object_id=ObjectID(class_id='@ui_button', object_id='#secondary_job_button'))
        self.secondary_job_label = UILabel(relative_rect=(110, 150, -1, -1), text="", manager=self.manager, container=self.action_panel,object_id=ObjectID(class_id='@action_text', object_id='#secondary_job_text'))

        self.primary_action_button =  UIButton(relative_rect=(-120,210,50,50), text="", manager=self.manager, anchors={"centerx":"centerx"}, container=self.action_panel, object_id = ObjectID(class_id='@ui_button', object_id='#None_action_button'))
        self.primary_action_label = UILabel(relative_rect=(110,220,-1,-1), text="", manager=self.manager,container=self.action_panel, object_id = ObjectID(class_id='@action_text', object_id='#primary_action_text'))
        self.secondary_action_button =  UIButton(relative_rect=(-120,280,50,50), text="", manager=self.manager, anchors={"centerx":"centerx"}, container=self.action_panel, object_id = ObjectID(class_id='@ui_button', object_id='#None_action_button'))
        self.secondary_action_label = UILabel(relative_rect=(110,290,-1,-1), text="", manager=self.manager,container=self.action_panel, object_id = ObjectID(class_id='@action_text', object_id='#secondary_action_text'))

        self.change_name_panel = AnimatedPanel(relative_rect=(0, 0, 300, 200), anchors={"centery": "centery"}, manager=self.manager, object_id=ObjectID(class_id="@panel", object_id="#change_name_panel"), visible=False)
        self.change_name_cancel_btn = UIButton(relative_rect=pygame.Rect(5,10,30,30),text="",manager=self.manager,container=self.change_name_panel,object_id=ObjectID(class_id="@misc_button",object_id="#cancel_button"))
        self.change_name_prompt = UITextEntryLine(relative_rect=pygame.Rect(0, 50, 200, 40), manager=self.manager,container=self.change_name_panel,placeholder_text="Enter a new name", anchors={'centerx': 'centerx'},object_id=ObjectID(class_id="@input", object_id="#new_name_input"),visible=False)
        self.change_name_continue_btn = UIButton(relative_rect=pygame.Rect(0,120,94,30),text="",manager=self.manager, anchors={"centerx": "centerx"},container=self.change_name_panel,object_id=ObjectID(class_id="@misc_button",object_id="#continue_button"))


        self.bank_panel = AnimatedPanel(relative_rect=(0, 50, 300, 200), anchors={"centery": "centery"}, manager=self.manager, object_id=ObjectID(class_id="@panel", object_id="#bank_panel"),visible=False)
        self.bank_cancel_btn = UIButton(relative_rect=pygame.Rect(5,10,30,30),text="",manager=self.manager,container=self.bank_panel,object_id=ObjectID(class_id="@misc_button",object_id="#cancel_button"))
        self.bank_type_label = UILabel(relative_rect=(0,10,-1,-1), text="",anchors={"centerx": "centerx"} ,manager=self.manager,container=self.bank_panel, object_id = ObjectID(class_id='@action_text', object_id='#bank_type_label'))
        self.min_type_label = UILabel(relative_rect=(10,-25,-1,-1), text=f"${1.00}",anchors={"centery": "centery"} , manager=self.manager,container=self.bank_panel, object_id = ObjectID(class_id='@action_text', object_id='#min_type_label'))
        self.max_type_label = UILabel(relative_rect=(215,-25,-1,-1), text="",anchors={"centery": "centery"} , manager=self.manager,container=self.bank_panel, object_id = ObjectID(class_id='@action_text', object_id='#max_type_label'))
        self.bank_prompt = UITextEntryLine(relative_rect=pygame.Rect(-15, 50, 150, 50), manager=self.manager,container=self.bank_panel,placeholder_text="", anchors={'centerx': 'centerx'},object_id=ObjectID(class_id="@input", object_id="#new_name_input"))
        self.bank_continue_btn = UIButton(relative_rect=pygame.Rect(0,120,94,30),text="",manager=self.manager, anchors={"centerx": "centerx"},container=self.bank_panel,object_id=ObjectID(class_id="@misc_button",object_id="#continue_button"))
        #*******************ACTIONS SECTION********************#

        self.chart_panel = AnimatedPanel(relative_rect=pygame.Rect(0,0,600,600),manager=self.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#chart_panel"),visible=False)
        self.chart_image = UIImage(relative_rect=pygame.Rect(0,0,550,500),manager=self.manager,image_surface=None,anchors={'center': 'center'},container=self.chart_panel)
        self.chart_icon = UIImage(relative_rect=pygame.Rect(0,0,50,50),manager=self.manager,image_surface=self.assets['metrics'],anchors={'centerx': 'centerx'},container=self.chart_panel)
        self.chart_cancel_btn = UIButton(relative_rect=pygame.Rect(20,10,30,30),text="",manager=self.manager,container=self.chart_panel,object_id=ObjectID(class_id="@misc_button",object_id="#cancel_button"))


#******************** UI **********************#

        self.tile_map =TileMap(self,tile_size=16)
        self.load_map(self.location)
        self.run()


    def load_map(self, map_id):
        self.tile_map.load(f'data/maps/{map_id}.json')
        self.npcs = []
        for spawner in self.tile_map.extract([('spawners', 0),('spawners', 1),('spawners', 2),('spawners', 3),('spawners', 4),
                                              ('spawners', 5),('spawners', 6),('spawners', 7),('spawners', 8),('spawners', 9),
                                              ('spawners', 10)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
            else:
                self.npcs.append(Npc(self, spawner['pos'], (20, 36),variant=spawner['variant']))


        self.scroll = [0,0]



    def run(self):
        self.assets_sfx['ambience'].play(-1)
        circle_transition(self)
        if self.player.day ==1:
            save_economy(self)
            self.economy = load_economy(self)
        update_csv(self)

        if self.player.gender == 0:
            self.player.set_action('male/front_idle')
        else:
            self.player.set_action('female/front_idle')
        running = True
        while running:
            dt = self.clock.tick(60) / 1000.0
            check_time(self)
            self.display.fill((0, 0, 0, 0))
            if self.is_night:
                self.display_2.fill((45, 38, 43))
            else:
                self.display_2.fill((159, 226, 255))

            mpos = self.manager.mouse_position

            # scroll mechanics
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1])) # changes the scroll values to integers to improve accuracy
            bg_x = -int(render_scroll[0])  # 0.5 for slower parallax, use 1 for 1:1 scroll
            bg_y = -int(render_scroll[1])

            # HUD mechanics
            player_x,player_y = self.player.rect().center
            player_x -= render_scroll[0]
            player_y -= render_scroll[1]

            # Scale to screen coordinates
            screen_x = int(player_x * self.screen.get_width() / self.display.get_width())
            screen_y = int(player_y * self.screen.get_height() / self.display.get_height())

            def interact():
                if self.is_action_panel is False and self.is_paused is False and not self.pause_panel.visible and not self.player.is_dead and not self.is_rate_panel:
                    self.clickable = True
                    self.screen.blit(self.assets["x_button"], (screen_x - 20, screen_y - 80))
                else:
                    pass

            if self.location in ('home','suburb','town'):
                if self.pause_panel.visible or self.action_panel.visible or self.chart_panel.visible:
                    self.display_2.blit(pygame.transform.gaussian_blur( self.assets['location'],radius=1),(bg_x, bg_y))
                else:
                    self.money_image.update(self.tile_map)
                    self.display_2.blit(self.assets['location'], (bg_x , bg_y ))


            self.tile_map.render(self.display, offset=render_scroll)




            if not self.pause_panel.visible and not self.action_panel.visible and not self.change_name_panel.visible and not self.bank_panel.visible and not self.chart_panel.visible:
                for npc in self.npcs.copy():
                    npc.update(self.tile_map,(0,0))
                    npc.render(self.display, offset=render_scroll)

                if not self.player.is_dead:
                    self.player.update(self.tile_map, (self.movement[1] - self.movement[0], self.movement[3]- self.movement[2]))
                else:
                    self.player.update(self.tile_map,(0,0))
                self.player.render(self.display, offset=render_scroll)


            try:
                self.player_job_label.set_text(f"{self.player.job.name}")
            except AttributeError:
                self.player_job_label.set_text(f"{self.player.job}")
            self.player_name_label.set_text(f"{self.player.name}")
            self.player_level_label.set_text(f"LVL {self.player.level}")
            if self.money_animator.current_value != self.player.money:
                self.assets_sfx['coins'].play(0)
            self.money_animator.set_target(self.player.money)

            self.day_label.set_text(f"Day {self.player.day}")

            self.smooth_energy_bar.set_value(float(self.player.energy))
            if self.player.energy <= 30.0:
                self.energy_bar.change_object_id("@low_progress_bar")
            else:
                self.energy_bar.change_object_id("@high_progress_bar")

            self.smooth_health_bar.set_value(float(self.player.health))
            if self.player.health <= 30.0:
                self.health_bar.change_object_id("@low_progress_bar")
            else:
                self.health_bar.change_object_id("@high_progress_bar")
            self.smooth_hunger_bar.set_value(float(self.player.hunger))
            if self.player.hunger <= 30.0:
                self.hunger_bar.change_object_id("@low_progress_bar")
            else:
                self.hunger_bar.change_object_id("@high_progress_bar")

            self.smooth_lvl_bar.set_value(float(self.player.level_progress))
            if self.player.level_progress >= 100.0:
                if self.player.level < 15:
                    self.player.level_progress = 0.0
                    self.player.level += 1
                    PopupPanel.show_message(manager=self.manager,
                                            text=f"You have leveled up to LVL {self.player.level}!!.",
                                            screen_size=self.screen.get_size(),is_lvl_up=True)
                else:
                    self.player.level = min(self.player.level,15)


            if self.deposit_mode:
                self.bank_type_label.set_text("Deposit")
                self.max_type_label.set_text(f"${max(0.0,round(self.player.money,2))}")
            elif self.withdraw_mode:
                self.bank_type_label.set_text("Withdraw")
                self.max_type_label.set_text(f"${max(0.0,self.player.deposit)}")


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if not self.player.is_dead:
                        if event.key == pygame.K_d: # Move right
                            self.movement[1] = True
                            self.assets_sfx['walk'].play(-1)
                            self.movement[1] += 2
                        if event.key == pygame.K_a:  # Move left
                            self.movement[0] = True
                            self.assets_sfx['walk'].play(-1)
                            self.movement[0] += 2

                        if event.key == pygame.K_w: # Move down
                            self.movement[2] = True
                            self.assets_sfx['walk'].play(-1)
                            self.movement[2] += 2
                        if event.key == pygame.K_s: # Move up
                            self.movement[3] = True
                            self.assets_sfx['walk'].play(-1)
                            self.movement[3] += 2
                        if event.key == pygame.K_ESCAPE:
                            self.is_paused = not self.is_paused
                            pause(self)

                    if event.key == pygame.K_x:
                        if self.clickable:
                            if self.location == "home":
                                if self.player.pos[0] in range(100, 132) and self.player.pos[1] in range(250,260):
                                    change_location(self,'suburb')
                                elif self.player.pos[0] in range(10, 90) and self.player.pos[1] in range(177,235):
                                    if end_life(self):
                                        self.assets_sfx['game_over'].play()
                                        self.clickable = False
                                        self.save_btn.disable()
                                        self.save_btn.hide()
                                        self.sound_btn.disable()
                                        self.sound_btn.hide()
                                    else:
                                        if self.player.energy <= 70:
                                            advance_day(self)
                                            if self.player.day % 5 == 0:
                                                tax_player(self)

                                        else:
                                            PopupPanel.show_message(manager=self.manager,
                                                                    text=f"You are not tired enough.",
                                                                    screen_size=self.screen.get_size(),positive=False)

                            elif self.location == "suburb":
                                if self.player.pos[0] in range(600, 704) and self.player.pos[1] in range(500, 540):
                                    change_location(self,'town')
                                elif self.player.pos[0] in range(240, 270) and self.player.pos[1] in range(230, 250):
                                    change_location(self,'home')
                            elif self.location == "town":
                                if self.player.pos[0] in range(-15, 10) and self.player.pos[1] in range(163, 277):
                                    change_location(self,'suburb')

                                # DRUG STORE TRIGGER
                                if self.player.pos[0] in range(49, 85) and self.player.pos[1] in range(150, 165):
                                    self.is_action_panel = not self.is_action_panel
                                    if not self.is_paused:
                                        show_action(self,primary_action_type="doctor",secondary_action_type="salesman")


                                elif self.player.pos[0] in range(225, 272) and self.player.pos[1] in range(161,170):
                                    self.is_action_panel = not self.is_action_panel
                                    if not self.is_paused:
                                        show_action(self,primary_action_type="cook",secondary_action_type="cashier")

                                elif self.player.pos[0] in range(449, 485) and self.player.pos[1] in range(481,490):
                                    self.is_action_panel = not self.is_action_panel
                                    if not self.is_paused:
                                        show_action(self,primary_action_type="programmer",secondary_action_type="clerk")

                                elif self.player.pos[0] in range(65, 130) and self.player.pos[1] in range(481,500) :
                                    self.is_action_panel = not self.is_action_panel
                                    if not self.is_paused:
                                        show_action(self,primary_action_type="accountant",secondary_action_type="bank")



                if event.type == pygame.KEYUP:  # Handle key releases
                    if event.key == pygame.K_d:  # Stop moving right
                        self.movement[1] = False
                        self.assets_sfx['walk'].stop()

                    if event.key == pygame.K_a:  # Stop moving left
                        self.movement[0] = False
                        self.assets_sfx['walk'].stop()

                    if event.key == pygame.K_w:
                        self.movement[2] = False
                        self.assets_sfx['walk'].stop()

                    if event.key == pygame.K_s:
                        self.movement[3] = False
                        self.assets_sfx['walk'].stop()



                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.assets_sfx['click'].play()
                    if event.ui_element == self.pause_btn:
                        if self.player.is_dead:
                            for item in self.menu.save_list:
                                item.hide()
                            self.menu.run()
                        else:
                            self.is_paused = not self.is_paused
                            pause(self)


                    if event.ui_element == self.pause_menu_btn:
                        self.assets_sfx['ambience'].stop()
                        self.assets_sfx['pause'].stop()
                        for item in self.menu.save_list:
                            item.hide()
                        self.menu.run()
                    if event.ui_element == self.pause_load_btn:
                        self.is_paused = False
                        pause(self)
                        self.player= load_game(player=self.player,name=self.saved_name)
                        self.player.name = self.player.name[0]
                        PopupPanel.show_message(
                            manager=self.manager,
                            text="Current session loaded.",
                            screen_size=self.screen.get_size()
                        )


                    if event.ui_element == self.save_btn:
                        overwrite_save(self.player,self.old_name)
                        self.saved_name = self.player.name
                        PopupPanel.show_message(
                            manager=self.manager,
                            text="Current session successfully saved.",
                            screen_size=self.screen.get_size()
                        )
                    if event.ui_element == self.rate_btn:
                        if not self.is_paused:
                            self.is_rate_panel = not self.is_rate_panel
                            init_chart(self)


                    # -----------------------------Action_Buttons ----------------------------- #

                    if event.ui_element == self.primary_job_button:
                        # -----------Medical_Action_Buttons----------- #
                        if self.in_drug_store:
                            if self.player.check_lvl(self,load_jobs()[5]):
                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Doctor!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[5]
                                elif self.player.job.name !="Doctor":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Doctor!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[5]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)

                        # -----------Burger_Shop_Action_Buttons----------- #
                        if self.in_burgershop:
                            if self.player.check_lvl(self,load_jobs()[6]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Cook!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[6]
                                elif self.player.job.name !="Cook":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Cook!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[6]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)

                        # -----------Office_Action_Buttons----------- #
                        if self.in_office:
                            if self.player.check_lvl(self,load_jobs()[4]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Programmer!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[4]
                                elif self.player.job.name !="Programmer":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Programmer!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[4]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)
                            # -----------Bank_Action_Buttons----------- #
                        if self.in_bank:
                            if self.player.check_lvl(self,load_jobs()[3]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as an Accountant!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[3]
                                elif self.player.job.name !="Accountant":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as an Accountant!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[3]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)



                    if event.ui_element == self.secondary_job_button:
                        # -----------Salesman_Action_Buttons----------- #

                        if self.in_drug_store:
                            if self.player.check_lvl(self,load_jobs()[1]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Salesman!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[1]
                                elif self.player.job.name !="Salesman":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Salesman!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[1]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)

                        # -----------Burger_Shop_Action_Buttons----------- #

                        if self.in_burgershop:
                            if self.player.check_lvl(self,load_jobs()[0]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Cashier!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[0]
                                elif self.player.job.name !="Cashier":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Cashier!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[0]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)


                        # -----------Office_Action_Buttons----------- #
                        if self.in_office:
                            if self.player.check_lvl(self,load_jobs()[2]):

                                if self.player.job is None:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Clerk!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[2]
                                elif self.player.job.name !="Clerk":
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="You now work as a Clerk!",
                                        screen_size=self.screen.get_size()
                                    )
                                    self.player.job = load_jobs()[2]
                                else:
                                    self.player.work(self)
                                set_panel_text(self)

                        if self.in_bank:
                            self.withdraw_mode = False
                            self.deposit_mode = True
                            set_transaction_type(self)



                    if event.ui_element == self.primary_action_button:
                        # -----------Medical_Action_Buttons----------- #
                        if self.in_drug_store:
                            if self.player.money >= (((20 * self.economy.inflation)/10) + 20):
                                self.player.health += 25
                                self.player.money -= (((20 * self.economy.inflation)/10) + 20)
                                self.player.health = min(self.player.health,100)
                            else:
                                PopupPanel.show_message(
                                    manager=self.manager,
                                    text="You can't afford healthcare!",
                                    screen_size=self.screen.get_size(),positive=False
                                )

                        # -----------Burger_Shop_Action_Buttons----------- #
                        if self.in_burgershop:
                            if self.player.money >= (((20 * self.economy.inflation)/10) + 20):
                                self.player.money -= (((20 * self.economy.inflation)/10) + 20)
                                self.player.hunger += 25
                                self.player.hunger = min(self.player.hunger,100)
                            else:
                                PopupPanel.show_message(
                                    manager=self.manager,
                                    text="You can't afford a Burger!",
                                    screen_size=self.screen.get_size(),positive=False
                                )

                        if self.in_office:
                            change_name(self)

                        if self.in_bank:
                            self.deposit_mode = False
                            self.withdraw_mode = True
                            set_transaction_type(self)

                    if event.ui_element == self.secondary_action_button:
                        # -----------Burger_Shop_Action_Buttons----------- #
                        if self.in_burgershop:
                            if self.player.money >=(((35 * self.economy.inflation)/10) + 35):
                                self.player.money -= (((35 * self.economy.inflation)/10) + 35)
                                self.player.hunger += 40
                                self.player.hunger = min(self.player.hunger,100)
                            else:
                                PopupPanel.show_message(
                                    manager=self.manager,
                                    text="You can't afford a Pizza!",
                                    screen_size=self.screen.get_size(),positive=False
                                )
                    if event.ui_element == self.change_name_cancel_btn:
                        if self.in_office:
                            self.primary_action_button.visible = True
                            self.primary_action_label.visible = True
                        self.change_name_prompt.clear()
                        self.change_name_panel.visible = False
                        self.change_name_cancel_btn.visible = False
                        self.change_name_prompt.visible = False
                        self.change_name_continue_btn.visible = False

                    if event.ui_element == self.bank_cancel_btn:
                        self.bank_prompt.clear()
                        self.bank_panel.visible = False
                        self.bank_type_label.visible = False
                        self.min_type_label.visible = False
                        self.max_type_label.visible = False
                        self.bank_cancel_btn.visible = False
                        self.bank_prompt.visible = False
                        self.bank_continue_btn.visible = False

                    if event.ui_element == self.chart_cancel_btn:
                        self.is_rate_panel = False
                        self.chart_cancel_btn.visible = False
                        self.chart_panel.visible = False
                        self.chart_image.visible = False
                        self.chart_icon.visible = False

                    if event.ui_element == self.change_name_continue_btn:
                        if not self.is_paused:
                            self.old_name = self.player.name
                            self.player.name = self.change_name_prompt.text

                    if event.ui_element == self.bank_continue_btn:
                        if not self.is_paused:
                            if self.deposit_mode:
                                try:
                                    self.player.deposit_money(amount=float(self.bank_prompt.text),game=self)
                                    self.bank_prompt.clear()
                                except ValueError:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="Enter an actual number!",
                                        screen_size=self.screen.get_size(),positive=False
                                    )
                            elif self.withdraw_mode:
                                try:
                                    self.player.withdraw_money(amount=float(self.bank_prompt.text),game=self)
                                    self.bank_prompt.clear()
                                except ValueError:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="Enter an actual number!",
                                        screen_size=self.screen.get_size(),positive=False
                                    )

                            else:
                                continue

                    if event.ui_element == self.sound_btn:
                        self.mute = not self.mute
                        if self.mute:
                            PopupPanel.show_message(
                                manager=self.manager,
                                text="SFX State: Muted.",
                                screen_size=self.screen.get_size(), positive=False
                            )
                            self.assets_sfx['ambience'].set_volume(0.0)
                            self.assets_sfx['pause'].set_volume(0.0)
                        else:
                            PopupPanel.show_message(
                                manager=self.manager,
                                text="SFX State: Unmuted.",
                                screen_size=self.screen.get_size(),
                            )
                            self.assets_sfx['ambience'].set_volume(0.1)
                            self.assets_sfx['pause'].set_volume(0.2)

                self.manager.process_events(event)

            self.display_2.blit(self.display,(0,0))


            # Draw
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0, 0))
            self.manager.draw_ui(self.screen)

            if self.location == "home":
                if (self.player.pos[0] in range(100, 132) and self.player.pos[1] in range(250,260) or
                self.player.pos[0] in range(10, 90) and self.player.pos[1] in range(190,235)):
                    interact()
                else:
                    self.clickable = False

            elif self.location == "suburb":
                if (self.player.pos[0] in range(240, 270) and self.player.pos[1] in range(230,250) or
                        self.player.pos[0] in range(600, 704) and self.player.pos[1] in range(500,540)):
                    interact()
                else:
                    self.clickable = False

            elif self.location == "town":
                if (self.player.pos[0] in range(49, 85) and self.player.pos[1] in range(150,165) or
                    self.player.pos[0] in range(225, 272) and self.player.pos[1] in range(161,170) or
                    self.player.pos[0] in range(449, 485) and self.player.pos[1] in range(481,490) or
                    self.player.pos[0] in range(65, 130) and self.player.pos[1] in range(481,500) or
                    self.player.pos[0] in range(-15, 10) and self.player.pos[1] in range(163, 277)
                    ) :
                    interact()
                else:
                    self.clickable = False
            self.money_image.render(self.screen)

            self.screen.blit(self.assets['cursor'],mpos)

            pygame.display.update()
            self.money_animator.update(dt)
            self.smooth_energy_bar.update(dt)
            self.smooth_hunger_bar.update(dt)
            self.smooth_health_bar.update(dt)
            self.smooth_lvl_bar.update(dt)
            self.manager.update(dt)

