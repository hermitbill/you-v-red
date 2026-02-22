import pygame
import sys
import random
import math
from typing import List, Tuple

from state import * 
from level_build import *

DIRECTION_KEYS = {
    pygame.K_RIGHT: "right",
    pygame.K_LEFT: "left",
    pygame.K_DOWN: "down",
    pygame.K_UP: "up",
}

class Gun:
    """
    Represent a gun.

    Handles bullet activation
    """

    def __init__(self):
        self.owner = None

    def fire(self) -> None:
        """
        "fires" your gun.

        Handles
        """""""
        * initates a bullet
        * activates the bullet
        * adds bullet to bullet pool
        * plays animation
        """

        bullet = BulletAK(self.owner)
        bullet.activate()
        self.owner.game.bullets.append(bullet)
        self.owner.on_fire()


class BulletAK:
    """
    Represents a single bullet with a AK-47 style effect fired by a weapon.

    Handles
    """""""
        * movement logic
        * particle effect
        * collision
        * rendering

    .. note::
        Bullets is inactive until ``activate()`` is called
    """

    def __init__(self, owner: object):
        """
        Initialize an inactive bullet.

        :param owner: the weapon attached to an entity that fired the bullet.

        .. note::
            owner object must have a game object
        """
        self.owner = owner
        self.game = owner.game

        # Physical Properties
        self.pos = pygame.Vector2(0, 0)
        self.size = (1, 1)
        self.speed = 18
        self.velocity = pygame.Vector2(0, -1)
        self.active = False
        self.length = 25
        self.damage = 5

        # Rendering State
        self.color = (250, 250, 250)
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        # Particle Management
        self.bullet_effect: List[object] = []
        self.collision_effect: List[object] = []

    def activate(self) -> None:
        """
        Initializes the bullet's starting position with a slight random spread.

        :returns: None
        """
        spread = random.uniform(-2, 2)
        self.pos = pygame.Vector2(
            self.game.player.rect.centerx + spread, self.game.player.rect.top
        )
        self.rect.center = self.pos
        self.active = True

        # Visual-only spark effects
        for _ in range(3):
            angle = -math.pi / 2  # Upward direction
            spread = random.uniform(-0.4, 0.4)
            speed = random.uniform(1, 2)
            self.bullet_effect.append(
                Spark(self.pos, angle + spread, speed, (255, 255, 255))
            )

    def update(self) -> None:
        """
        Updates physics and cleans up expired particle effects.

        :returns: None
        """
        if not self.active:
            pass
        else:
        # Advance position based on velocity
            self.pos += self.velocity * self.speed
            self.rect.center = self.pos

        # Update and prune effects
        for e in self.bullet_effect.copy():
            kill = e.update()
            if kill:
                self.bullet_effect.remove(e)

        for c in self.collision_effect.copy():
            kill = c.update()
            if kill:
                self.collision_effect.remove(c)

    def collided(self) -> None:
        """
        Visual effect for bullet collision.

        :returns: None
        """
        pos = pygame.Vector2(self.pos)
        for _ in range(5):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 3)
            self.collision_effect.append(Spark(pos, angle, speed, (255, 255, 255)))

    def render(self, surf: pygame.Surface) -> None:
        """
        Draws the bullet trail and associated particles to the screen.

        :param surf: The Pygame surface to draw onto.
        :returns: None
        """
        if self.active:
            # Draw bullet as a line to simulate high-speed motion blur
            end_pos = self.pos - self.velocity * self.length
            pygame.draw.line(surf, self.color, self.pos, end_pos, 1)

        for s in self.bullet_effect:
            s.render(surf)

        for c in self.collision_effect:
            c.render(surf)


