import pygame
import ctypes
import random

def main():
    class Button(pygame.sprite.Sprite):
        def __init__(
            self,
            texts = None,
            size = None,
            width_room = 20,
            height_room = 10,
            text_color = (0, 0, 0),
            background_color = (0, 0, 0, 0),
            spacing = 20,
            style = "default",
            on_click = "",
            debug_color = (255, 0, 0)
        ):
            super().__init__()
            # Prepare Texts
            if texts is None:
                texts = [("", text_color)]
            elif isinstance(texts, str):
                texts = [(texts, text_color)]
            elif isinstance(texts, list):
                new_texts = []
                for text in texts:
                    if isinstance(text, tuple):
                        new_texts.append(text)
                    else:
                        new_texts.append((text, text_color))
                texts = new_texts

            # Button Size
            text_surfaces = [font.render(text, False, color) for text, color in texts]
            width = max(text_surface.get_width() for text_surface in text_surfaces)
            total_text_height = sum(text_surface.get_height() for text_surface in text_surfaces) + (len(text_surfaces) - 1) * spacing
            size = size or (width + width_room, total_text_height + height_room)

            # Vertical Offset
            vertical_offset = (size[1] - total_text_height) // 2

            # Button Surface
            self.surface = pygame.Surface(size, pygame.SRCALPHA)
            if background_color:
                self.surface.fill(background_color)

            # Position Texts
            current_y = vertical_offset
            for i, text_surface in enumerate(text_surfaces):
                if style == "centered":
                    self.surface.blit(text_surface, ((size[0] - text_surface.get_width()) // 2, current_y))
                else:
                    self.surface.blit(text_surface, (width_room // 2, i * spacing))
                current_y += text_surface.get_height() + spacing
        
            self.rect = self.surface.get_rect()
            self.on_click = on_click

            self.debug_color = debug_color
        
        def click(self):
            if self.on_click:
                self.on_click()

        def debug(self, surface: pygame.Surface):
            pygame.draw.rect(surface, self.debug_color, self.rect, 1)

    # Initialize
    pygame.init()
    pygame.display.set_caption("Pong")
    font = pygame.font.SysFont("Arial", 20)
    clock = pygame.time.Clock()

    # Screen Settings
    internal_width = 640
    internal_height = 360
    ctypes.windll.user32.SetProcessDPIAware()
    screen_size = (1920, 1080)

    # Surfaces
    internal_surface = pygame.Surface((internal_width, internal_height))
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    # Buttons
    game_board = Button(
        size = (min(internal_width, internal_height), min(internal_width, internal_height)),
        width_room = 0,
        height_room = 0,
        background_color = (255, 253, 208)
    )
    game_board.rect.center = (internal_width // 2, internal_height // 2)

    blocks = []
    game_board_size = 4
    cell_size = game_board.rect.width / game_board_size
    possible_coords = [(x * (cell_size / 2) * (game_board_size / 2) + (cell_size / 2), y * (cell_size / 2) * (game_board_size / 2) + (cell_size / 2)) for x in range(game_board_size) for y in range(game_board_size)]
    new_round = True
    new_game = True

    running = True
    debug_mode = False
    gamestate = "game"
    max_fps = 60

    space_pressed = False

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
        
        if keys[pygame.K_RETURN]:
            if not return_pressed:
                return_pressed = True
                new_round = True
        else:
            return_pressed = False

        if gamestate == "game":
            if possible_coords == []:
                gamestate = "gameover"

            elif new_round:
                new_block = Button(
                    size = (cell_size, cell_size),
                    width_room = 0,
                    height_room = 0,
                    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                )
                new_block_pos = random.choice(possible_coords)
                possible_coords.remove(new_block_pos)

                new_block.rect.center = new_block_pos

                blocks.append(new_block)

                active_coords = [block.rect.center for block in blocks]

                new_round = False

            # Interal rendering
            internal_surface.fill((0, 0, 0))

            for block in blocks:
                game_board.surface.blit(block.surface, block.rect)

            if debug_mode:
                for block in blocks:
                    block.debug(game_board.surface)
                
                game_board.debug(internal_surface)
            
            internal_surface.blit(game_board.surface, game_board.rect)
        
        elif gamestate == "gameover":
            internal_surface.fill((50, 50, 50))

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()