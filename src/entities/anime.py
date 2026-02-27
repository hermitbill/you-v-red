# robot_explosion.py
# Plug-and-play demo: a robot represented by a rect that explodes / dies with animation.
# Controls:
#   SPACE or left mouse click -> trigger explosion
#   R -> respawn robot
#   ESC or window close -> quit

import pygame
import random
import math
from pygame.math import Vector2

WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 20)

# ----- Helpers -----
def clamp(v, a, b):
    return max(a, min(b, v))

# ----- Explosion particle -----
class Particle:
    def __init__(self, pos, vel, lifetime, size, color, drag=0.98):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
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
class Shard:
    def __init__(self, rect, vel, ang_vel, lifetime, color):
        self.rect = pygame.Rect(rect)
        self.vel = Vector2(vel)
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

# ----- Robot entity -----
class Robot:
    def __init__(self, x, y, w=80, h=110):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.color = (50, 180, 240)
        self.alive = True
        self.flash_timer = 0.0

    def hit(self):
        self.alive = False

    def update(self, dt):
        if self.flash_timer > 0:
            self.flash_timer -= dt

    def draw(self, surf, camera_offset):
        # flash if recently hit (not used here but left for extension)
        col = self.color
        if not self.alive and int(pygame.time.get_ticks() / 80) % 2 == 0:
            col = (255, 100, 100)
        pygame.draw.rect(surf, col, self.rect.move(camera_offset.x, camera_offset.y), border_radius=6)
        # face / eyes
        eye_w, eye_h = 12, 10
        eye_y = self.rect.top + 28 + camera_offset.y
        left_eye_x = self.rect.left + 18 + camera_offset.x
        right_eye_x = self.rect.right - 18 - eye_w + camera_offset.x
        eye_surf = pygame.Surface((eye_w, eye_h), pygame.SRCALPHA)
        pygame.draw.rect(eye_surf, (20, 20, 20), (0, 0, eye_w, eye_h))
        surf.blit(eye_surf, (left_eye_x, eye_y))
        surf.blit(eye_surf, (right_eye_x, eye_y))
        # antenna
        pygame.draw.line(surf, (120,120,120), (self.rect.centerx + camera_offset.x, self.rect.top - 8 + camera_offset.y),
                         (self.rect.centerx + camera_offset.x, self.rect.top - 28 + camera_offset.y), 4)
        pygame.draw.circle(surf, (255,200,0), (self.rect.centerx + camera_offset.x, self.rect.top - 34 + camera_offset.y), 6)

# ----- Explosion controller -----
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
            vel = Vector2(math.cos(angle)*speed, math.sin(angle)*speed * 0.7 - random.uniform(0,80))
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
            vel = Vector2(random.uniform(-180, 180), random.uniform(-280, -80))
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
        cam = Vector2(0, 0)
        if self.camera_shake > 0:
            cam.x = random.uniform(-1, 1) * self.camera_shake
            cam.y = random.uniform(-1, 1) * self.camera_shake

        # draw shards under particles for depth
        for s in self.shards:
            s.draw(surf, cam)
        for p in self.particles:
            p.draw(surf, cam)

# ----- Main demo -----
def main():
    robot = Robot(WIDTH//2, HEIGHT//2, 80, 110)
    explosion = None
    camera_offset = Vector2(0, 0)
    running = True
    respawn_cooldown = 0.0

    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if robot.alive:
                        robot.hit()
                        explosion = Explosion(robot.rect)
                        respawn_cooldown = 0.6
                    # if not alive, pressing space does nothing
                elif event.key == pygame.K_r:
                    # respawn
                    robot = Robot(WIDTH//2, HEIGHT//2, 80, 110)
                    explosion = None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    if robot.rect.collidepoint(mx, my) and robot.alive:
                        robot.hit()
                        explosion = Explosion(robot.rect)
                        respawn_cooldown = 0.6

        # update
        robot.update(dt)
        if explosion:
            explosion.update(dt)
            if explosion.finished:
                explosion = None

        # camera offset lerp to create subtle shake while explosion exists
        if explosion and explosion.camera_shake > 0:
            camera_offset.x = random.uniform(-explosion.camera_shake, explosion.camera_shake)
            camera_offset.y = random.uniform(-explosion.camera_shake, explosion.camera_shake)
        else:
            # smoothly return camera to zero
            camera_offset *= 0.8

        # if robot dead but explosion finished, keep robot invisible; allow respawn after cooldown
        if not robot.alive:
            respawn_cooldown -= dt
            if respawn_cooldown <= 0 and explosion is None:
                # auto respawn after short time (optional)
                pass

        # draw
        screen.fill((18, 18, 20))
        # ground shadow / floor
        pygame.draw.rect(screen, (28,28,30), (0, HEIGHT - 80, WIDTH, 80))

        # draw robot or debris
        if robot.alive:
            robot.draw(screen, camera_offset)
        else:
            # small residual flicker rectangle to hint the corpse before fully gone
            if not explosion:
                # draw a faint burnt base
                burnt = pygame.Surface((robot.rect.w, robot.rect.h), pygame.SRCALPHA)
                burnt.fill((40, 40, 40, 160))
                screen.blit(burnt, (robot.rect.x + camera_offset.x, robot.rect.y + camera_offset.y))

        # draw explosion effects on top
        if explosion:
            explosion.draw(screen)

        # HUD
        hud = FONT.render("Left-click on robot or press SPACE to explode. R to respawn. ESC to quit.", True, (220,220,220))
        screen.blit(hud, (14, 12))
        if not robot.alive:
            t = FONT.render("ROBOT: DOWN", True, (220, 120, 120))
            screen.blit(t, (14, 36))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()

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
                        
                        if e.name == "grunt":
                            self.screenshake = max(10, self.screenshake)
                            e.life_stats.take_damage(b.damage)
                            e.flash_state = True
                        b.active = False
                        b.collided()
                        #break

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

        self.entities = [e for e in self.entities if not (e.is_dead and e.exploded)]