class Spark:
    """
    Represents a particle used for collision and firing animation.

    Handles
    """""""
    * movement logic
    * renderinig
    """

    def __init__(
        self,
        pos: pygame.Vector2,
        angle: float,
        speed: float,
        color: Tuple[int, int, int],
    ):
        """
        Initiate particle object.

        :param pos: particle position.
        :param angle: direction of the particle.
        :param speed: the linear velocity i.e the lenght the particle will travel.
        :param color: the color of the particle
        """
        
        # Physical Properties
        self.pos = pygame.math.Vector2(pos)
        self.angle = angle
        self.speed = speed
        self.color = color

    def update(self) -> None:
        """
        Updates physics and cleans up expired particle effects.

        :returns: None
        """

        # Advance position based on velocity
        self.pos.x += math.cos(self.angle) * self.speed
        self.pos.y += math.sin(self.angle) * self.speed

        # Update particle by reducing the linear velocity
        self.speed -= 0.1
        return self.speed <= 0

    def render(self, surf: pygame.Surface) -> None:
        """

        Draw the particle to screen.

        :param surf: The Pygame surface to draw onto.
        :type surf: pygame.Surface
        :returns: None
        """
        end = (
            self.pos.x + math.cos(self.angle) * self.speed * 2,
            self.pos.y + math.sin(self.angle) * self.speed * 2,
        )
        pygame.draw.line(surf, self.color, self.pos, end, 1)


class BloodParticles:
    """
    Represents a blood particle when player get hit.

    Handles
    """""""
        * movement logic
        * renderinig
    """

    def __init__(
        self,
        pos: pygame.Vector2,
        angle: float,
        speed: float,
        color: Tuple[int, int, int],
    ):
        # Physical Properties
        self.pos = pygame.Vector2(pos)
        self.angle = angle
        self.speed = speed
        self.life = random.randint(8, 15)

        # Rendering State
        self.color = color
        self.stuck = False

    def update(self) -> None:
        """
        Updates physics and cleans up expired particle effects.

        :returns: None
        """

        # Advance position based on velocity
        if not self.stuck:
            self.pos.x += math.cos(self.angle) * self.speed
            self.pos.y += math.sin(self.angle) * self.speed

            self.life -= 1
            if self.life <= 0:
                self.stuck = True
                self.speed = 0

    def render(self, surf: pygame.Surface) -> None:
        """
        Draw the particle to screen.

        :param surf: The Pygame surface to draw onto.
        :returns: None
        """

        if self.stuck:
            pygame.draw.circle(surf, self.color, self.pos, 1)
        else:
            end = (
                self.pos.x + math.cos(self.angle) * self.speed,
                self.pos.y + math.sin(self.angle) * self.speed,
            )
            pygame.draw.line(surf, self.color, self.pos, end, 1)


class Life:
    """

    Represents the health stats of an entity.

    Handles
    ^^^^^^^
        * damage intake
        * current health stats management
        * death state

    ..note::
        ``Life`` is the metadata of the entity while
        ``Lifebar`` is the visual representation of that metadata
    """

    def __init__(self, hp: float):
        """
        Initializes the health stats of an entity in order to be managed.

        :param hp: the hit points of the entity
        """
        self.owner = None
        self.hp = hp
        self.max_hp = self.hp
        self.is_dead = False

        # Visual representation
        self.life_bar = Lifebar(self)

    def take_damage(self, amount: float) -> None:
        """
        Docstring for take_damage

        :param self: Description
        :param amount: Description
        """
        if self.is_dead:
            return

        self.hp -= amount

    def update(self) -> None:
        """
        Update entity's hit point data.

        :returns: None
        """

        if self.hp <= 0:
            self.is_dead = True
            self.owner.is_dead = self.is_dead

        # Update visual representation
        self.life_bar.update()
        pass

    def render(self, surf: pygame.Surface) -> None:
        """
        Draw visual respresentation of the entity's hit bar.

        :param surf: The Pygame surface to draw onto.
        :returns: None
        """
        if not self.is_dead:
            self.life_bar.render(surf)


class Lifebar:
    """
    The visual representation of an entities hit bar.

    Handles
    ^^^^^^^
        * update visual respresentation
        * rendering
    """

    def __init__(self, owner: object):
        """
        Docstring for __init__

        :param self: Description
        :param owner: the enity

        ..note::
            owner object is attached.
        """

        # Physical Properties
        self.owner = owner
        self.hp = self.owner.hp
        self.max_hp = self.owner.max_hp
        self.pos = pygame.Vector2(0, 0)
        self.life_pos = pygame.Vector2(0, 0)

        # Visual Properties
        self.color = (68, 195, 68)  # green
        self.bg_color = (211, 211, 211)  # gray

    def update(self) -> None:
        """
        Update hit bar visual representation in accordance to
        the entity's hit points.

        :returns: None
        """

        # Re-labeling for readablility
        self.entity = self.owner.owner

        x = self.entity.rect.x
        y = self.entity.rect.y - 10

        self.life_pos = pygame.Vector2(x, y)

        self.hp = self.owner.hp
        self.max_hp = self.owner.max_hp

    def render(self, surf: pygame.Surface) -> None:
        """
        Draw hit bar object.

        :param surf: pygame.Surface
        :returns: None
        """
        width = self.entity.rect.width
        ratio = self.hp / self.max_hp
        current_width = width * ratio
        height = 4

        # Visual hit bar background
        bg_rect = pygame.Rect(self.life_pos.x, self.life_pos.y, width, height)
        pygame.draw.rect(surf, self.bg_color, bg_rect)

        # Main visual hit bar
        hp_rect = pygame.Rect(self.life_pos.x, self.life_pos.y, current_width, height)
        pygame.draw.rect(surf, self.color, hp_rect)


