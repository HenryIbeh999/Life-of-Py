class SmoothProgressBar:
    def __init__(self, bar, speed=0.5):
        self.bar = bar
        self.current = bar.current_progress
        self.target = bar.current_progress
        self.speed = speed

    def set_value(self, value):
        """Set a new target percentage (0.0–1.0)."""
        self.target = max(0.0, min(100.0, value))

    def update(self, dt):
        """Ease toward target smoothly."""
        diff = self.target - self.current
        if abs(diff) < 0.001:
            return
        self.current += diff * min(1, dt * self.speed * 10)
        self.bar.set_current_progress(self.current)
