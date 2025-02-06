import pygame
import ctypes
def main():
    class Stats:
        def __init__(self):
            self.day = 0
    class Player():
        def __init__(
            self,
            money = 0,  
            stress = 0, 
            happiness = 0,
            productivity = 10,
            hunger = 0,
            time_since_last_meal = 0,
            packed_lunch = False,
            health = 100,
        ):
            self.money = money
            self.stress = stress
            self.happiness = happiness
            self.productivity = productivity
            self.hunger = hunger
            self.time_since_last_meal = time_since_last_meal
            self.packed_lunch = packed_lunch
            self.health = health
    
    class Job():
        def __init__(
            self,
            name = "Job",
            salary = 7,
            work_time = 8,
            promotion_progress = 0,
            ladder_level = 0
        ):
            self.name = name
            self.salary = salary
            self.work_time = work_time
            self.promotion_progress = promotion_progress
            self.ladder_level = ladder_level
        
        def promotion(self):
            self.ladder_level += 1
            self.salary += round(self.ladder_level * 1.5 + 1) + self.salary

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
            parent = None,
            on_click = None,
            on_hover = None,
            clean_up = None,
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
            self.parent = parent
            self.on_click = on_click

            # Hovering
            self.on_hover = on_hover
            self.clean_up = clean_up
            self.hovering = False

            self.debug_color = debug_color
        
        def click(self):
            if self.on_click:
                self.on_click()
        
        def hover(self):
            if self.on_hover:
                self.on_hover()

        def debug(self, surface: pygame.Surface):
            pygame.draw.rect(surface, self.debug_color, self.rect, 1)

    def get_hover_chain(button):
        '''Return a list of this button and all its parents.'''
        chain = []
        current = button
        while current:
            chain.append(current)
            current = current.parent  # assumes parent is either a Button or None
        return chain

    def calculate_hunger_increase(time_taken: int):
        hunger_increase = 0
        for i in range(time_taken):
            if player.time_since_last_meal <= 3:
                hunger_increase += 5
            elif player.time_since_last_meal <= 6:
                hunger_increase += 12
            else:
                hunger_increase += 20
            player.time_since_last_meal += 1
            i += 1
        return hunger_increase

    def advance_day():
        stats.day += 1

        change_productivity = player.productivity + (player.happiness - player.stress) / 10
        if change_productivity > 100:
            player.productivity = 100
        elif change_productivity < 0:
            player.productivity = 0
        else:
            player.productivity = change_productivity

        job.promotion_progress += player.productivity / 10
        if job.promotion_progress >= 100:
            job.promotion_progress = 0
            job.promotion()

    '''*******************************Button Clicks*******************************'''
    
    def work():
        player.money += job.work_time * job.salary

        hunger_increase = calculate_hunger_increase(job.work_time)

        player.hunger += hunger_increase
        if player.hunger > 100:
            player.health -= player.hunger - 100
            player.hunger = 100
    
    def rest(time_taken: int = 10):
        if player.health < 100:
            player.health = min(player.health + time_taken, 100)

        hunger_increase = calculate_hunger_increase(time_taken)
        
        player.hunger += hunger_increase
        if player.hunger > 100:
            player.health -= player.hunger - 100
            player.hunger = 100
    
    def eat(food_type: str = "small_snack"):
        if player.money >= 20:
            player.money -= 20

            add_health = player.health + 5
            if add_health > 100:
                player.health = 100
            else:
                player.health = add_health

            less_hunger = player.hunger - 10
            if less_hunger < 0:
                player.hunger = 0
            else:
                player.hunger = less_hunger

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
    buttons = []
    visible_buttons = []
    hoverable_buttons = []
    prev_hovered = set()

    work_button = Button(
        "Work", 
        style = "centered", 
        background_color = (240, 240, 240), 
        debug_color = (255, 0, 0), 
        on_click = work, 
        on_hover = lambda: visible_buttons.append(pack_lunch_button) and hoverable_buttons.append(pack_lunch_button) if pack_lunch_button not in visible_buttons else None,
        clean_up = lambda: visible_buttons.remove(pack_lunch_button) and hoverable_buttons.remove(pack_lunch_button) if pack_lunch_button in visible_buttons else None
    )
    work_button.rect.center = (internal_width // 2, internal_height // 2 - 50)
    hoverable_buttons.append(work_button)
    visible_buttons.append(work_button)
    buttons.append(work_button)

    rest_button = Button(
        "Rest", 
        style = "centered", 
        background_color = (240, 250, 250), 
        debug_color = (0, 255, 0), 
        on_click = rest
    )
    rest_button.rect.center = (internal_width // 2, internal_height // 2)
    visible_buttons.append(rest_button)
    buttons.append(rest_button)
    
    eat_button = Button(
        "Eat", 
        style = "centered", 
        background_color = (240, 240, 240), 
        debug_color = (0, 0, 255), 
        on_click = eat
    )
    eat_button.rect.center = (internal_width // 2, internal_height // 2 + 50)
    visible_buttons.append(eat_button)
    buttons.append(eat_button)

    pack_lunch_button = Button(
        "Pack Lunch",
        style = "centered",
        background_color = (240, 240, 240),
        debug_color = (255, 0, 255),
        on_click = lambda: setattr(player, "packed_lunch", True),
        parent = work_button
    )
    pack_lunch_button.rect.center = (work_button.rect.width // 2 + pack_lunch_button.rect.width // 2 + work_button.rect.centerx, work_button.rect.centery)
    buttons.append(pack_lunch_button)

    # Player
    job = Job()
    player = Player()

    # Stats
    stats = Stats()

    running = True
    debug_mode = False
    gamestate = "game"
    max_fps = 60

    space_pressed = False

    while running:
        keys = pygame.key.get_pressed()

        # Get accurate mouse position
        scaled_mouse_pos = pygame.mouse.get_pos()
        mouse_pos = (
            scaled_mouse_pos[0] * internal_width / screen_size[0],
            scaled_mouse_pos[1] * internal_height / screen_size[1]
            )

        if keys[pygame.K_ESCAPE]:
            running = False
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in buttons:
                        if button.rect.collidepoint(mouse_pos):
                            button.click()

                            advance_day()
                            if player.health <= 0:
                                gamestate = "game over"
        
        # Handle mouse hovering
        current_hovered = set()

        for button in hoverable_buttons:
            if button.rect.collidepoint(mouse_pos):
                chain = get_hover_chain(button)
                for btn in chain:
                    btn.hover()
                    btn.hovering = True
                    current_hovered.add(btn)
        
        for button in prev_hovered - current_hovered:
            btn.clean_up()
            button.hovering = False

        prev_hovered = current_hovered
        
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
            internal_surface.fill((200, 200, 200))

            # Create User Interface
            user_interface_surfaces = []

            # Player
            money_text_surface = Button(f"Money : {player.money}", style="centered", debug_color=(0, 255, 0))
            money_text_surface.rect.topleft = (0, 0)
            user_interface_surfaces.append(money_text_surface)

            hunger_text_surface = Button(f"Hunger : {player.hunger}", style="centered", debug_color=(0, 255, 0))
            hunger_text_surface.rect.topleft = (0, 25)
            user_interface_surfaces.append(hunger_text_surface)

            health_text_surface = Button(f"Health : {player.health}", style="centered", debug_color=(0, 255, 0))
            health_text_surface.rect.topleft = (0, 50)
            user_interface_surfaces.append(health_text_surface)

            # Job
            ladder_level_text_surface = Button(f"Ladder Level : {job.ladder_level}", style="centered", debug_color=(0, 255, 0))
            ladder_level_text_surface.rect.topleft = (internal_width - ladder_level_text_surface.rect.width, 0)
            user_interface_surfaces.append(ladder_level_text_surface)

            work_time_text_surface = Button(f"Work Time : {job.work_time}", style="centered", debug_color=(0, 255, 0))
            work_time_text_surface.rect.topleft = (internal_width - work_time_text_surface.rect.width, 25)
            user_interface_surfaces.append(work_time_text_surface)

            salary_text_surface = Button(f"Salary : {job.salary}", style="centered", debug_color=(0, 255, 0))
            salary_text_surface.rect.topleft = (internal_width - salary_text_surface.rect.width, 50)
            user_interface_surfaces.append(salary_text_surface)

            for surface in user_interface_surfaces:
                internal_surface.blit(surface.surface, surface.rect.topleft)

            # Render Buttons
            for button in visible_buttons:
                internal_surface.blit(button.surface, button.rect.topleft)
                
                if debug_mode:
                    button.debug(internal_surface)

        # Upscale to 1920x1080
        scaled_surface = pygame.transform.scale(internal_surface, screen_size)
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        # Tick Speed
        dt = clock.tick(max_fps) / 1000

if __name__ == "__main__":
    main()


'''
 - Implement "parnet" buttons, to keep menus open during navigation
 - Implement new food types
 - Implement packing lunch
'''