class PlayerLifebar:
    """
    Represents players Hit bar

    Handles
    ^^^^^^^
        * damage intake
        * current health stats management
        * death state
    """

    def __init__(self, bars: int):
        """
        Initiates Players Hit bar

        :param bars: the visual representation of the player hit points
        :type bars: int
        """
        # Physical representation
        self.owner: object = None
        self.hp = bars
        self.max_hp = self.hp
        self.is_dead = False

        # Visual representation
        self.size = (8, 12)
        self.color = (52, 174, 10)

        # Hit point Management
        self.total_health = []
        self.add_health_bars()

    def add_health_bars(self) -> None:
        """
        Rectangle objects that represent individual hit points.

        :returns: None
        """
        for _ in range(self.hp):
            rect = pygame.Rect(0, 0, *self.size)
            self.total_health.append(rect)

    def take_damage(self) -> None:
        """
        Reduces hit bar.

        :returns: None
        """
        if self.is_dead:
            return

        self.total_health.pop()
        self.hp -= 1

    def update(self):
        """
        Update players hit point data.

        :returns: None
        """
        if self.is_dead:
            return

        if self.hp <= 0:
            self.is_dead = True
            self.owner.is_dead = self.is_dead

    def render(self, surf: pygame.Surface):
        """
        Draws player hit bar.

        :param surf: The Pygame surface to draw onto.
        :returns: None
        """
        if self.is_dead:
            return

        # Hit bar placement
        for i in range(self.hp):
            if i == 0:
                self.total_health[i].topleft = (10, 10)
            else:
                self.total_health[i].topleft = (
                    self.total_health[i - 1].x + 12,
                    self.total_health[i - 1].y,
                )

        for rect in self.total_health:
            pygame.draw.rect(surf, self.color, rect, 0)
        pass


class PlayerMovement:
    """
    Players movement component

    Handles
    ^^^^^^^
        * directional input data
        * updates player movement
    """

    def __init__(self):
        """
        Initiates movement component
        """

        # Physical representation
        self.owner: object = None
        self.speed = 2
        self.velocity = pygame.Vector2(0, 0)

        self.keys = {"right": False, "left": False, "down": False, "up": False}

    def handle_input(self, event: pygame.event) -> None:
        """
        Handles manual dirctional key inputs

        :param event: pygame event input.
        :returns: None
        """
        if event.type not in (pygame.KEYDOWN, pygame.KEYUP):
            return

        is_down = event.type == pygame.KEYDOWN

        for key, label in DIRECTION_KEYS.items():
            if event.key == key:
                self.keys[label] = is_down

    def has_any_direction(self) -> None:
        """
        Checks if any directional keys have changed.

        :returns: bool
        """
        return any(self.keys.values())

    def update(self) -> None:
        """
        Updates player position and collision with stage.

        :returns: None
        """

        if not self.has_any_direction:
            return

        # Game platform
        bounds = self.owner.game.platform.rect

        dx = self.keys["right"] - self.keys["left"]
        dy = self.keys["down"] - self.keys["up"]

        direction = pygame.Vector2(dx, dy)
        if direction.length_squared() > 0:
            direction.normalize_ip()

        self.velocity = direction * self.speed
        self.owner.pos += self.velocity

        # collision check
        self.owner.rect.center = self.owner.pos
        self.owner.rect.clamp_ip(bounds)
        self.owner.pos = self.owner.rect.center


