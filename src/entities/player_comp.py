import pygame

DIRECTION_KEYS = {
    pygame.K_RIGHT: "right",
    pygame.K_LEFT: "left",
    pygame.K_DOWN: "down",
    pygame.K_UP: "up",
}


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

        # display borders
        bounds = self.owner.game.display.get_rect()

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