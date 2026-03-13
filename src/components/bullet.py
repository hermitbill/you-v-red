import math, random
import pygame
from typing import List 

from components.visual import Spark

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

class BlueBullet:
    def __init__(self):
        # draw bullet4
        self.size = (4, 4)
        self.radius = 6
        self.color = (55, 188, 255)
        self.image = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))

        # bullet 
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, 1)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius//2, 0)
        pygame.draw.circle(self.image, (255, 255, 225), (self.radius, self.radius), self.radius//2, 1)
        
        self.id = 'blue'


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

        self.ring_radius += self.speed
        x = self.center.x + math.cos(self.angle) * self.ring_radius
        y = self.center.y + math.sin(self.angle) * self.ring_radius
        self.rect.center = (x, y)

        # wall
        if not self.owner.screen.get_rect().colliderect(self.rect):
            self.active = False

    def render(self, surf):
        surf.blit(self.image, self.rect)

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
            # store previous position b4 moving
            self.prev_pos = self.pos.copy()

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

    
    def check_collision(self, target) -> bool:
        if not self.active:
            return False
        
        start = self.prev_pos
        end = self.pos

        return target.rect.clipline(start, end) != () 
    

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