class Entity:
    """
    Entity Interface.
    Entities are players and monsters.

    Handles
    ^^^^^^^
    * individual components
    * updating components
    * rendering components
    """

    def __init__(
        self,
        game: object,
        name: str,
        attack: int,
        pos: List,
        color: Tuple[int, int, int],
        size: Tuple,
        combat: object | None = None,
        life_stats: object | None = None,
    ):
        """
        Initiate Entity 
        
        :param game: The main game engine instance.
        :param name: The name of the entity.
        :param attack: Base attack power.
        :param pos: Initial (x, y) coordinates.
        :param color: RGB color tuple.
        :param size: Width and height tuple.
        :param combat: Combat logic component.
        :param life_stats: HP and status component.
        """
        # Physical representation 
        self.game = game
        self.name = name
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.attack = attack
        self.is_dead = False
        self.death_particles = []
        self.bullets_group = None

        # Visual representation
        self.original_color = color
        self.color = self.original_color

        # Hit flashes 
        self.flash_state = False
        self.flash_color = (195, 100, 100)
        self.flash_timer = 5
        self.flash_toggle_timer = 0

        # Combat component
        self.combat = combat
        if self.combat:
            self.combat.owner = self

        # Hit bar component 
        self.life_stats = life_stats
        if self.life_stats:
            self.life_stats.owner = self
            self.is_dead = self.life_stats.is_dead

    def on_fire(self) -> None:
        """
        Firing animation
        resets firing animation variable 

        :returns: None
        """
        self.squash = 1.0

    def kill(self): #TODO ...
        # particle
        self.velocity = pygame.Vector2(0, 0)
        pass

    def update(self, dt) -> None:
        """
        Udate individual components and flash animation
        
        :param dt: Delta time (time passed since last frame).
        :returns: None 
        """

        if self.life_stats:
            self.life_stats.update()

        if self.flash_state:
            self.color = self.flash_color
            self.flash_timer -= 1

        if self.flash_timer <= 0:
            self.flash_state = False
            self.color = self.original_color
            self.flash_timer = 5

    def render(self, surf: pygame.Surface) -> None:
        """
        Draw Entity on to screen.
        
        :param surf: The Pygame surface to draw onto.
        :returns: None
        """

        if self.is_dead:
            return

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(self.color)

        surf.blit(self.image, self.rect)


class Player(Entity):
    """
    The controllable Player entity. 
    
    The player extends :class:``Entity`` with:
        * Movement control
        * Squash/stretch animation feedback
        * Blood particle effects on hit
        * A smaller collision box in reference to bullet hell style
    
    ..note::
        The player owns its movement component and visual effects, but
        core combat and life handling are inherited from ``Entity``.
    """
    def __init__(
        self,
        game : object,
        name: str,
        attack: int,
        pos: tuple,
        color: Tuple[int, int, int],
        size: tuple,
        combat: object | None = None,
        life_stats: object | None =None,
        movement: object | None = None,
    ):
        """
        :param game: The main game engine instance.
        :param name: Name of the player.
        :param attack: Base attack power.
        :param pos: Initial (x, y) coordinates.
        :param color: RGB color tuple.
        :param size: Width and height tuple.
        :param combat: Combat logic component.
        :param life_stats: HP and status component.
        :param movement: Movement logic component.
        """
        super().__init__(game, name, attack, pos, color, size, combat, life_stats)

        self.movement = movement
        self.blood_effect = [] 

        # Collision setup: Box is 60% of the visual size
        self.collision = (self.size[0] * 0.6, self.size[1] * 0.6)
        self.collision_rect = pygame.Rect(0, 0, *self.collision)
        self.collision_rect.center = self.pos

        self.rect = pygame.Rect(0, 0, *self.size)
        self.rect.midbottom = self.collision_rect.midbottom

        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

        # Squash/stretch animation variables when shooting
        self.squash = 0.0
        self.squash_return_speed = 8.0
        self.max_squash = 0.35

        # movement component
        if self.movement:
            self.movement.owner = self

    def spawn_blood(self) -> None:
        """
        Creates a burst of red particles at the player's position.
        :returns: None 
        """
        for _ in range(6):
            angle = random.uniform(0, math.pi * 2)
            speed = 1  # random.uniform(1,2)
            spawn_pos = pygame.Vector2(self.pos) + pygame.Vector2(0, -5)  # in front
            self.blood_effect.append(
                BloodParticles(spawn_pos, angle, speed, (174, 31, 17))
            )

    def update(self, dt: float) -> None:
        """
        Updates player physics, animations, and particle effects.

        :param dt: Delta time (time passed since last frame).
        :returns: None
        """
        super().update(dt)

        if self.is_dead:
            self.game.game_over()
            return

        # Recover from squash/stretch deformation
        if self.squash > 0.0:
            self.squash -= self.squash_return_speed * dt
    
            if self.squash < 0.0:
                self.squash = 0.0

        if self.movement:
            self.movement.update()

        self.collision_rect.center = self.pos

        # Update and clean up blood particles
        for b in self.blood_effect.copy():
            b.update()

    def render(self, surf: pygame.Surface) -> None:
        """
        Draws the player.

        :param surf: The surface to draw the player onto.
        :returns: None
        """
        self.life_stats.render(surf)

        for b in self.blood_effect.copy():
            b.render(surf)

        super().render(surf)

        if self.life_stats:
            self.life_stats.render(surf)

        # Apply squash & stretch: wider when shorter, thinner when taller
        squash_amt = self.squash * self.max_squash 
        height_scale = 1.0 - squash_amt
        width_scale = 1.0 + squash_amt

        new_w = int(self.size[0] * width_scale)
        new_h = int(self.size[1] * height_scale)

        # Ensure the player's 'feet' stay on the ground during squash
        self.rect.size = (new_w, new_h)
        self.rect.midbottom = self.collision_rect.midbottom


