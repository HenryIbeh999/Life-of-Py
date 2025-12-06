import time

from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel

from scripts.utils import load_image
import pytweening
import pygame
from subclass.pop_up_panel import PopupPanel
from scripts.economy import *
from scripts.jobs import load_jobs
from subclass.ui_panel import AnimatedPanel

"""There wasn't really an appropriate place to put these functions, so here they are."""
def show_action(game, primary_action_type, secondary_action_type):
    if game.is_action_panel is True:
        game.action_panel.show()
        game.action_panel.slide_to((0, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.ui_action_image.show()
        game.small_action_panel.show()
        game.small_action_panel.slide_to((0, -167), duration=1.0, easing=pytweening.easeOutBack)
        game.primary_job_button.show()
        game.primary_job_label.show()
        game.secondary_job_button.show()
        game.secondary_job_label.show()
        game.primary_action_button.show()
        game.primary_action_label.show()
        game.rate_btn.disable()



        if primary_action_type == "doctor" and secondary_action_type == "salesman":
            game.ui_action_image.set_image(load_image("ui/ui_doctor.png"))

            game.primary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#job_doctor_button"))
            game.primary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#action_doctor_button"))
            game.secondary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#job_salesman_button"))
            game.secondary_action_button.hide()
            game.secondary_action_label.hide()
            game.in_drug_store = True
            game.in_burgershop = False
            game.in_office = False
            game.in_bank = False
            set_panel_text(game)


        if primary_action_type == "cook" and secondary_action_type == "cashier":
            game.ui_action_image.set_image(load_image("ui/ui_burgershop.png"))
            game.primary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#job_cook_button"))
            game.primary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#action_burger_button"))
            game.secondary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#job_cashier_button"))
            game.secondary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#action_pizza_button"))
            game.secondary_action_button.show()
            game.secondary_action_label.show()
            game.in_drug_store = False
            game.in_burgershop = True
            game.in_office = False
            game.in_bank = False
            set_panel_text(game)

        if primary_action_type == "programmer" and secondary_action_type == "clerk":
            game.ui_action_image.set_image(load_image("ui/ui_office.png"))
            game.primary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#job_programmer_button"))
            game.primary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#action_change_name_button"))
            game.secondary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#job_clerk_button"))
            game.secondary_action_button.hide()
            game.secondary_action_label.hide()
            game.in_drug_store = False
            game.in_burgershop = False
            game.in_office = True
            game.in_bank = False
            set_panel_text(game)

        if primary_action_type == "accountant" and secondary_action_type == "bank":
            game.ui_action_image.set_image(load_image("ui/ui_bank.png"))
            game.primary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#job_accountant_button"))
            game.secondary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#action_deposit_button"))
            game.primary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id="#action_withdraw_button"))

            game.secondary_action_button.hide()
            game.secondary_action_label.hide()
            game.in_drug_store = False
            game.in_burgershop = False
            game.in_office = False
            game.in_bank = True
            set_panel_text(game)
    else:
        game.action_panel.hide()
        game.small_action_panel.hide()
        game.ui_action_image.hide()
        game.primary_job_button.hide()
        game.primary_job_label.hide()
        game.secondary_job_button.hide()
        game.secondary_job_label.hide()
        game.primary_action_button.hide()
        game.primary_action_label.hide()
        game.secondary_action_button.hide()
        game.secondary_action_label.hide()
        game.rate_btn.enable()


