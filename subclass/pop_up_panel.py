import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UILabel
from pygame_gui.core import ObjectID
import math


class PopupPanel(UIPanel):
    """
    Bottom-right popup that overwrites existing one instead of stacking.
    Smooth slide-in, bounce, and fade-out animation.
    """

    active_popup: "PopupPanel" = None  # only one instance at a time

    def __init__(self, manager, text, screen_size,
                 duration=2000, fade_time=400,
                 width=500, height=80,
                 slide_speed=400):
        screen_w, screen_h = screen_size
        base_x = screen_w - width - 265
        base_y = screen_h - height - 20
        start_y = base_y + 100  # start slightly below screen for animation

        rect = pygame.Rect(base_x, start_y, width, height)

        super().__init__(
            relative_rect=rect,
            manager=manager,
            object_id=ObjectID(class_id="@panel", object_id="#popup_panel"),
            starting_height=5,
            visible=True
        )

        # Store properties
        self.manager = manager
        self.text = text
        self.duration = int(duration)
        self.fade_time = int(fade_time)
        self.elapsed_ms = 0
        self.alpha = 255

        self.slide_speed = slide_speed
        self.target_y = base_y
        self.bounce_offset = 10
        self.bounce_phase = 0
        self.is_bouncing = True


        # Label inside
        padding = 10
        self.label = UILabel(
            relative_rect=pygame.Rect(padding, padding, width - padding, height - padding),
            text=self.text,
            manager=manager,
            container=self,
            object_id=ObjectID(class_id="@label", object_id="#popup_label")
        )
        self.label.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

        # Kill previous popup if exists
        if PopupPanel.active_popup:
            PopupPanel.active_popup.kill()

        PopupPanel.active_popup = self

    @staticmethod
    def show_message(manager, text, screen_size, duration=4000, fade_time=400,positive= True):
        if positive:
            pygame.mixer.music.load('data/sfx/notice.wav')
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.load('data/sfx/negative_notice.mp3')
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play()
        """Shows or updates the popup with new text."""
        if PopupPanel.active_popup:
            popup = PopupPanel.active_popup
            popup.text = text
            popup.label.set_text(text)
            popup.elapsed_ms = 0
            popup.alpha = 255
            popup.image.set_alpha(255)
            popup.is_bouncing = True
            popup.bounce_phase = 0
            return popup
        else:
            return PopupPanel(manager=manager, text=text, screen_size=screen_size,
                              duration=duration, fade_time=fade_time)

    def update(self, time_delta: float):
        """Frame-based animation update."""
        super().update(time_delta)
        self.elapsed_ms += int(time_delta * 1000)
        time_left = self.duration - self.elapsed_ms

        # Slide animation
        current_y = self.rect.y
        dy = self.target_y - current_y
        if abs(dy) > 0.5:
            move = self.slide_speed * time_delta
            direction = 1 if dy > 0 else -1
            self.set_relative_position((self.rect.x, current_y + direction * min(abs(dy), move)))

        # Bounce easing
        if abs(dy) < 4 and self.is_bouncing:
            self.bounce_phase += time_delta * 6
            bounce = self.bounce_offset * math.exp(-3 * self.bounce_phase) * math.cos(12 * self.bounce_phase)
            self.set_relative_position((self.rect.x, self.target_y + bounce))
            if abs(bounce) < 0.5:
                self.is_bouncing = False

        # Fade out
        if time_left <= self.fade_time:
            fade_progress = (self.fade_time - max(0, time_left)) / max(1, self.fade_time)
            new_alpha = max(0, int(255 * (1.0 - fade_progress)))
            if new_alpha != self.alpha:
                self.alpha = new_alpha
                self.image.set_alpha(self.alpha)

        # End of life
        if self.elapsed_ms >= self.duration:
            self.kill_popup()

    def kill_popup(self):
        """Remove popup."""
        if PopupPanel.active_popup is self:
            PopupPanel.active_popup = None
        self.kill()
