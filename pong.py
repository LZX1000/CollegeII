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
            pos: tuple[int, int] | None = None,
            size: tuple[int, int] = (8, 8),
            speed: int | float = 100,
            angle: float | int = 0,
            max_bounce_angle: float = math.radians(45)
        ):
            super().__init__()
            if pos is None:
                self.pos = (internal_width // 2, internal_height // 2)
            else:
                self.pos = pos

            self.size = size
            self.speed = speed
            self.angle = angle
            self.max_bounce_angle = max_bounce_angle
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
            pygame.draw.rect(surface, (0, 0, 255), self.rect, 1)

    def check_movement(
        x: pygame.sprite.Sprite,
        movement: int
    ):
        min_y = 0 + x.rect.height // 2
        max_y = internal_height - x.rect.height // 2
        x.pos = (x.pos[0], max(min_y, min(movement, max_y)))

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
    internal_surface_rect = internal_surface.get_rect()
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

        if gamestate == "gameover":
            running = False
        elif gamestate == "game":
            # Player Movement
            player_movement = None
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_movement = player.pos[1] - movement_speed * dt
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_movement = player.pos[1] + movement_speed * dt
            # Player Boundry Check
            if player_movement is not None:
                check_movement(player, player_movement)
            
            # Ball Movement
            ball_speed_x = ball.speed * math.cos(ball.angle)
            ball_speed_y = ball.speed * math.sin(ball.angle)
            ball.pos = (
                ball.pos[0] + ball_speed_x * dt,
                ball.pos[1] + ball_speed_y * dt
            )
            # Ball Collision Check
            if ball.rect.colliderect(player.rect) or ball.rect.colliderect(opponent.rect):
                paddle = player if ball.rect.colliderect(player.rect) else opponent

                where_hit = (ball.pos[1] - paddle.pos[1]) / (paddle.rect.height / 2)

                ball.angle = where_hit * ball.max_bounce_angle

                if paddle == player:
                    ball.angle = math.pi - ball.angle
                elif paddle == opponent:
                    ball.angle = -ball.angle
                
                ball.speed *= 1.05
            # Ball Boundry Check
            if ball.pos[1] <= 0 or ball.pos[1] >= internal_height:
                ball.angle = -ball.angle
            elif ball.pos[0] <= 0 or ball.pos[0] >= internal_width:
                gamestate = "gameover"

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