class WorkerBee(Entity):
    """
    An enemy entity controlled by an optional phase machine.

    Monsters can trigger phase transitions and manage 'Helper' sub monsters
    that provide additional fire support.

    ..note::
        :ivar phase 
        :vartype phase: Dict 
        phase is a dictionary of instructions read from `level_build.py`. Its optional but 
        then you would have to manual insert movement, helper and combat instrustions.
        Monster would still render without components.    
    """
    def __init__(
        self,
        game: object,
        name: str,
        attack: int,
        pos: tuple,
        color: Tuple[int,int,int],
        size: tuple,
        combat: object | None = None,
        life_stats: object | None = None,
        ability: object | None = None,
        monsterai: object | None = None,
    ):
        """
        Docstring for __init__
        
        :param game: The main game engine instance.
        :param name: Name of the Monster.
        :param attack: Base attack power
        :param pos: Initial (x, y) coordinates.
        :param color: RGB color tuple.
        :param size: Width and height tuple.
        :param combat: Combat logic component.
        :param life_stats: HP and status component.
        :param monsterai: component that reads, edits and implement the phase machine.
        """
        super().__init__(game, name, attack, pos, color, size, combat, life_stats)

        self.ability = ability
        self.monster_ai = monsterai

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        # =========================
        # Safe Owner Wiring
        # =========================

        def safe_set_owner(component):
            if component is not None:
                component.owner = self

        # Direct components
        safe_set_owner(self.ability)
        safe_set_owner(self.monster_ai)

        # Nested AI components (safe even if missing)
        if self.monster_ai is not None:
            safe_set_owner(getattr(self.monster_ai, "movement_engine", None))
            safe_set_owner(getattr(self.monster_ai, "pattern", None))
            safe_set_owner(getattr(self.monster_ai, "combat", None))

    def update(self, dt: float) -> None:
        """
        Updates monster components.

        :param dt: Delta time (time passed since last frame).
        :returns: None
        """
        super().update(dt)

        if self.is_dead:
            self.game.game_over()
            return

        # does allow #TODO undo
        #if self.game.transition_sys.active:
        #    return

        self.monster_ai.update(dt)
        self.rect.center = self.pos

    def render(self, surf: pygame.Surface) -> None:
        """
        Draws the monster.

        :param surf: The surface to draw the player onto.
        :returns: None
        """
        super().render(surf)

        if self.is_dead:
            return

        if self.life_stats:
            self.life_stats.render(surf)

        # if not self.is_dead:
        self.monster_ai.render(surf)



