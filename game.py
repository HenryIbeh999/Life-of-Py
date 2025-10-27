from scripts.entities import Coin
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
        self.player.name = self.player.name[0]
        self.player.money = round((float(self.player.money)),2)
        self.old_name = self.player.name
        self.saved_name = self.player.name

        #-----------------------------Indicators ----------------------------- #
        self.location = ""
        self.is_paused = False
        self.is_action_panel = False
        self.is_change_name_panel = False
        self.is_home = True
        self.clickable = False
        self.in_drug_store = False
        self.in_burgershop = False
        self.in_office = False
        self.in_bank = False
        self.deposit_mode = False
        self.withdraw_mode = False
        #-----------------------------Indicators ----------------------------- #


        if self.is_home:
            self.location = "town"
        # self.manager.set_visual_debug_mode(is_active=True)

        self.assets = {
            'decor': load_images('tiles/decor'),
            'terrain': load_images('tiles/terrain'),
            'large_decor': load_images('tiles/large_decor'),
            'stone': load_images('tiles/stone'),
            'building': load_images('tiles/building'),
            'location' : load_image(f'{self.location}.jpg'),
            'bed': load_images('tiles/bed'),
            'toilet': load_images('tiles/toilet'),
            'furniture': load_images('tiles/furniture'),
            'structure': load_images('tiles/structure'),
            'wall': load_images('tiles/wall'),
            'rug': load_images('tiles/rug'),
            'shelve': load_images('tiles/shelve'),
            'sofas': load_images('tiles/sofas'),
            'painting': load_images('tiles/painting'),
            'fireplace': load_images('tiles/fireplace'),
            'item/coin' : Animation(load_images('coins')),
            'job' : load_image('ui/job.png'),
            'energy' : load_image('ui/energy.png'),
            'happiness' : load_image('ui/happiness.png'),
            'hunger' : load_image('ui/hunger.png'),
            'x_button' : load_image('ui/x_button.png'),
            "cursor": load_image("cursor/cursor.png"),
            "calender": load_image("ui/calender.png"),
            "ui_character": load_image(f"ui/ui_character.png"),

        }
