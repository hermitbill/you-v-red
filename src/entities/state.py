import pygame
import math 
import random
 
class PhaseMachine():
    """
    Respesent phase 
    
    Handles
    """""""
        * selects the configuration base on hp ratio.

    """

    def __init__(self, level:dict):
        """
        Initiate Phase Configuration component.
        
        :param level: a dictionary of configuration dictionary.
        :type level: dict
        """

        self.owner: object = None
        self.level: dict = level
        self.currentPhase_key: dict = None


    def pick_phase(self) -> dict|None:
        """
        Pick the apropriate configuration.
        
        :return: a configuration dictionary 
        :rtype: dict
        """

        ratio = self.owner.life_stats.hp / self.owner.life_stats.max_hp 

        if self.currentPhase_key is not None:
            low, high  = self.level[self.currentPhase_key]['hp_ratio']
            if low <= ratio <= high:
                return None

        for key, phase in self.level.items():
            low, high = phase['hp_ratio']
            if low <= ratio <= high:
                self.currentPhase_key = key
                return phase

        return None 
    
class MonsterAi:
    """
    The engine that manages the boss components. 

    Handles
    """""""
        * apply instructions
        * updates components 
        * rendering 
    
    """

    def __init__(self, combat:object|None = None, movement_engine: object|None = None, pattern_engine: object|None = None):
        """
        Initiate the Monster Component Controller. 
        
        :param combat: Combat logic component.
        :param movement_engine: Movement logic component.
        :param pattern_engine: Bullet Pattern component. 
        """
        self.owner: object|None = None 
        self.combat=combat
        self.pattern = pattern_engine 
        self.movement_engine = movement_engine
        self.movement_pattern = None 

    def apply_phase(self, phase:dict) -> None:
        """
        Feed the data in the phase definition to the monster components.
        
        :param phase: a configuration dictionary 
        :type phase: dict
        """

        self.pattern.active_pattern.clear()
        for name, kwargs in phase['patterns']:
            func = getattr(self.pattern, name)
            self.pattern.add_pattern(func, **kwargs)

        movement_pattern = phase['movement']
        func = getattr(self.movement_engine, movement_pattern)
        self.movement_pattern = func

    def update(self, dt:float) -> None:
        """
        Runs the update function in the monsters components 
        
        :param dt: delta time
        :type dt: float

        returns
        """""""
        None

        """
        self.movement_pattern()
        self.movement_engine.update()
        self.pattern.execute_patterns(dt)
        self.combat.update()

    def render(self, surf:pygame.Surface) -> None:
        """
        Draw bullets on to screen.
        
        :param surf: he Pygame surface to draw onto
        :type surf: pygame.Surface
        """
        self.combat.render(surf)



class WorkerAi:
    """
    The engine that manages the boss components. 

    Handles
    """""""
        * apply instructions
        * updates components 
        * rendering 
    
    """

    def __init__(self, combat:object|None = None, movement_engine: object|None = None, pattern_engine: object|None = None):
        """
        Initiate the Monster Component Controller. 
        
        :param combat: Combat logic component.
        :param movement_engine: Movement logic component.
        :param pattern_engine: Bullet Pattern component. 
        """
        self.owner: object|None = None 
        self.combat=combat
        self.pattern = pattern_engine 
        self.movement_engine = movement_engine

        #TODO should I set owner??? NO entity does that 


    def update(self, dt:float) -> None:
        """
        Runs the update function in the monsters components 
        
        :param dt: delta time
        :type dt: float

        returns
        """""""
        None
        """

        if self.movement_engine:
            self.movement_engine.update(dt)

        if self.pattern and self.owner.is_visible():
            self.pattern.execute_patterns(dt)
        
        if self.combat:
            self.combat.update(dt)

    def render(self, surf:pygame.Surface) -> None:
        """
        Draw bullets on to screen.
        
        :param surf: he Pygame surface to draw onto
        :type surf: pygame.Surface
        """
        if self.combat:
            self.combat.render(surf)

class Movement:
    def __init__(self):
        """
        Initiates movement component
        """

        self.owner = None
        self.current_movement = None
        self.velocity = None
        self.start = pygame.Vector2(0,0)
        self.speed = 0.0

        self.movement = {
            'left_right': self.left_right
        }
        pass

    def left_right(self):
        right = 100
        left = -100

        if self.velocity is None or self.velocity == pygame.Vector2(0,0):
            self.velocity = pygame.Vector2(1,0)
            self.speed = 1

        self.start.x += self.velocity.x * self.speed

        if self.start.x >= right:
            self.start.x = right
            self.velocity.x *= -1

        if self.start.x <= left:
            self.start.x = left
            self.velocity.x *= -1
        
        return self.velocity # velocity 
    
    def stand_still(self):
        if self.owner.pos != pygame.Vector2(135, 50):
            self.owner.pos = pygame.Vector2(135, 50) # return to origin
            self.owner.life_stats.update() 

        self.velocity = pygame.Vector2(0,0)
        return  
    
    def update(self):

        self.owner.pos.x = self.owner.pos.x + self.velocity.x 
        self.owner.pos.y =   self.owner.pos.y + self.velocity.y

        self.owner.rect.topleft = self.owner.pos
        self.owner.pos = pygame.Vector2(self.owner.rect.topleft)


