import pygame
import sys
import random

# world comp 
from components.world import * 

#configurations 
from config.boss_config import *
from config.level_config import * 

# visual 
from components.visual import * 

# entity
from entities.player_comp import *
from entities.entity import *
from entities.enemy_comp import * 
from components.bullet import *
from  components.level_eng import * 


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

        #Scroll system & Level
        self.explosions = []
        self.scroll = ScrollSystem(speed=60)
        self.game_level = StageTimeline(self, EVENTS, self.scroll)

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
        # self.platform = Platform()
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
        
        self.entities.extend([self.player]) # self.enemy

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
            for b in (b for b in self.monster_bullets if b.active):
                if b.rect.colliderect(self.player.collision_rect):
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

                    hit = False

                    # Check Boss Helpers
                    if hasattr(e, "helpers_active") and e.helpers_active:
                        for help in e.helpers.copy():
                            if b.rect.colliderect(help.rect):
                                self.screenshake = max(10, self.screenshake)
                                help.life_stats.take_damage(b.damage)
                                hit = True
                                break

                        if hit:
                            b.active = False
                            b.collided()
                            break #stop checking other enemies 

                    
                    if e.name == "grunt" and b.check_collision(e):
                        self.screenshake = max(10, self.screenshake)
                        e.life_stats.take_damage(b.damage)
                        e.flash_state = True
                        hit = True
                       
                    # Damge the boss only if helpers are down
                    elif e.name == "boss" and not e.helpers_active and b.check_collision(e):
                            self.screenshake = max(10, self.screenshake)
                            e.life_stats.take_damage(b.damage)
                            e.flash_state = True
                            hit = True

                    if hit:
                        b.active = False
                        b.collided()
                        break
                    

    def game_over(self) -> None:
        """
        Trigger Game Over state.
        
        :returns: None
        """
        # self.font = pygame.font.SysFont(None, 20)
        # self.display.fill((0, 0, 0))

        #self.collision_on = False
        #self.can_fire = False
        #self.game_state = False

        # for e in self.entities:
        #     e.kill()

        #self.monster_bullets.empty()

        # self.screen.blit(
        #     self.font.render("Game Over", False, (255, 255, 255)), (100, 100)
        # )
        # pygame.display.update()

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
            dt = self.clock.tick(50) / 1000.0

            # UPDATE OBJECTS 
            #################
            self.active_mons_bullet =  [b for b in self.monster_bullets if b.active] #NOTE
            self.bullets = [b for b in self.bullets if b.active or b.bullet_effect or b.collision_effect]
            self.entities = [e for e in self.entities if not (e.is_dead and e.exploded)]
            self.explosions = [exp for exp in self.explosions if not exp.finished]
            ###################

            # Delay screenshake over time
            self.screenshake = max(0, self.screenshake - 1)
            
            self.scroll.update(dt)
            self.game_level.update()

            # Event handling 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.player.combat.fire()

                self.player.movement.handle_input(event)

            for e in self.entities:
                e.update(dt)

            for exp in self.explosions:
                exp.update(dt)

            # self.transition_sys.update(dt) # TODO Enemy uses transition

            for b in self.bullets:
                b.update()

            for b in self.active_mons_bullet:
                b.update(dt) #dt

            self.collisionSystem() #maybe get the list as input TODO?

            # RENDERING 
            for e in self.entities:  
                e.render(self.display)

            for exp in self.explosions:
                exp.draw(self.display) #TODO render rename

            for b in self.active_mons_bullet:
                b.render(self.display) #dt

            for b in self.bullets:
                b.render(self.display)

            # Debug scroll distance
            font = pygame.font.SysFont(None, 12)
            text = font.render(
                f"scroll distance: {int(self.scroll.distance)}", False, (200, 200, 200), (0,0,0)
            )
            self.display.blit(text, (210, 290))

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
