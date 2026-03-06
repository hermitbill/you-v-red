import math
import pygame 

class PatternInstance:
    def __init__(self, func, kwargs):
        self.func = func
        self.kwargs = kwargs
        self.cooldown = 0.0

    def update(self, dt):
        self.cooldown += dt
        self.func(dt=dt, _pattern=self, **self.kwargs)

class PatternEngine:
    def __init__(self):
        self.owner = None
        self.active_pattern = []

    def add_pattern(self, pattern_func, **kwargs):
        self.active_pattern.append(PatternInstance(pattern_func, kwargs))

    def execute_patterns(self, dt):
        if self.owner.game.transition_sys.active:
            return 
        
        for pattern in self.active_pattern:
            pattern.update(dt)

    # --------------------------------------------------
    # PATTERNS
    # --------------------------------------------------

    def ring(self, radius=20, n_bullets=12, speed=2,
             spread_rate=0.5, _pattern=None, **kwargs):

        if _pattern.cooldown < spread_rate:
            return
        
        # a reference to the pattern object 
        _pattern.cooldown = 0.0

        bullets = [b for b in self.owner.game.monster_bullets if not b.active][:n_bullets]
        if not bullets:
            return

        cx, cy = self.owner.rect.center

        for i, bullet in enumerate(bullets):
            angle = (2 * math.pi / n_bullets) * i
            bullet.activate(
                center=(cx, cy),
                angle=angle,
                speed=speed,
                radius=radius
            )

    def spray(self, angle_deg, n, spread, speed,
              spread_rate=0.3, _pattern=None, **kwargs):
        #angle_deg is the direction 

        if _pattern.cooldown < spread_rate:
            return

        _pattern.cooldown = 0.0

        bullets = [b for b in self.owner.game.monster_bullets if not b.active][:n]
        if not bullets:
            return

        cx, cy = self.owner.rect.center
        start = angle_deg - spread / 2

        for i, bullet in enumerate(bullets):
            angle = math.radians(start + i * (spread / max(1, n - 1)))
            bullet.activate(
                center=(cx, cy),
                angle=angle,
                speed=speed,
                radius=0
            )

    def stack(self, angle_deg, n, speed,
              spread_rate=0.4, _pattern=None, **kwargs):

        if _pattern.cooldown < spread_rate:
            return

        _pattern.cooldown = 0.0

        bullets = [
            b for b in self.owner.game.monster_bullets
            if not b.active and b.id == 'yellow'
        ][:n]

        if not bullets:
            return

        cx, cy = self.owner.rect.center
        angle = math.radians(angle_deg)

        for i, bullet in enumerate(bullets):
            bullet.activate(
                center=(cx, cy),
                angle=angle,
                speed=speed - i,
                radius=0
            )

    # TODO !!!
    def directed(self,
             n,
             speed,
             spread=20,          # optional cone spread
             spread_rate=0.4,
             _pattern=None,
             **kwargs):

        if _pattern.cooldown < spread_rate:
            return

        _pattern.cooldown = 0.0

        bullets = [
            b for b in self.owner.game.monster_bullets
            if not b.active and b.id == 'yellow'
        ][:n]

        if not bullets:
            return

        # Snapshot position once (important!)
        shooter_pos = pygame.Vector2(self.owner.rect.center)
        player_pos = pygame.Vector2(self.owner.game.player.pos)

        # Compute base direction once
        base_angle = math.atan2(
            player_pos.y - shooter_pos.y,
            player_pos.x - shooter_pos.x
        )

        spread_rad = math.radians(spread)

        for i, bullet in enumerate(bullets):

            # Optional small spread cone
            if n > 1:
                offset = (i - (n - 1) / 2) * (spread_rad / max(1, n - 1))
            else:
                offset = 0

            final_angle = base_angle + offset

            bullet.activate(
                center=shooter_pos,
                angle=final_angle,
                speed=speed,
                radius=0
            )
    def spiral(self,
           angle_deg,
           n,
           spread,
           speed,
           rotation_speed=120,   # degrees per second
           spread_rate=0.3,
           _pattern=None,
           **kwargs):
        """
        Spiral pattern:
        Continuously rotates the firing direction over time.
        """

        if _pattern.cooldown < spread_rate:
            return

        _pattern.cooldown = 0.0

        # --- initialize spiral state ---
        if not hasattr(_pattern, "phase"):
            _pattern.phase = 0.0

        # rotate over time (frame independent)
        _pattern.phase += math.radians(rotation_speed) * spread_rate

        bullets = [
            b for b in self.owner.game.monster_bullets
            if not b.active
        ][:n]

        if not bullets:
            return

        cx, cy = self.owner.rect.center

        # apply rotation to base angle
        base_angle = math.radians(angle_deg) + _pattern.phase
        start = base_angle - math.radians(spread) / 2

        for i, bullet in enumerate(bullets):
            if n > 1:
                angle = start + i * (math.radians(spread) / (n - 1))
            else:
                angle = base_angle

            bullet.activate(
                center=(cx, cy),
                angle=angle,
                speed=speed,
                radius=0
            )