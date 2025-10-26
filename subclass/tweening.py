import pygame
import pytweening
from pygame_gui.elements import UIPanel


class TweenAnimation:
    def __init__(self, start_value, end_value, duration, easing_func=pytweening.easeOutQuad):
        self.start_value = start_value
        self.end_value = end_value
        self.duration = duration
        self.easing_func = easing_func
        self.elapsed = 0.0
        self.finished = False

    def update(self, time_delta):
        if self.finished:
            return self.end_value

        self.elapsed += time_delta
        t = min(self.elapsed / self.duration, 1.0)
        eased_t = self.easing_func(t)
        value = self.start_value + (self.end_value - self.start_value) * eased_t

        if t >= 1.0:
            self.finished = True
        return value