def set_panel_text(game):
    if game.in_drug_store:
        medical_salary = round(load_jobs()[5].base_salary * game.economy.salary_index,2)
        sales_salary = round(load_jobs()[1].base_salary * game.economy.salary_index,2)
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Medical field - ${medical_salary}")
            game.secondary_job_label.set_text(f"Work in the Sales field - ${sales_salary}")
        elif game.player.job.name != "Doctor" and game.player.job.name != "Salesman":
            game.primary_job_label.set_text(f"Work in the Medical field - ${medical_salary}")
            game.secondary_job_label.set_text(f"Work in the Sales field - ${sales_salary}")
        elif game.player.job.name == "Doctor":
            game.primary_job_label.set_text(f"Work as a Doctor - ${medical_salary}")
            game.secondary_job_label.set_text(f"Work in the Sales field - ${sales_salary}")
        elif game.player.job.name == "Salesman":
            game.primary_job_label.set_text(f"Work in the Medical field - ${medical_salary}")
            game.secondary_job_label.set_text(f"Work as a Salesman - ${sales_salary}")
        game.primary_action_label.set_text(f"Health check-up - ${round((((20 * game.economy.inflation) / 10) + 20),2)}")

    if game.in_burgershop:
        cook_salary = round(load_jobs()[6].base_salary * game.economy.salary_index,2)
        cashier_salary = round(load_jobs()[0].base_salary * game.economy.salary_index,2)
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Culinary field - ${cook_salary}")
            game.secondary_job_label.set_text(f"Work in the Cashier field - ${cashier_salary}")

        elif game.player.job.name != "Cook" and game.player.job.name != "Cashier":
            game.primary_job_label.set_text(f"Work in the Culinary field - ${cook_salary}")
            game.secondary_job_label.set_text(f"Work in the Cashier field - ${cashier_salary}")
        elif game.player.job.name == "Cook":
            game.primary_job_label.set_text(f"Work as a Cook - ${cook_salary}")
            game.secondary_job_label.set_text(f"Work in the Cashier field - ${cashier_salary}")
        elif game.player.job.name == "Cashier":
            game.primary_job_label.set_text(f"Work in the Culinary field - ${cook_salary}")
            game.secondary_job_label.set_text(f"Work as a Cashier - ${cashier_salary}")
        game.primary_action_label.set_text(f"Order a Burger Meal - ${round((((20 * game.economy.inflation) / 10) + 20),2)}")
        game.secondary_action_label.set_text(f"Order a Pizza - ${round((((35 * game.economy.inflation) / 10) + 35),2)}")

    if game.in_office:
        programmer_salary = round((load_jobs()[4].base_salary * game.economy.salary_index),2)
        clerk_salary = round(load_jobs()[2].base_salary * game.economy.salary_index,2)
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Tech field - ${programmer_salary}")
            game.secondary_job_label.set_text(f"Work in the Reception field - ${clerk_salary}")
        elif game.player.job.name != "Programmer" and game.player.job.name != "Clerk":
            game.primary_job_label.set_text(f"Work in the Tech field - ${programmer_salary}")
            game.secondary_job_label.set_text(f"Work in the Reception field - ${clerk_salary}")
        elif game.player.job.name == "Programmer":
            game.primary_job_label.set_text(f"Work as a Programmer - ${programmer_salary}")
            game.secondary_job_label.set_text(f"Work in the Reception field - ${clerk_salary}")
        elif game.player.job.name == "Clerk":
            game.primary_job_label.set_text(f"Work in the Tech field - ${programmer_salary}")
            game.secondary_job_label.set_text(f"Work as a Clerk - ${clerk_salary}")
        game.primary_action_label.set_text("Change your name")

    if game.in_bank:
        accountant_salary = round(load_jobs()[3].base_salary * game.economy.salary_index,2)

        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Financial field - ${accountant_salary}")
        elif game.player.job.name != "Accountant":
            game.primary_job_label.set_text(f"Work in the Financial field - ${accountant_salary}")
        elif game.player.job.name == "Accountant":
            game.primary_job_label.set_text(f"Work as an Accountant - ${accountant_salary}")
        game.secondary_job_label.set_text("Deposit Money")
        game.primary_action_label.set_text("Withdraw Money")



