import pygame
import math

from components.pattern import PatternEngine
from entities.entity import WorkerBee, Life
from entities.enemy_comp import WorkerAi, MonstersGun

class SpawnEvent:
    def __init__(
        self,
        trigger,
        enemy_type,
        formation,
        count,
        patterns=None,
    ):
        self.trigger = trigger
        self.enemy_type = enemy_type
        self.formation = formation
        self.count = count
        self.patterns = patterns or [] #TODO 
        self.triggered = False


class StageTimeline:
    """
    Plays the events
    """

    def __init__(self, game, events, scroll: object):
        self.game = game
        self.events = sorted(events, key=lambda e: e.trigger)
        self.scroll = scroll
        self.current_event = None
        self.index = 0  # pointer to next event

    def update(self):
        if self.index >= len(self.events):
            return

        event = self.events[self.index]

        if not event.triggered and self.scroll.distance >= event.trigger:
            self.execute(event)
            event.triggered = True
            self.index += 1

    def execute(self, event):
        formation = event.formation
        
        for i in range(event.count):
            spawn_pos = formation.get_position(i)
            movement_engine = formation.get_movement(i)
            pattern_engine = PatternEngine()
            
            
            for pattern_name, kwargs in event.patterns:
                pattern_func = getattr(pattern_engine, pattern_name)
                pattern_engine.add_pattern(pattern_func, **kwargs)

            #combat = MonstersGun()

            ai = WorkerAi(movement_engine=movement_engine, pattern_engine=pattern_engine)

            enemy = WorkerBee(
                game=self.game,
                name=event.enemy_type,
                attack=5,
                pos=spawn_pos,
                color=(225, 0, 0),
                size=(10, 10),
                life_stats=Life(hp=10),
                monsterai=ai
            )

            self.game.entities.append(enemy)


class BaseMovement:
    """
    represents entities movement formation link.
    """
    def __init__(self):
        self.owner = None
        self.time = 0

    def update(self, dt: float):
        self.time += dt


class DiagonalFormation:
    def __init__(self, start_pos, angle_deg, spacing, speed):
        self.start_pos = start_pos
        self.angle = math.radians(angle_deg)
        self.spacing = spacing
        self.speed = speed

        self.direction = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

    def get_position(self, index):
        return self.start_pos + self.direction * self.spacing * index

    def get_movement(self, index):
        return DiagonalMovement(self.angle, self.speed)


# move to movement engine
class DiagonalMovement(BaseMovement):
    """
    Diagonal movement component
    """
    def __init__(self, angle_deg: int, speed: float):
        super().__init__()

        self.angle = angle_deg
        self.speed = speed

        self.direction = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

        self.velocity = self.direction * speed

    def update(self, dt):
        if self.owner:
            self.owner.pos += self.velocity * dt


class StraightDownFormation:
    def __init__(self, start_pos, stop_y, spacing, speed):
        self.start_pos = start_pos
        self.spacing = spacing
        self.speed = speed
        self.direction = pygame.Vector2(0, 1)

        self.stop_y = stop_y

    def get_position(self, index):
        return self.start_pos + self.direction * self.spacing * index

    def get_movement(self, index):
        return StraightDown(self.speed, self.stop_y)


class StraightDown(BaseMovement):
    def __init__(self, speed, stop_y=None):
        super().__init__()
        self.direction = pygame.Vector2(0, 1)
        self.speed = speed
        self.velocity = self.direction * self.speed

        self.stop_y = stop_y

    def update(self, dt):
        super().update(dt)

        if self.stop_y is not None and self.owner.pos.y >= self.stop_y:
            return 
         
        self.owner.pos += self.velocity * dt

class RotationCircleFormation:
    def __init__(self, center, radius, count, rotation_speed, drift_velocity=(0, 0)):
        self.center = pygame.Vector2(center)
        self.radius = radius
        self.count = count

        self.rotation_speed = rotation_speed
        self.current_rotation = 0

        self.drift_velocity = drift_velocity
        self.angle_step = (math.pi * 2) / self.count

    def get_position(self, index):
        angle = self.angle_step * index
        x = self.center.x + self.radius * math.cos(angle)
        y = self.center.y + self.radius * math.sin(angle)
        return pygame.Vector2(x, y)

    def get_movement(self, index):
        return RotatingCircle(
            self.center,
            self.radius,
            index,
            self.count,
            self.rotation_speed,
            self.drift_velocity,
        )


class RotatingCircle(BaseMovement):
    def __init__(
        self, center, radius, index, count, rotation_speed, drift_velocity=(0, 0)
    ):
        super().__init__()

        self.center = pygame.Vector2(center)
        self.radius = radius
        self.index = index
        self.count = count

        self.rotation_speed = rotation_speed
        self.current_rotation = 0

        self.drift_velocity = pygame.Vector2(drift_velocity)
        self.angle_step = (math.pi * 2) / self.count

    def update(self, dt):
        if not self.owner:
            return

        self.current_rotation += self.rotation_speed * dt
        self.center += self.drift_velocity * dt
        angle = self.angle_step * self.index + self.current_rotation

        x = self.center.x + self.radius * math.cos(angle)
        y = self.center.y + self.radius * math.sin(angle)

        self.owner.pos = pygame.Vector2(x, y)