class PurpleBullet:
    def __init__(self):
        # draw bullet4
        self.size = (4, 4)
        self.radius = 6
        self.color = (190, 60, 255)
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        # bullet 
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, 1)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius//2, 0)
        pygame.draw.circle(self.image, (255, 255, 225), (self.radius, self.radius), self.radius//2, 1)
        
        self.id = 'purple'
        
class YellowBullet:
    def __init__(self):
        self.color = (251, 237, 104) # yellow 
        self.size = (12,12)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        #self.image.fill(0,0,0)
        rect = pygame.Rect(0,0, self.size[0], self.size[1])
        pygame.draw.rect(self.image, self.color, rect, 1)
        pygame.draw.circle(self.image, (255, 255, 255), (6, 6), 3)
        self.id = 'yellow'


class BlueBullet: # TODO
    def __init__(self):
        self.color = (55, 188, 255) #blue 
        # pygame.draw.ellipse(screen, "red", [225, 10, 50, 20], 2)
        pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, owner, design):
        super().__init__()
        self.owner = owner
        self.image = design.image
        self.id = design.id
        self.rect = self.image.get_rect()

        self.center = pygame.Vector2(0, 0)
        self.angle = 0.0
        self.speed = 0.0
        self.ring_radius = 0.0
        self.active = False

    def activate(self, center, angle, speed, radius):
        self.center = pygame.Vector2(center)
        self.angle = angle
        self.speed = speed
        self.ring_radius = radius
        self.active = True

    def update(self, dt):
        if not self.active:
            return

        self.ring_radius += self.speed * dt
        x = self.center.x + math.cos(self.angle) * self.ring_radius
        y = self.center.y + math.sin(self.angle) * self.ring_radius
        self.rect.center = (x, y)

        if not self.owner.screen.get_rect().colliderect(self.rect):
            self.active = False


class MonstersGun:
    def __init__(self):
        self.owner = None

    def update(self, dt):
        for b in self.owner.game.monster_bullets:
            if b.active:
                b.update(dt)

    def render(self, surf):
        if self.owner.game.transition_sys.active:
            for b in self.owner.game.monster_bullets:
                b.active = False 
            return
        
        for b in self.owner.game.monster_bullets:
            if b.active:
                surf.blit(b.image, b.rect) #special_flags=pygame.BLEND_RGBA_ADD)

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
    

class Transition:
    #?????? might be a function in boss 
    def __init__(self):
        self.owner = None 
        self.active = False 
        self.daig = 0 
        self.timer = random.uniform(1, 2)

    def start(self, owner:None):
        self.owner = owner 
        self.active = True
        self.daig = 0 
        self.owner.game.collision_on = False 
        self.owner.game.can_fire = False 
        pass

    def end(self):
        self.active = False
        self.owner.game.collision_on = True 
        self.owner.game.can_fire = True  
        pass 
    
    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.timer = random.uniform(2, 4)
            self.end()


class Helper:
    def __init__(self, enemy, game, offset, pattern=None, life=None):
        """
        offset: (dx, dy) relative to enemy.position
        """
        self.enemy = enemy #owner of the helper
        self.game = game
        self.offset = pygame.Vector2(offset)
        self.size = (20, 20)
        self.color = (255, 255, 255)
        self.active = False 
        self.is_dead = False #

        # The helper's own image and rect
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(0, 0)
        self.pattern = pattern 
        self.life_stats = life 

        if pattern:
            self.pattern.owner = self
            #self.stack = PatternInstance(self.pattern.directed, dict(n=1, speed=2, spread=45, spread_rate=0.5)) # rename TODO
            self.pattern.add_pattern(self.pattern.directed, **dict(n=1, speed=2, spread=45, spread_rate=0.5))

        if self.life_stats:
            self.life_stats.owner = self
            self.is_dead = self.life_stats.is_dead

    def update(self, dt):
        # LIFEBAR
        if self.active:
            self.life_stats.update()
            # self.stack = PatternInstance(self.pattern.directed, dict(n=1, speed=2, spread=45, spread_rate=0.5)) # rename TODO
            self.pattern.execute_patterns(dt)

        self.position = self.enemy.pos + self.offset
        self.rect.topleft = self.position

        if self.is_dead:
            self.enemy.helpers.remove(self)
            pass


    def render(self, surf):
        self.image.fill((0, 0, 0, 0))

        if self.active: # gets passed by the phase 
            self.life_stats.render(surf)
        
        if not self.is_dead:
            pygame.draw.rect(
                self.image,
                self.color,
                pygame.Rect(0, 0, self.size[0], self.size[1]),
                1
            ) # not puting your 
            
            surf.blit(self.image, self.position)