def pause(game):
    if game.is_paused is True:
        game.clickable = False
        game.assets_sfx['ambience'].set_volume(0.0)

        game.assets_sfx['n-ambience'].set_volume(0.0)
        game.assets_sfx['pause'].play(-1)
        game.is_action_panel = False
        game.action_panel.hide()
        game.small_action_panel.hide()
        game.ui_action_image.hide()
        game.primary_job_button.hide()
        game.primary_job_label.hide()
        game.secondary_job_button.hide()
        game.secondary_job_label.hide()
        game.primary_action_button.hide()
        game.primary_action_label.hide()
        game.secondary_action_button.hide()
        game.secondary_action_label.hide()
        game.change_name_panel.hide()
        game.change_name_prompt.hide()
        game.change_name_cancel_btn.hide()
        game.is_rate_panel = False
        game.chart_panel.hide()
        game.chart_image.hide()
        game.chart_cancel_btn.hide()
        game.rate_btn.disable()


        game.pause_panel.show()
        game.pause_panel.slide_to((0, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.pause_load_btn.show()
        game.pause_menu_btn.show()
        game.credit_head_label.show()
        game.credit_sub_1_label.show()
        game.credit_sub_2_label.show()
        game.credit_sub_3_label.show()

    else:
        game.clickable = True
        game.assets_sfx['pause'].stop()
        if not game.is_night:
            game.assets_sfx['ambience'].set_volume(0.1)
        else:
            game.assets_sfx['n-ambience'].set_volume(0.4)
        game.pause_panel.hide()
        game.pause_load_btn.hide()
        game.pause_menu_btn.hide()
        game.credit_head_label.hide()
        game.credit_sub_1_label.hide()
        game.credit_sub_2_label.hide()
        game.credit_sub_3_label.hide()
        game.rate_btn.enable()


def change_location(game,location):
    game.location = location
    if location == "home":
        game.is_home = True
    game.assets['location'] = load_image(f'{game.location}.png')
    game.load_map(game.location)

    circle_transition(game)


def check_time(game):
    if game.player.energy <= 40:
        game.is_night = True
        if game.is_night:
            if game.location == 'home':
                game.assets['location'] = load_image(f'night_{game.location}.png')
            else:
                game.assets['location'] = load_image(f'night_{game.location}.jpg')

            game.assets_sfx['n-ambience'].set_volume(0.4)
            game.assets_sfx['ambience'].set_volume(0.0)




    elif game.player.energy > 40:
        game.is_night = False
        game.assets['location'] = load_image(f'{game.location}.png')
        if not game.is_night:
            game.assets_sfx['n-ambience'].set_volume(0.0)
            game.assets_sfx['ambience'].set_volume(0.1)


def circle_transition(game, duration=1000):
    check_time(game)
    center = (game.display_2.get_width() // 2, game.display_2.get_height() // 2)
    max_radius = int((game.display_2.get_width() ** 2 + game.display_2.get_height() ** 2) ** 0.5)
    start_time = pygame.time.get_ticks()
    pygame.mixer.music.load('data/sfx/flow.wav')
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play()
    while True:
        game.clickable = False
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        progress = min(1, elapsed / duration)
        radius = int(progress * max_radius)

        # Draw game scene
        game.display.fill((0, 0, 0, 0))
        if game.is_night:
            game.display_2.fill((45, 38, 43))
        else:
            game.display_2.fill((159, 226, 255))
        if game.location == 'home':
            game.display_2.blit(game.assets['location'], (100,0))
        else:
            game.display_2.blit(game.assets['location'], (0,0))

        game.tile_map.render(game.display, offset=(0, 0))

        # Create transition mask
        mask = pygame.Surface(game.display_2.get_size(), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 255))
        pygame.draw.circle(mask, (0, 0, 0, 0), center, radius)



        game.display_2.blit(mask, (0, 0))
        game.screen.blit(pygame.transform.scale(game.display_2, game.screen.get_size()), (0, 0))


        pygame.display.update()


        if progress >= 1:
            game.player.pos[0] = int(game.player.pos[0])
            game.player.pos[1] = int(game.player.pos[1])
            game.clickable = True
            break

def change_name(game):
    game.is_change_name_panel = True
    if game.is_change_name_panel and game.in_office:
        game.change_name_panel.show()
        game.change_name_cancel_btn.show()
        game.change_name_prompt.show()
        game.change_name_continue_btn.show()
        game.primary_action_button.hide()
        game.primary_action_label.hide()
        game.change_name_panel.slide_to((0, 50), duration=1.0, easing=pytweening.easeOutBack)
    else:
        game.clickable = True


def set_transaction_type(game):
    if game.in_bank:
        game.bank_panel.show()
        game.bank_panel.slide_to((0, 70), duration=1.0, easing=pytweening.easeOutBack)
        game.bank_type_label.show()
        game.bank_prompt.show()
        game.bank_cancel_btn.show()
        game.bank_continue_btn.show()
        game.min_type_label.show()
        game.max_type_label.show()

def get_salary(game):
    salary = game.player.job.base_salary * game.economy.salary_index
    return salary

def gain_interest(game):
    rate = game.economy.interest_rate
    principal = game.player.deposit
    day= 1

    interest = round(float((principal * rate * day)/20),2)

    return interest

def init_chart(game):
    if game.is_rate_panel:
        game.clickable = False
        game.chart_panel.show()
        game.chart_panel.slide_to((100, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.chart_image.set_image(show_graph(game))
        game.chart_image.show()
        game.chart_icon.show()
        game.chart_cancel_btn.show()
    else:
        game.clickable = True
        game.chart_panel.hide()
        game.chart_image.hide()
        game.chart_icon.hide()
        game.chart_cancel_btn.hide()


def advance_day(game):
    game.player.energy = 100.0
    game.player.day += 1
    game.is_rate_panel = False
    game.chart_panel.hide()
    game.chart_image.hide()
    game.chart_cancel_btn.hide()
    advance_economy(game)
    save_economy(game)
    update_csv(game)
    circle_transition(game)

    if game.player.day % 2 == 0:
        if game.player.deposit > 0:
            interest = gain_interest(game)
            game.player.deposit += interest
            game.achievement.money_made += interest
            PopupPanel.show_message(manager=game.manager,text=f"You have gained a ${interest} interest on your deposit",screen_size=game.screen.get_size())
    return


def end_life(game):
    if 0 < game.player.health <= 40:
        PopupPanel.show_message(
            manager=game.manager,
            text="You really need a health checkup!",
            screen_size=game.screen.get_size(), positive=False
        )
        return False

    elif game.player.health == 0.0 or game.player.hunger == 0.0:
        dead_panel = AnimatedPanel(relative_rect=pygame.Rect(0,0,400,500),manager=game.manager,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#death_panel"))
        small_dead_panel =AnimatedPanel(relative_rect=pygame.Rect(0,0,300,300),manager=game.manager,container=dead_panel,anchors={'center': 'center'},object_id=ObjectID(class_id="@panel", object_id="#death_panel"))
        dead_panel.slide_to((300, 0), duration=1.0, easing=pytweening.easeOutBack)

        UILabel(relative_rect=(0,20,-1,-1), anchors={"centerx":"centerx"},container=dead_panel,text="YOU ARE DEAD",manager=game.manager,object_id=ObjectID("@label","#dead_label"))
        if game.player.health == 0:
            UILabel(relative_rect=(0,60,-1,-1), anchors={"centerx":"centerx"},container=dead_panel,
                                 text="Health is Wealth",manager=game.manager,object_id=ObjectID("@label","#small_dead_label"))
        elif game.player.hunger == 0:
            UILabel(relative_rect=(0, 60, -1, -1), anchors={"centerx": "centerx"},
                                       container=dead_panel,
                                       text="Due to starvation", manager=game.manager,
                                       object_id=ObjectID("@label", "#small_dead_label"))

        UILabel(relative_rect=(-73,20,-1,-1),container=small_dead_panel,anchors={"centerx":"centerx"},
                             text=f"Days lived: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(0,20,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"{game.achievement.days_lived}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(-43,60,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"Total Money made: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(90,60,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"${round(game.achievement.money_made,2)}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(-40,100,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"Total Money spent: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(90,100,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"${round(game.achievement.money_spent,2)}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(-50,140,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"Total Taxes paid: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(70,140,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"${round(game.achievement.taxes_paid,2)}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(-40,180,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"Total Jobs worked: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(70,180,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"{game.achievement.jobs_had}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(-30,220,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"Max Level obtained: ",manager=game.manager,object_id=ObjectID("@label","#achievement_label"))
        UILabel(relative_rect=(100,220,-1,-1), anchors={"centerx":"centerx"},container=small_dead_panel,
                             text=f"LVL {game.achievement.level}",manager=game.manager,object_id=ObjectID("@label","#achievement_value"))



        UILabel(relative_rect=(0, 430, -1, -1), anchors={"centerx": "centerx"}, container=dead_panel,
                                   text="-TESTIMONIAL-", manager=game.manager,
                                   object_id=ObjectID("@label", "#testimonial_label"))



        game.player.is_dead = True
        game.player.die()

        return True


def tax_player(game):
    if game.player.money < 200:
        if game.player.deposit < 200:
            return
        else:
            taxable_income = round(((game.player.deposit * game.economy.tax_rate)/5),2)
            game.player.deposit -= taxable_income
            game.achievement.money_spent += taxable_income
            game.achievement.taxes_paid += taxable_income
            PopupPanel.show_message(manager=game.manager,
                                    text=f"It's tax time, ${taxable_income} has been taken away from you.",
                                    screen_size=game.screen.get_size(),positive=False)

    else:
        taxable_income = round(((game.player.money * game.economy.tax_rate) / 5), 2)
        game.player.money -= taxable_income
        game.achievement.money_spent += taxable_income
        game.achievement.taxes_paid += taxable_income
        PopupPanel.show_message(manager=game.manager,
                                text=f"It's tax time, ${taxable_income} has been taken away from you.",
                                screen_size=game.screen.get_size(),positive=False)