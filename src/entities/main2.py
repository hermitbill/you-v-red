import pygame
import math
import sys

from main import WorkerBee
from state import WorkerAi
from world import ScrollSystem


class SpawnEvent:
    def __init__(
        self,
        trigger,
        enemy_type,
        # start_pos,
        formation,
        # movement,
        count,
        # spacing=40,
        fire_pattern=None,
    ):
        self.trigger = trigger
        self.enemy_type = enemy_type
        # self.start_pos = pygame.Vector2(start_pos)
        self.formation = formation
        # self.movement = movement
        self.count = count
        # self.spacing = spacing
        self.fire_pattern = fire_pattern
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

        # check once per loop???? or always check?
        # answer: use an order list

        if not event.triggered and self.scroll.distance >= event.trigger:
            self.execute(event)
            event.triggered = True
            self.index += 1

    def execute(self, event):
        formation = event.formation

        for i in range(event.count):
            spawn_pos = formation.get_position(i)
            movement_engine = formation.get_movement(i)

            enemy = WorkerBee(
                game=self.game,
                name=event.enemy_type,
                attack=5,
                pos=spawn_pos,
                color=(225, 0, 0),
                size=(20, 20),
                monsterai=WorkerAi(movement_engine=movement_engine),
            )

            self.game.entities.append(enemy)


class BaseMovement:
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

    # im getting is a movement mechanic

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
    def __init__(self, start_pos, spacing, speed):
        self.start_pos = start_pos
        self.spacing = spacing
        self.speed = speed
        self.direction = pygame.Vector2(0, 1)

    def get_position(self, index):
        return self.start_pos + self.direction * self.spacing * index

    def get_movement(self, index):
        return StraightDown(self.speed)


class StraightDown(BaseMovement):
    def __init__(self, speed):
        super().__init__()
        self.direction = pygame.Vector2(0, 1)
        self.speed = speed
        self.velocity = self.direction * self.speed

    def update(self, dt):
        super().update(dt)
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


events = [
    SpawnEvent(
        trigger=100,
        enemy_type="grunt",
        formation=DiagonalFormation(
            start_pos=(700, -100), spacing=60, angle_deg=135, speed=120
        ),
        count=5,
    ),
    SpawnEvent(
        trigger=50,
        enemy_type="grunt",
        formation=StraightDownFormation(start_pos=(300, -100), spacing=40, speed=120),
        count=1,
    ),
    SpawnEvent(
        trigger=30,
        enemy_type="grunt",
        formation=RotationCircleFormation(
            center=(700 // 2, -100),
            radius=100,
            count=5,
            rotation_speed=2,
            drift_velocity=(0, 45),
        ),
        count=5,
    ),
]


class Gametest:
    # mini test
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.display = pygame.Surface((300, 300))
        self.clock = pygame.time.Clock()
        self.running = True

        self.scroll = ScrollSystem(speed=60)
        self.entities = []
        self.game_level = StageTimeline(self, events, self.scroll)

    def run(self):
        while self.running:
            self.screen.fill((18, 18, 28))
            dt = self.clock.tick(60) / 1000.0

            self.scroll.update(dt)
            self.game_level.update()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for e in self.entities:
                e.update(dt)

            for e in self.entities:
                e.render(self.screen)

            # Debug scroll distance
            font = pygame.font.SysFont(None, 24)
            text = font.render(
                f"scroll distance: {int(self.scroll.distance)}", True, (200, 200, 200)
            )
            self.screen.blit(text, (10, 10))

            pygame.display.update()
            self.clock.tick(60)


Gametest().run()
