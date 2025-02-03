import pygame
import ctypes

def main():
    class Button(pygame.sprite.Sprite):
        def __init__(
            self,
            texts = None,
            size = None,
            width_room = 20,
            height_room = 10,
            text_color = (0, 0, 0),
            spacing = 20,
            style = "default",
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
            self.surface = pygame.Surface(size)
            self.surface.fill((255, 255, 255))

            # Position Texts
            current_y = vertical_offset
            for i, text_surface in enumerate(text_surfaces):
                if style == "centered":
                    self.surface.blit(text_surface, ((size[0] - text_surface.get_width()) // 2, current_y))
                else:
                    self.surface.blit(text_surface, (width_room // 2, i * spacing))
                current_y += text_surface.get_height() + spacing
        
            self.rect = self.surface.get_rect()
            self.debug_color = debug_color

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

    internal_surface = pygame.Surface((internal_width, internal_height))
    screen = pygame.display.set_mode(screen_size) # pygame.FULLSCREEN

    # Create Buttons
    test_button = Button("Test", style="centered")
    test_button.rect.topleft = (50, 50)

    test_button1 = Button("Test Button", style="centered", debug_color=(0, 255, 0))
    test_button1.rect.topleft = (50, 150)
    
    test_button2 = Button(["Test", "Button"], style="centered", debug_color=(0, 0, 255), spacing=10)
    test_button2.rect.topleft = (50, 250)

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

        if gamestate == "game":
            # Interal rendering
            internal_surface.fill((0, 0, 0))
            internal_surface.blit(test_button.surface, test_button.rect.topleft)
            internal_surface.blit(test_button1.surface, test_button1.rect.topleft)
            internal_surface.blit(test_button2.surface, test_button2.rect.topleft)

            if debug_mode:
                test_button.debug(internal_surface)
                test_button1.debug(internal_surface)
                test_button2.debug(internal_surface)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()