import pygame 
import math, random
from typing import Tuple

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

    def render(self, surf):
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