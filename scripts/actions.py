from pygame_gui.core import ObjectID
from scripts.utils import load_image
import pytweening
import pygame
from subclass.pop_up_panel import PopupPanel

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
            game.primary_action_label.set_text("Health check-up")


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

def set_panel_text(game):
    if game.in_drug_store:
        if game.player.job is None:
            game.primary_job_label.set_text("Work in the Medical field")
            game.secondary_job_label.set_text("Work in the Sales field")
        elif game.player.job.name != "Doctor" and game.player.job.name != "Salesman":
            game.primary_job_label.set_text("Work in the Medical field")
            game.secondary_job_label.set_text("Work in the Sales field")
        elif game.player.job.name == "Doctor":
            game.primary_job_label.set_text(f"Work as a Doctor")
            game.secondary_job_label.set_text("Work in the Sales field")
        elif game.player.job.name == "Salesman":
            game.primary_job_label.set_text("Work in the Medical field")
            game.secondary_job_label.set_text("Work as a Salesman")


    if game.in_burgershop:
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Culinary field")
            game.secondary_job_label.set_text("Work in the Cashier field")

        elif game.player.job.name != "Cook" and game.player.job.name != "Cashier":
            game.primary_job_label.set_text(f"Work in the Culinary field")
            game.secondary_job_label.set_text("Work in the Cashier field")
        elif game.player.job.name == "Cook":
            game.primary_job_label.set_text("Work as a Cook")
            game.secondary_job_label.set_text("Work in the Cashier field")
        elif game.player.job.name == "Cashier":
            game.primary_job_label.set_text("Work in the Culinary field")
            game.secondary_job_label.set_text("Work as a Cashier")
        game.primary_action_label.set_text("Order a Burger Meal")
        game.secondary_action_label.set_text("Order a Pizza")

    if game.in_office:
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Tech field")
            game.secondary_job_label.set_text("Work in the Reception field")
        elif game.player.job.name != "Programmer" and game.player.job.name != "Clerk":
            game.primary_job_label.set_text(f"Work in the Tech field")
            game.secondary_job_label.set_text("Work in the Reception field")
        elif game.player.job.name == "Programmer":
            game.primary_job_label.set_text("Work as a Programmer")
            game.secondary_job_label.set_text("Work in the Reception field")
        elif game.player.job.name == "Clerk":
            game.primary_job_label.set_text("Work in the Tech field")
            game.secondary_job_label.set_text("Work as a Clerk")
        game.primary_action_label.set_text("Change your name")

    if game.in_bank:
        if game.player.job is None:
            game.primary_job_label.set_text(f"Work in the Financial field")
        elif game.player.job.name != "Accountant":
            game.primary_job_label.set_text(f"Work in the Financial field")
        elif game.player.job.name == "Accountant":
            game.primary_job_label.set_text("Work as an Accountant")
        game.secondary_job_label.set_text("Deposit Money")
        game.primary_action_label.set_text("Withdraw Money")



def pause(game):
    if game.is_paused is True:
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

        game.pause_panel.visible = True
        game.pause_panel.slide_to((0, 0), duration=1.0, easing=pytweening.easeOutBack)
        game.pause_load_btn.visible = True
        game.pause_menu_btn.visible = True
        game.credit_head_label.visible = True
        game.credit_sub_1_label.visible = True
        game.credit_sub_2_label.visible = True
        game.credit_sub_3_label.visible = True

    else:
        game.pause_panel.visible = False
        game.pause_load_btn.visible = False
        game.pause_menu_btn.visible = False
        game.credit_head_label.visible = False
        game.credit_sub_1_label.visible = False
        game.credit_sub_2_label.visible = False
        game.credit_sub_3_label.visible = False


def exit_house(game):
    game.is_home = False
    game.location = "suburb"
    game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)


def exit_suburb(game):
    game.location = "town"
    game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)

def exit_town(game):
    game.location = "suburb"
    game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)

def enter_house(game):
    game.is_home = True
    game.location = "home"
    game.assets['location'] = load_image(f'{game.location}.png')

    game.load_map(game.location)

    circle_transition(game)

def circle_transition(game, duration=1000):
    center = (game.display_2.get_width() // 2, game.display_2.get_height() // 2)
    max_radius = int((game.display_2.get_width() ** 2 + game.display_2.get_height() ** 2) ** 0.5)
    start_time = pygame.time.get_ticks()
    while True:
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        progress = min(1, elapsed / duration)
        radius = int(progress * max_radius)

        # Draw game scene
        game.display.fill((0, 0, 0, 0))
        game.display_2.fill((159, 226, 255))
        game.display_2.blit(game.assets['location'], (0,0))
        game.tile_map.render(game.display, offset=(0, 0))
        # self.player.render(self.display, offset=(0, 0))
        game.display_2.blit(game.display, (0, 0))

        # Create transition mask
        mask = pygame.Surface(game.display_2.get_size(), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 255))
        pygame.draw.circle(mask, (0, 0, 0, 0), center, radius)



        game.display_2.blit(mask, (0, 0))

        # Draw to screen
        game.screen.blit(pygame.transform.scale(game.display_2, game.screen.get_size()), (0, 0))

        pygame.display.update()

        if progress >= 1:
            game.player.pos[0] = int(game.player.pos[0])
            game.player.pos[1] = int(game.player.pos[1])
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
        pass


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

def gain_interest(game):
    rate = 0.4
    principal = game.player.deposit
    day = game.player.day
    interest = round(float((principal * rate * day)/100),2)

    return interest


def advance_day(game):
    circle_transition(game)
    game.player.energy = 100.0
    game.player.day += 1
    if game.player.deposit > 0:
        interest = gain_interest(game)
        game.player.deposit += interest
        PopupPanel.show_message(manager=game.manager,text=f"You have gained a ${interest} interest on your deposit",screen_size=game.screen.get_size())


def end_life(game):
    if 0 < game.player.happiness <= 40:
        PopupPanel.show_message(
            manager=game.manager,
            text="You really need a health checkup!",
            screen_size=game.screen.get_size()
        )
        return False

    elif game.player.happiness == 0:
        return True


