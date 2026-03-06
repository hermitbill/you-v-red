import pygame 
import math, random
from typing import List, Tuple

from components.visual import BloodParticles, Explosion
from components.pattern import PatternEngine
from entities.enemy_comp import Helper


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
        self.flash_timer = 2
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
            self.flash_timer -= dt

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
        #combat: object | None = None,
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
        super().__init__(game, name, attack, pos, color, size, life_stats=life_stats)

        self.ability = ability
        self.monster_ai = monsterai

        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=self.pos)

        self.exploded = False

        # Owner Wiring/ different approach
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
            #safe_set_owner(getattr(self.monster_ai, "combat", None))

    def is_visible(self):
        return self.game.display.get_rect().colliderect(self.rect)

    def update(self, dt: float) -> None:
        """
        Updates monster components.

        :param dt: Delta time (time passed since last frame).
        :returns: None
        """
        super().update(dt)

        if self.is_dead:
            #self.game.game_over() #TODO remove from list
            # play dead animation
            # self.game.entities.pop(entity)
            if not self.exploded:
                self.game.explosions.append(Explosion(self.rect))
                self.exploded = True
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

        # if not self.is_dead: TODO cause to render 
        # self.monster_ai.render(surf)



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