class Monster(Entity):
    """
    An enemy entity controlled by an optional phase machine.

    Monsters can trigger phase transitions and manage 'Helper' sub monsters
    that provide additional fire support.

    ..note::
        :ivar phase 
        :vartype phase: Dict 
        phase is a dictionary of instructions read from `level_build.py`. Its optional but 
        then you would have to manual insert movement, helper and combat instrustions.
        Monster would still render without components.    
    """
    def __init__(
        self,
        game: object,
        name: str,
        attack: int,
        pos: tuple,
        color: Tuple[int,int,int],
        size: tuple,
        combat: object | None = None,
        life_stats: object | None = None,
        ability: object | None = None,
        phase_machine: object | None = None,
        monsterai: object | None = None,
    ):
        """
        Docstring for __init__
        
        :param game: The main game engine instance.
        :param name: Name of the Monster.
        :param attack: Base attack power
        :param pos: Initial (x, y) coordinates.
        :param color: RGB color tuple.
        :param size: Width and height tuple.
        :param combat: Combat logic component.
        :param life_stats: HP and status component.
        :param phase_machine: Dictionary filled with instruction on what state the component should be.
        :param monsterai: component that reads, edits and implement the phase machine.
        """
        super().__init__(game, name, attack, pos, color, size, combat, life_stats)

        self.ability = ability
        self.phase_machine = phase_machine
        self.monster_ai = monsterai
        self.phase = None
        self.helpers = []
        self.helpers_active = False

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        # components
        if ability:
            self.ability.owner = self

        # Phase machine component 
        if self.phase_machine:
            self.phase_machine.owner = self

        # Monster AI component 
        if self.monster_ai:
            self.monster_ai.owner = self
            self.monster_ai.movement_engine.owner = self

            if self.monster_ai.pattern is not None:
                self.monster_ai.pattern.owner = self
            if self.monster_ai.combat:
                self.monster_ai.combat.owner = self

        # Entity's Helper Components
        # TODO place this into the Helper object so you just call the Helper objects 
        
        # Physical placement 
        w, h = self.size
        left_offset = pygame.Vector2(-10 - 20, 0) 
        right_offset = pygame.Vector2(w + 10, 0)

        self.left_helper = Helper(
            self, self.game, left_offset, pattern=PatternEngine(), life=Life(10)
        )
        self.right_helper = Helper(
            self, self.game, right_offset, pattern=PatternEngine(), life=Life(10)
        )

        # Helper management 
        self.helpers.extend([self.left_helper, self.right_helper])

    def update(self, dt: float) -> None:
        """
        Updates monster components.

        :param dt: Delta time (time passed since last frame).
        :returns: None
        """
        super().update(dt)

        if self.is_dead:
            self.game.game_over()
            return

        # does allow
        if self.game.transition_sys.active:
            return

        # change phase
        phase_event = self.phase_machine.pick_phase()

        if phase_event is not None:
            self.game.transition_sys.start(self)
            phase_dict = phase_event
            self.monster_ai.apply_phase(phase_dict)

            # activate helpers
            self.helpers_active = phase_event["helper"]
            self.left_helper.active = phase_event["helper"]
            self.right_helper.active = phase_event["helper"]

        self.monster_ai.update(dt)

        # ---- helper entity ------
        if len(self.helpers) != 0:
            for h in self.helpers:
                h.update(dt)
        else:
            self.helpers_active = False

    def render(self, surf: pygame.Surface) -> None:
        """
        Draws the monster.

        :param surf: The surface to draw the player onto.
        :returns: None
        """
        super().render(surf)

        if self.is_dead:
            return

        if self.life_stats and not self.helpers_active:
            self.life_stats.render(surf)

        for h in self.helpers:
            h.render(surf)

        # if not self.is_dead:
        self.monster_ai.render(surf)


class Platform:
    """
    The area the player can move in. 
    """
    def __init__(self):
        """
        Initiate platform.
        """
        #Physical respresentation 
        self.size = (260, 100)
        self.image = pygame.Surface(self.size)
        self.pos = pygame.Vector2(20, 150)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.color = (82, 82, 82)

    def render(self, surf: pygame.Surface) -> None:
        """
        Draw platform to surface.
        
        :param surf: The Pygame surface to draw onto.
        :returns: None
        """
        self.image.fill(self.color)
        surf.blit(self.image, (20, 150))


