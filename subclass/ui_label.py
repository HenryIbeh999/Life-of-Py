import pygame

class MoneyAnimator:
    def __init__(self, label, base_color=(0, 0, 0)):
        self.label = label
        self.base_color = pygame.Color(*base_color)
        self.pulse_color = pygame.Color(0, 255, 0)
        self.current_value = 0
        self.target_value = 0
        self.animation_time = 0.5  # duration of number animation
        self.elapsed = 0
        self.active = False

        # Pulse animation
        self.pulsing = False
        self.pulse_timer = 0.0
        self.pulse_duration = 0.6  # total pulse time (seconds)

    def set_target(self, new_value):
        """Trigger numeric + pulse animation automatically."""
        if new_value == self.target_value:
            return

        # Set pulse color automatically
        if new_value > self.target_value:
            self.pulse_color = pygame.Color(0, 200, 0)  # gain: green
        else:
            self.pulse_color = pygame.Color(200, 0, 0)  # loss: red

        # Prepare number tween
        self.current_value = self.target_value
        self.target_value = new_value
        self.elapsed = 0
        self.active = True

        # Start pulse
        self.pulsing = True
        self.pulse_timer = 0.0

    def update(self, dt):
        """Call every frame with dt = clock.tick(60)/1000."""
        # Smooth numeric tween
        if self.active:
            self.elapsed += dt
            t = min(self.elapsed / self.animation_time, 1.0)
            interpolated = self.current_value + (self.target_value - self.current_value) * t
            self.label.set_text(f"${round(float(interpolated),2)}")

            if t >= 1.0:
                self.active = False
                self.current_value = self.target_value

        # Smooth color pulse animation (no time module)
        if self.pulsing:
            self.pulse_timer += dt
            t = self.pulse_timer / self.pulse_duration

            if t <= 0.5:
                lerp = t / 0.5  # fade to pulse color
            else:
                lerp = 1.0 - (t - 0.5) / 0.5  # fade back to base color

            r = int(self.base_color.r + (self.pulse_color.r - self.base_color.r) * max(0, min(lerp, 1)))
            g = int(self.base_color.g + (self.pulse_color.g - self.base_color.g) * max(0, min(lerp, 1)))
            b = int(self.base_color.b + (self.pulse_color.b - self.base_color.b) * max(0, min(lerp, 1)))
            self.label.text_colour = pygame.Color(r, g, b)
            self.label.rebuild()

            if self.pulse_timer >= self.pulse_duration:
                self.pulsing = False
                self.label.text_colour = self.base_color
                self.label.rebuild()
