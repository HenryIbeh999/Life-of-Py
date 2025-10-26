from pygame_gui.elements import UIPanel
from subclass.tweening import *

class AnimatedPanel(UIPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.anim_x = None
        self.anim_y = None
        self.anim_alpha = None

    def slide_to(self, new_pos, duration=1.0, easing=pytweening.easeOutCubic):
        start_x, start_y = self.rect.topleft
        end_x, end_y = new_pos
        self.anim_x = TweenAnimation(start_x, end_x, duration, easing)
        self.anim_y = TweenAnimation(start_y, end_y, duration, easing)

    def fade_to(self, target_alpha, duration=1.0, easing=pytweening.easeOutQuad):
        start_alpha = self.image.get_alpha() or 255
        self.anim_alpha = TweenAnimation(start_alpha, target_alpha, duration, easing)

    def update(self, time_delta):
        super().update(time_delta)

        if self.anim_x and not self.anim_x.finished:
            x = self.anim_x.update(time_delta)
            y = self.anim_y.update(time_delta)
            self.set_relative_position((x, y))

        if self.anim_alpha and not self.anim_alpha.finished:
            alpha = self.anim_alpha.update(time_delta)
            self.set_alpha(alpha)
