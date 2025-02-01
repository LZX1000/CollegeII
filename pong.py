import pygame
import math
import ctypes

def main():
    class GamePlayer(pygame.sprite.Sprite):
        def __init__(
            self,
            type: str = "player",
            size: tuple[int, int] | None = (8, 80)
        ):
            super().__init__()

            if type == "player":
                pos = (internal_width - size[0], internal_height // 2)
            else:
                pos = (size[0], internal_height // 2)

            self.pos = pos
            self.size = size
            self.surface = pygame.Surface(self.size)
            self.surface.fill((255, 255, 255))
            self.rect = self.surface.get_rect()

        def update(
            self,
            display_surface: pygame.Surface
        ):
            # # Update positions
            self.rect.center = self.pos
            # # Render
            display_surface.blit(self.surface, self.rect)
        
        def debug(
            self,
            surface: pygame.Surface
        ):
            pygame.draw.rect(surface, (255, 0, 0), self.rect, 1)

    class Ball(pygame.sprite.Sprite):
        def __init__(
            self,
            size: tuple[int, int] = (8, 8),
        ):
            super().__init__()

            self.pos = (internal_width // 2, internal_height // 2)
            self.size = size
            self.speed = 100
            self.angle = 0
            self.surface = pygame.Surface(self.size)
            self.surface.fill((255, 255, 255))
            self.rect = self.surface.get_rect()

        def update(
            self,
            display_surface: pygame.Surface
        ):
            # # Update positions
            self.rect.center = self.pos
            # # Render
            display_surface.blit(self.surface, self.rect)

        def debug(
            self,
            surface: pygame.Surface
        ):
            pygame.draw.rect(surface, (0, 0, 255), self.rect)

    # Initialize
    pygame.init()
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()

    # Display
    # # Resolutions
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)
    # # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height)) # For rendering
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    player = GamePlayer()
    opponent = GamePlayer("opponent")
    ball = Ball()

    running = True
    debug_mode = False
    gamestate = "game"
    movement_speed = 100
    max_fps = 60
    dt = 0

    while running:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            running = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Special Binds
        if keys[pygame.K_LCTRL] and keys[pygame.K_SPACE]:
            if not space_pressed:
                space_pressed = True
                if debug_mode:
                    debug_mode = False
                else:
                    debug_mode = True
        else:
            space_pressed = False

        # Player Movement
        movement = None
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            movement = player.pos[1] - movement_speed * dt
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            movement = player.pos[1] + movement_speed * dt
        # Boundry Check
        if movement is not None:
            min_y = 0 + player.rect.height // 2
            max_y = internal_height - player.rect.height // 2
            player.pos = (player.pos[0], max(min_y, min(movement, max_y)))

        # Interal rendering
        internal_surface.fill((0, 0, 0))
        player.update(internal_surface)
        opponent.update(internal_surface)
        ball.update(internal_surface)

        if debug_mode:
            player.debug(internal_surface)
            opponent.debug(internal_surface)
            ball.debug(internal_surface)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()