class Game:
    """
    Main Game engine 

    Handles
    """"""" 
    * main game loop 
    * collision dectection systems 
    * bullet pooling
    * event handling 
    """
    def __init__(self):
        """
        Initializes Pygame, creates display surfaces and pool bullets 
        and populate entites.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.display = pygame.Surface((300, 300))
        self.clock = pygame.time.Clock()
        self.running = True
        self.screenshake = 0

        # System States 
        self.transition_sys = Transition()
        self.collision_on = True
        self.can_fire = True
        self.game_state = True

        # Entity Tracking 
        self.bullets = []  # Active player bullets
        self.entities = []  # Collidable participants 

        # Bullet Pooling
        # pre-allocate 1000 bullets 
        self.monster_bullets = pygame.sprite.Group() 
        for _ in range(500):
            self.monster_bullets.add(Bullet(self, design=PurpleBullet()))
        for _ in range(500):
            self.monster_bullets.add(Bullet(self, design=YellowBullet()))

        # Object initialization
        self.platform = Platform()
        self.player = Player(
            self,
            "player",
            10,
            [150, 225],
            (255, 255, 255),
            (6, 10),
            combat=Gun(),
            movement=PlayerMovement(),
            life_stats=PlayerLifebar(5),
        )
        self.enemy = Monster(
            self,
            "boss",
            5,
            [135, 50],
            (195, 0, 0),
            (30, 30),
            life_stats=Life(hp=150),
            phase_machine=PhaseMachine(level=level),
            monsterai=MonsterAi(MonstersGun(), Movement(), PatternEngine()),
        )
        self.entities.extend([self.player, self.enemy])

    def collisionSystem(self) -> None:
        """
        process all object interactions for the current frame. 

        Checks
        """"""
        * monster bullet vs player collision.
        * player bullet vs screen boundaries.
        * player bullet vs Monster and Helpers collision.

        ..note::
            This method also removes bullets from the active list and marks them for reuse.
        """
        screen_rect = self.screen.get_rect()
        if self.collision_on:
            
            # monster bullet vs player collision.
            for b in self.monster_bullets:
                if b.active and b.rect.colliderect(self.player.collision_rect):
                    self.player.life_stats.take_damage()
                    self.player.spawn_blood()
                    b.active = False
                    continue

            for b in self.bullets:
                if not b.active:
                    continue
                
                # Check screen boundaries
                if not screen_rect.colliderect(b.rect):
                    b.active = False
                    b.collided()
                    continue

                for e in self.entities:
                    if e.is_dead:
                        continue

                    if b.rect.colliderect(e.rect):
                        # Damge the boss only if helpers are down
                        if e.name == "boss" and not e.helpers_active:
                            self.screenshake = max(10, self.screenshake)
                            e.life_stats.take_damage(b.damage)
                            e.flash_state = True
                        b.active = False
                        b.collided()
                        break
                    
                    # Check Boss Helpers
                    if hasattr(e, "helpers_active"):
                        if e.helpers_active:
                            for h in e.helpers.copy():
                                if b.rect.colliderect(h.rect):
                                    self.screenshake = max(10, self.screenshake)
                                    h.life_stats.take_damage(b.damage)
                                    b.active = False
                                    b.collided()
                            break
        
        # Keep active bullets
        self.bullets = [
            b for b in self.bullets if b.active or b.bullet_effect or b.collision_effect
        ]

    def game_over(self) -> None:
        """
        Trigger Game Over state.
        
        :returns: None
        """
        self.font = pygame.font.SysFont(None, 20)
        self.display.fill((0, 0, 0))

        self.collision_on = False
        self.can_fire = False
        self.game_state = False

        for e in self.entities:
            e.kill()

        self.monster_bullets.empty()

        self.screen.blit(
            self.font.render("Game Over", False, (255, 255, 255)), (100, 100)
        )
        pygame.display.update()

    def run(self) -> None:
        """
        The main game loop.
        
        Handles
        """""""
        * input logic 
        * update logic
        * rending
        * screenshake
        
        :param self: Description
        """
        while self.running:
            self.display.fill((18, 18, 28))
            dt = self.clock.tick(60) / 1000.0

            # Delay screenshake over time
            self.screenshake = max(0, self.screenshake - 1)

            # Event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.combat.fire()

                self.player.movement.handle_input(event)

            # Logic Updates 
            self.enemy.update(dt)
            self.player.update(dt)
            self.transition_sys.update(dt)

            for b in self.bullets.copy():
                b.update()

            self.collisionSystem()

            # Rendering
            self.platform.render(self.display)
            self.player.render(self.display)
            self.enemy.render(self.display)

            for b in self.bullets.copy():
                b.render(self.display)


            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2,
            )
            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()),
                screenshake_offset,
            )
            pygame.display.update()
            self.clock.tick(60)

# Initiate Game 
if __name__ == "__main__":
    Game().run()