# -----------            
# Explosion 
# ------------
class Particle:
    def __init__(self, pos, vel, lifetime, size, color, drag=0.98):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(vel)
        self.lifetime = lifetime
        self.max_life = lifetime
        self.size = size
        self.color = color
        self.drag = drag

    def update(self, dt):
        self.vel *= self.drag
        self.vel.y += 200 * dt  # gravity
        self.pos += self.vel * dt
        self.lifetime -= dt

    def draw(self, surf, camera_offset):
        t = clamp(self.lifetime / self.max_life, 0, 1)
        alpha = int(255 * t)
        s = max(1, int(self.size * (0.6 + 0.4 * t)))
        surf_col = (*self.color, alpha)
        surf_rect = pygame.Surface((s, s), pygame.SRCALPHA)
        pygame.draw.rect(surf_rect, surf_col, (0, 0, s, s))
        surf.blit(surf_rect, (self.pos.x + camera_offset.x - s/2, self.pos.y + camera_offset.y - s/2))

# ----- Shard (larger rectangle fragment) -----

def clamp(v, a, b):
    return max(a, min(b, v))

class Shard:
    def __init__(self, rect, vel, ang_vel, lifetime, color):
        self.rect = pygame.Rect(rect)
        self.vel = pygame.Vector2(vel)
        self.angle = 0
        self.ang_vel = ang_vel
        self.lifetime = lifetime
        self.max_life = lifetime
        self.color = color

    def update(self, dt):
        self.vel.y += 300 * dt  # gravity
        self.rect.x += self.vel.x * dt
        self.rect.y += self.vel.y * dt
        self.angle += self.ang_vel * dt
        self.lifetime -= dt

    def draw(self, surf, camera_offset):
        t = clamp(self.lifetime / self.max_life, 0, 1)
        alpha = int(255 * t)
        # draw rotated rect to a surface
        s = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        col = (*self.color, alpha)
        pygame.draw.rect(s, col, (0, 0, self.rect.w, self.rect.h))
        rot = pygame.transform.rotate(s, math.degrees(self.angle))
        pos = (self.rect.centerx + camera_offset.x - rot.get_width()/2,
               self.rect.centery + camera_offset.y - rot.get_height()/2)
        surf.blit(rot, pos)

class Explosion:
    def __init__(self, origin_rect):
        cx, cy = origin_rect.center
        self.particles = []
        self.shards = []
        self.time = 0.0
        self.duration = 2.5  # when the effect is considered finished
        self.camera_shake = 0.0

        # spawn many small particles
        for _ in range(80):
            angle = random.random() * math.pi * 2
            speed = random.uniform(80, 420)
            vel = pygame.Vector2(math.cos(angle)*speed, math.sin(angle)*speed * 0.7 - random.uniform(0,80))
            lifetime = random.uniform(0.5, 1.6)
            size = random.uniform(2, 6)
            # color palette: hot metal
            color = (random.randint(200,255), random.randint(80,160), random.randint(20,60))
            self.particles.append(Particle((cx + random.uniform(-10,10), cy + random.uniform(-10,10)), vel, lifetime, size, color, drag=0.94))

        # shards: break the rect into a few fragments
        w, h = origin_rect.w, origin_rect.h
        # break into 6-10 shards
        pieces = random.randint(6, 10)
        for i in range(pieces):
            rw = random.randint(max(8, w//6), max(12, w//3))
            rh = random.randint(max(8, h//8), max(12, h//4))
            rx = cx + random.randint(-w//2, w//2) - rw//2
            ry = cy + random.randint(-h//2, h//2) - rh//2
            ang_vel = random.uniform(-6, 6)
            vel = pygame.Vector2(random.uniform(-180, 180), random.uniform(-280, -80))
            color = (120 + random.randint(-30,30), 120 + random.randint(-30,30), 140 + random.randint(-40,40))
            lifetime = random.uniform(1.0, 2.8)
            self.shards.append(Shard((rx, ry, rw, rh), vel, ang_vel, lifetime, color))

        self.finished = False

    def update(self, dt):
        self.time += dt
        self.camera_shake = max(0.0, 16.0 * (1.0 - (self.time / 0.15)))  # short strong shake at start
        for p in self.particles:
            p.update(dt)
        for s in self.shards:
            s.update(dt)
        # remove dead
        self.particles = [p for p in self.particles if p.lifetime > 0]
        self.shards = [s for s in self.shards if s.lifetime > 0]
        if self.time > self.duration and not self.particles and not self.shards:
            self.finished = True

    def draw(self, surf):
        # camera shake offset
        cam = pygame.Vector2(0, 0)
        if self.camera_shake > 0:
            cam.x = random.uniform(-1, 1) * self.camera_shake
            cam.y = random.uniform(-1, 1) * self.camera_shake

        # draw shards under particles for depth
        for s in self.shards:
            s.draw(surf, cam)
        for p in self.particles:
            p.draw(surf, cam)