import time

from pygame_gui.core import ObjectID
from pygame_gui.elements import UILabel

from scripts.utils import load_image
import pytweening
import pygame
from subclass.pop_up_panel import PopupPanel
from scripts.economy import *
from scripts.jobs import load_jobs

def show_action(game, primary_action_type, secondary_action_type):
    if game.is_action_panel is True:
        game.action_panel.visible = True
        game.action_panel.slide_to((0, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.ui_action_image.visible = True
        game.small_action_panel.visible = True
        game.small_action_panel.slide_to((0, -167), duration=1.0, easing=pytweening.easeOutBack)
        game.primary_job_button.visible = True
        game.primary_job_label.visible = True
        game.secondary_job_button.visible = True
        game.secondary_job_label.visible = True
        game.primary_action_button.visible = True
        game.primary_action_label.visible = True
        game.rate_btn.disable()



        if primary_action_type == "doctor" and secondary_action_type == "salesman":
            game.ui_action_image.set_image(load_image("ui/ui_doctor.png"))

            game.primary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#job_doctor_button"))
            game.primary_action_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#action_doctor_button"))
            game.secondary_job_button.change_object_id(
                ObjectID(class_id="@ui_button", object_id=f"#job_salesman_button"))
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
            game.secondary_action_button.visible = True
            game.secondary_action_label.visible = True
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
            game.secondary_action_button.visible = False
            game.secondary_action_label.visible = False
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

            game.secondary_action_button.visible = False
            game.secondary_action_label.visible = False
            game.in_drug_store = False
            game.in_burgershop = False
            game.in_office = False
            game.in_bank = True
            set_panel_text(game)
    else:
        game.action_panel.visible = False
        game.small_action_panel.visible = False
        game.ui_action_image.visible = False
        game.primary_job_button.visible = False
        game.primary_job_label.visible = False
        game.secondary_job_button.visible = False
        game.secondary_job_label.visible = False
        game.primary_action_button.visible = False
        game.primary_action_label.visible = False
        game.secondary_action_button.visible = False
        game.secondary_action_label.visible = False
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
        game.assets_sfx['ambience'].stop()
        game.assets_sfx['pause'].play(-1)
        game.is_action_panel = False
        game.action_panel.visible = False
        game.small_action_panel.visible = False
        game.ui_action_image.visible = False
        game.primary_job_button.visible = False
        game.primary_job_label.visible = False
        game.secondary_job_button.visible = False
        game.secondary_job_label.visible = False
        game.primary_action_button.visible = False
        game.primary_action_label.visible = False
        game.secondary_action_button.visible = False
        game.secondary_action_label.visible = False
        game.change_name_panel.visible = False
        game.change_name_prompt.visible = False
        game.change_name_cancel_btn.visible = False
        game.is_rate_panel = False
        game.chart_panel.visible = False
        game.chart_image.visible = False
        game.chart_cancel_btn.visible = False
        game.rate_btn.disable()


        game.pause_panel.visible = True
        game.pause_panel.slide_to((0, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.pause_load_btn.visible = True
        game.pause_menu_btn.visible = True
        game.credit_head_label.visible = True
        game.credit_sub_1_label.visible = True
        game.credit_sub_2_label.visible = True
        game.credit_sub_3_label.visible = True

    else:
        game.clickable = True
        game.assets_sfx['pause'].stop()
        game.assets_sfx['ambience'].play(-1)
        game.pause_panel.visible = False
        game.pause_load_btn.visible = False
        game.pause_menu_btn.visible = False
        game.credit_head_label.visible = False
        game.credit_sub_1_label.visible = False
        game.credit_sub_2_label.visible = False
        game.credit_sub_3_label.visible = False
        game.rate_btn.enable()



def exit_house(game):
    game.is_home = False
    game.location = "suburb"
    if game.player.energy <= 30:
        game.assets['location'] = load_image(f'night_{game.location}.jpg')
    else:
        game.assets['location'] = load_image(f'{game.location}.png')


    game.load_map(game.location)

    circle_transition(game)


def exit_suburb(game):
    game.location = "town"
    if game.player.energy <= 30:
        game.assets['location'] = load_image(f'night_{game.location}.jpg')
    else:
        game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)

def exit_town(game):
    game.location = "suburb"
    if game.player.energy <= 30:
        game.assets['location'] = load_image(f'night_{game.location}.jpg')
    else:
        game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)

def change_location(game,location):
    game.location = location
    if location == "home":
        game.is_home = True
    game.assets['location'] = load_image(f'{game.location}.png')
    game.load_map(game.location)

    circle_transition(game)


def check_time(game):
    if game.player.energy <= 30:
        game.is_night = True
        if game.is_night:
            if game.location == 'home':
                game.assets['location'] = load_image(f'night_{game.location}.png')
            else:
                game.assets['location'] = load_image(f'night_{game.location}.jpg')

    elif game.player.energy > 30:
        game.is_night = False
        game.assets['location'] = load_image(f'{game.location}.png')

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
        game.change_name_panel.visible = True
        game.change_name_cancel_btn.visible = True
        game.change_name_prompt.visible = True
        game.change_name_continue_btn.visible = True
        game.primary_action_button.visible = False
        game.primary_action_label.visible = False
        game.change_name_panel.slide_to((0, 50), duration=1.0, easing=pytweening.easeOutBack)
    else:
        game.clickable = True


def set_transaction_type(game):
    if game.in_bank:
        game.bank_panel.visible = True
        game.bank_panel.slide_to((0, 50), duration=1.0, easing=pytweening.easeOutBack)
        game.bank_type_label.visible = True
        game.bank_prompt.visible = True
        game.bank_cancel_btn.visible = True
        game.bank_continue_btn.visible = True
        game.min_type_label.visible = True
        game.max_type_label.visible = True

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
    # game.player.energy = 100.0
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

    elif game.player.health == 0:

        dead_label = UILabel(relative_rect=(0,250,-1,-1), anchors={"center":"center"},
                             text="YOU ARE DEAD!!!",manager=game.manager,object_id=ObjectID("@label","#dead_label"),visible=False)
        small_dead_label = UILabel(relative_rect=(0,330,-1,-1), anchors={"center":"center"},
                             text="Try to be happy next time :)",manager=game.manager,object_id=ObjectID("@label","#small_dead_label"),visible=False)
        dead_label.visible = True
        small_dead_label.visible = True
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
            PopupPanel.show_message(manager=game.manager,
                                    text=f"It's tax time, ${taxable_income} has been taken away from you.",
                                    screen_size=game.screen.get_size(),positive=False)

    else:
        taxable_income = round(((game.player.money * game.economy.tax_rate) / 5), 2)
        game.player.money -= taxable_income
        PopupPanel.show_message(manager=game.manager,
                                text=f"It's tax time, ${taxable_income} has been taken away from you.",
                                screen_size=game.screen.get_size(),positive=False)