#******************** UI **********************#

        self.status_panel = UIPanel(relative_rect=pygame.Rect(0,0, 300, 300),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#status_panel"))
        self.name_status_panel = UIPanel(relative_rect=pygame.Rect(0,0, 300, 50),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#player_status_panel"))
        self.player_name_label = UILabel(relative_rect=pygame.Rect(50,10,-1,-1),text=f"{self.player.name}",manager=self.manager,container=self.name_status_panel, object_id=ObjectID(class_id="@text",object_id="#name_text"))
        self.character_image = UIImage(relative_rect=pygame.Rect(10,5,30,30),image_surface=self.assets['ui_character'],manager=self.manager,container=self.name_status_panel)
        self.job_image = UIImage(relative_rect=pygame.Rect(20,60,24,24),image_surface=self.assets['job'],manager=self.manager,container=self.status_panel)
        self.player_job_label = UILabel(relative_rect=pygame.Rect(48,60,-1,-1),text=f"{self.player.job}",manager=self.manager,container=self.status_panel, object_id=ObjectID(class_id="@text",object_id="#job_text"))
        self.money_image = Coin(self,(165,70),(16,16))
        self.player_money_label = UILabel(relative_rect=pygame.Rect(180,60,-1,-1),text=f"${self.player.money}",manager=self.manager,container=self.status_panel, object_id=ObjectID(class_id="@text",object_id="#money_text"))
        self.money_animator = MoneyAnimator(self.player_money_label)
        self.money_animator.current_value = round((float(self.player.money)),2)
        self.energy_image = UIImage(relative_rect=pygame.Rect(20,100,28,28),image_surface=self.assets['energy'],manager=self.manager,container=self.status_panel)
        self.energy_bar = UIProgressBar(relative_rect=pygame.Rect(48,100,180,27),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#hunger_bar"))
        self.smooth_energy_bar = SmoothProgressBar(self.energy_bar)
        self.hunger_image = UIImage(relative_rect=pygame.Rect(20,140,28,28),image_surface=self.assets['hunger'],manager=self.manager,container=self.status_panel)
        self.hunger_bar = UIProgressBar(relative_rect=pygame.Rect(48,140,180,27),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#hunger_bar"))
        self.smooth_hunger_bar = SmoothProgressBar(self.hunger_bar)
        self.happiness_image = UIImage(relative_rect=pygame.Rect(20,180,28,28),image_surface=self.assets['happiness'],manager=self.manager,container=self.status_panel)
        self.happiness_bar = UIProgressBar(relative_rect=pygame.Rect(48,180,180,27),manager=self.manager,container=self.status_panel,object_id=ObjectID(class_id="@high_progress_bar",object_id="#happiness_bar"))
        self.smooth_happiness_bar = SmoothProgressBar(self.happiness_bar)

        #******************* MISC ****************************#
        self.misc_status_panel = UIPanel(relative_rect=pygame.Rect(0,0,400,80),manager=self.manager,object_id=ObjectID(class_id="@panel",object_id="#misc_status_panel"),anchors={"centerx":"centerx"})
        self.pause_btn = UIButton(relative_rect=pygame.Rect(20,0,30,30),text="",manager=self.manager,container=self.misc_status_panel,tool_tip_text="Pause Game",object_id=ObjectID(class_id="@misc_button",object_id="#pause_button"),anchors={"centery":"centery"})
        self.sound_btn = UIButton(relative_rect=pygame.Rect(70,0,30,30),text="",manager=self.manager,container=self.misc_status_panel,tool_tip_text="Mute BG music",object_id=ObjectID(class_id="@misc_button",object_id="#sound_button"),anchors={"centery":"centery"})
        self.day_image = UIImage(relative_rect=pygame.Rect(-50,0,30,30),image_surface=self.assets['calender'],manager=self.manager,container=self.misc_status_panel,anchors={"center": "center"})
        self.day_label = UILabel(relative_rect=pygame.Rect(30, 0, -1, -1), text=f"Day {player.day}", manager=self.manager, container=self.misc_status_panel, object_id=ObjectID(class_id="@text", object_id="#day_text"), anchors={"center": "center"})
        self.save_btn = UIButton(relative_rect=pygame.Rect(300,0,62,30),text="",manager=self.manager,container=self.misc_status_panel,tool_tip_text="Save Game",object_id=ObjectID(class_id="@misc_button",object_id="#save_button"),anchors={"centery":"centery"})
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
        self.min_type_label = UILabel(relative_rect=(35,-25,-1,-1), text=f"${1.00}",anchors={"centery": "centery"} , manager=self.manager,container=self.bank_panel, object_id = ObjectID(class_id='@action_text', object_id='#min_type_label'))
        self.max_type_label = UILabel(relative_rect=(235,-25,-1,-1), text="",anchors={"centery": "centery"} , manager=self.manager,container=self.bank_panel, object_id = ObjectID(class_id='@action_text', object_id='#max_type_label'))
        self.bank_prompt = UITextEntryLine(relative_rect=pygame.Rect(0, 50, 150, 50), manager=self.manager,container=self.bank_panel,placeholder_text="", anchors={'centerx': 'centerx'},object_id=ObjectID(class_id="@input", object_id="#new_name_input"))
        self.bank_continue_btn = UIButton(relative_rect=pygame.Rect(0,120,94,30),text="",manager=self.manager, anchors={"centerx": "centerx"},container=self.bank_panel,object_id=ObjectID(class_id="@misc_button",object_id="#continue_button"))

        #*******************ACTIONS SECTION********************#

#******************** UI **********************#

        self.tile_map =TileMap(self,tile_size=16)
        self.load_map(self.location)
        self.run()


    def load_map(self, map_id):
        self.tile_map.load(f'data/maps/{map_id}.json')
        for spawner in self.tile_map.extract([('spawners', 0),('spawners', 1)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
        self.scroll = [0,0]



    def run(self):
        circle_transition(self)
        running = True
        while running:
            self.display.fill((0,0,0,0))
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
                if self.is_action_panel is False and self.is_paused is False:
                    self.clickable = True
                    self.screen.blit(self.assets["x_button"], (screen_x - 5, screen_y - 60))
                else:
                    pass

            if self.location == "home":
                self.display_2.blit(self.assets['location'], (bg_x - 50, bg_y - 50))
            elif self.location in ("suburb", "town"):
                self.display_2.blit(self.assets['location'], (bg_x, bg_y))
            else:
                # fallback: draw the location at (0,0) so nothing weird happens
                self.display_2.blit(self.assets['location'], (bg_x, bg_y))

            self.tile_map.render(self.display, offset=render_scroll)

            if not self.pause_panel.visible and not self.action_panel.visible and not self.change_name_panel.visible and not self.bank_panel.visible:
                self.player.update(self.tile_map, (self.movement[1] - self.movement[0], self.movement[3]- self.movement[2]))

            try:
                self.player_job_label.set_text(f"{self.player.job.name}")
            except AttributeError:
                self.player_job_label.set_text(f"{self.player.job}")
            self.player_name_label.set_text(f"{self.player.name}")
            self.money_animator.set_target(self.player.money)
            self.smooth_energy_bar.set_value(float(self.player.energy))
            if self.player.energy <= 30.0:
                self.energy_bar.change_object_id("@low_progress_bar")
            else:
                self.energy_bar.change_object_id("@high_progress_bar")

            self.smooth_happiness_bar.set_value(float(self.player.happiness))
            if self.player.happiness <= 30.0:
                self.happiness_bar.change_object_id("@low_progress_bar")
            else:
                self.happiness_bar.change_object_id("@high_progress_bar")
            self.smooth_hunger_bar.set_value(float(self.player.hunger))
            if self.player.hunger <= 30.0:
                self.hunger_bar.change_object_id("@low_progress_bar")
            else:
                self.hunger_bar.change_object_id("@high_progress_bar")


            if self.deposit_mode:
                self.bank_type_label.set_text("Deposit")
                self.max_type_label.set_text(f"${max(0.0,self.player.money)}")
            elif self.withdraw_mode:
                self.bank_type_label.set_text("Withdraw")
                self.max_type_label.set_text(f"${max(0.0,self.player.deposit)}")
            self.player.render(self.display, offset=render_scroll)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d: # Move right
                        self.movement[1] = True
                        self.movement[1] += 2
                    if event.key == pygame.K_a:  # Move left
                        self.movement[0] = True
                        self.movement[0] += 2

                    if event.key == pygame.K_w: # Move down
                        self.movement[2] = True
                        self.movement[2] += 2
                    if event.key == pygame.K_s: # Move up
                        self.movement[3] = True
                        self.movement[3] += 2
                    if event.key == pygame.K_ESCAPE:
                        self.is_paused = not self.is_paused
                        pause(self)

                    if event.key == pygame.K_x:
                        if self.clickable:
                            if self.location == "home":
                                exit_house(self)
                            elif self.location == "suburb":
                                if self.player.pos[0] in range(600, 704) and self.player.pos[1] in range(500, 540):
                                    exit_suburb(self)
                                elif self.player.pos[0] in range(240, 270) and self.player.pos[1] in range(230, 250):
                                    enter_house(self)
                            elif self.location == "town":

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
                    if event.key == pygame.K_d:  # Stop moving left
                        self.movement[1] = False
                    if event.key == pygame.K_a:  # Stop moving right
                        self.movement[0] = False

                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False



                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.pause_btn:
                        self.is_paused = not self.is_paused
                        pause(self)


                    if event.ui_element == self.pause_menu_btn:
                        for item in self.menu.save_list:
                            item.visible = False
                        self.menu.run()
                    if event.ui_element == self.pause_load_btn:
                        self.is_paused = False
                        pause(self)
                        self.player= load_game(player=self.player,name=self.saved_name)
                        self.player.name = self.player.name[0]


                    if event.ui_element == self.save_btn:
                        overwrite_save(self.player,self.old_name)
                        self.saved_name = self.player.name

                    # -----------------------------Action_Buttons ----------------------------- #

                    if event.ui_element == self.primary_job_button:
                        # -----------Medical_Action_Buttons----------- #
                        if self.in_drug_store:
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
                            self.player.happiness += 20
                            self.player.happiness = min(self.player.happiness,100)
                        # -----------Burger_Shop_Action_Buttons----------- #
                        if self.in_burgershop:
                            if self.player.money >= 20:
                                self.player.money -= 20
                                self.player.hunger += 25
                                self.player.hunger = min(self.player.hunger,100)
                            else:
                                PopupPanel.show_message(
                                    manager=self.manager,
                                    text="Money Too Low!",
                                    screen_size=self.screen.get_size()
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
                            if self.player.money >= 35:
                                self.player.money -= 35
                                self.player.hunger += 40
                                self.player.hunger = min(self.player.hunger,100)
                            else:
                                PopupPanel.show_message(
                                    manager=self.manager,
                                    text="Money Too Low!",
                                    screen_size=self.screen.get_size()
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

                    if event.ui_element == self.change_name_continue_btn:
                        if not self.is_paused:
                            self.old_name = self.player.name
                            self.player.name = self.change_name_prompt.text

                    if event.ui_element == self.bank_continue_btn:
                        if not self.is_paused:
                            if self.deposit_mode:
                                try:
                                    self.player.deposit_money(amount=float(self.bank_prompt.text),game=self)
                                except ValueError:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="Enter an actual number!",
                                        screen_size=self.screen.get_size()
                                    )
                            elif self.withdraw_mode:
                                try:
                                    self.player.withdraw_money(amount=float(self.bank_prompt.text),game=self)
                                except ValueError:
                                    PopupPanel.show_message(
                                        manager=self.manager,
                                        text="Enter an actual number!",
                                        screen_size=self.screen.get_size()
                                    )

                            else:
                                continue

                self.manager.process_events(event)
            dt = self.clock.tick(60)

            self.display_2.blit(self.display,(0,0))


            # Draw
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0, 0))
            self.manager.draw_ui(self.screen)

            if self.location == "home":
                if self.player.pos[0] in range(200, 260) and self.player.pos[1] in range(100,140):
                    interact()
                else:
                    self.clickable = False

            elif self.location == "suburb":
                if self.player.pos[0] in range(240, 270) and self.player.pos[1] in range(230,250) or  self.player.pos[0] in range(600, 704) and self.player.pos[1] in range(500,540):
                    interact()
                else:
                    self.clickable = False

            elif self.location == "town":
                if (self.player.pos[0] in range(49, 85) and self.player.pos[1] in range(150,165) or
                    self.player.pos[0] in range(225, 272) and self.player.pos[1] in range(161,170) or
                    self.player.pos[0] in range(449, 485) and self.player.pos[1] in range(481,490) or
                    self.player.pos[0] in range(65, 130) and self.player.pos[1] in range(481,500)
                ) :
                    interact()
                else:
                    self.clickable = False
            self.money_image.update(self.tile_map)
            self.money_image.render(self.screen)

            self.screen.blit(self.assets['cursor'],mpos)

            pygame.display.update()
            self.manager.update(dt / 1000.0)
            self.money_animator.update(dt / 1000.0)
            self.smooth_energy_bar.update(dt / 1000.0)
            self.smooth_hunger_bar.update(dt / 1000.0)
            self.smooth_happiness_bar.update(dt / 1000.0)


