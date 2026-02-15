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

    def __init__(self, combat=object|None, movement_engine=object|None, pattern_engine=object|None):
        """
        Initiate the Monster Component Controller. 
        
        :param combat: Combat logic component.
        :param movement_engine: Movement logic component.
        :param pattern_engine: Bullet Pattern component. 
        """
        self.owner | object = None 
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

        self.movement ={
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

# TODO
class BlueBullet:
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

    def update(self):
        if not self.active:
            return

        self.ring_radius += self.speed
        x = self.center.x + math.cos(self.angle) * self.ring_radius
        y = self.center.y + math.sin(self.angle) * self.ring_radius
        self.rect.center = (x, y)

        if not self.owner.screen.get_rect().colliderect(self.rect):
            self.active = False


class MonstersGun:
    def __init__(self):
        self.owner = None

    def update(self):
        for b in self.owner.game.monster_bullets:
            if b.active:
                b.update()

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
    def directed(self, n, speed,
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

        pos = pygame.Vector2(self.owner.rect.center)
        player = self.owner.game.player.pos

        distance = player - pos
        angle = math.atan2(distance.y, distance.x)

        for i, bullet in enumerate(bullets):
            bullet.activate(
                center=pos,
                angle=angle,
                speed=speed - i,
                radius=0
            )    

class Transition:
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


    def render(self, surf):
    #     if not self.active:
    #         return 
        
    #     pos = self.owner.rect.midbottom
    #     font = pygame.font.SysFont(None, 20)
    #     text = str(self.daig)

    #     surf.blit(font.render(text, True, (255, 255, 255)), (pos[0], pos[1] + 10))
        pass

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
            
        

