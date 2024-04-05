import pygame, math, sys
from pygame.math import Vector2 as vector
from settings import *
from mass import Mass
from context_menu.context_menu import ContextMenu

class Simulation():
    def __init__(self) -> None:
        self.display_surface = pygame.display.get_surface()
        self.surface = pygame.Surface((WINDOW_WIDTH * 3, WINDOW_HEIGHT * 3)).convert_alpha()
    
        self.origin = vector(0, 0)
        self.zoom = 1
        self.context_menu = None

        self.active_context_menu = None

        #masses.extend([Mass(vector(450, 250), 50, centered=True), Mass(vector(650, 150), 15, vector(1.3, 2.2)), Mass(vector(350, 350), 15, vector(2.3, 1.5))])

    def update_keys_pressed(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            for key in KEYS_PRESSED:
                if event.key == key:
                    if KEYS_PRESSED[key] == True:
                        KEYS_PRESSED[key] = False
                    else:
                        KEYS_PRESSED[key] = True

    def move_origin(self) -> None:
        scroll_amount = 5
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]: self.origin.y -= scroll_amount
        elif pressed[pygame.K_s] : self.origin.y += scroll_amount
        elif pressed[pygame.K_d] : self.origin.x += scroll_amount
        elif pressed[pygame.K_a] : self.origin.x -= scroll_amount

    def center(self) -> None:
        for mass in masses:
            if mass.centered:
                self.origin = ((vector(0, 0) - mass.position) + vector((WINDOW_WIDTH / self.zoom) / 2, (WINDOW_HEIGHT / self.zoom) / 2))
                continue

    def manage_window(self, event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWMAXIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.WINDOWMINIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                pygame.quit()
                sys.exit()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.context_menu = None
                if event.key == pygame.K_MINUS and self.zoom > 0.5:
                    self.zoom -= 0.1
                if event.key == pygame.K_EQUALS and self.zoom < 2:
                    self.zoom += 0.1
            #elif event.key == pygame.K_ESCAPE:
                #ACTIVE_STATE['active_state'] = 'main_menu'

    def create_context_menu(self) -> None:
        if pygame.mouse.get_pressed()[2] and self.context_menu == None:
            self.create_orbital_radius = 15
            self.create_orbital_velocity = vector(0, 0)
            self.create_orbital_centered = False
            self.context_menu = ContextMenu(
                self.display_surface,
                [
                    ['Mass', 'radius_input'],
                    ['Set Velocity', ['Vector Input', 'vector_input'], 'Orbit around Clicked', 'Back'],
                    ['Centered', 'True', 'False', 'Back'],
                    'Create Orbital'
                ], 15)

    def return_context_menu(self) -> None:
        if self.context_menu != None:
            output = self.context_menu.read_output()
            print(output)
            if output[-1] != None:
                if output == ['Mass', 'Return']:
                    self.create_orbital_radius = self.context_menu.active_context_menu.return_radius()
                elif output == ['Set Velocity', 'Vector Input', 'Return']:
                    self.create_orbital_velocity = self.context_menu.active_context_menu.active_context_menu.return_vector()
                elif output == ['Set Velocity', 'Orbit around Clicked']:
                    vector_distance = ((self.context_menu.position / self.zoom) - self.origin) - masses[0].position
                    distance = math.sqrt(vector_distance.x ** 2 + vector_distance.y ** 2)
                    mass = math.pi * (self.create_orbital_radius ** 2) * MASS_AREA_RATIO
                    force = G * ((mass * masses[0].mass) / (distance ** 2))
                    acceleration = force / mass
                    angle = math.atan2(masses[0].position.y - ((self.context_menu.position / self.zoom) - self.origin).y, masses[0].position.x - ((self.context_menu.position / self.zoom) - self.origin).x) + 1.5708
                    self.create_orbital_velocity = vector(math.cos(angle) * acceleration, math.sin(angle) * acceleration)
                    print(self.create_orbital_velocity)
                elif output == ['Centered', 'True']:
                    self.create_orbital_centered = True
                elif output == ['Create Orbital']:
                    masses.append(Mass(
                        self.surface,
                        ((self.context_menu.position / self.zoom) - self.origin),
                        self.create_orbital_radius,
                        self.create_orbital_velocity,
                        self.create_orbital_centered))
                    self.context_menu = None
                    print(self.create_orbital_velocity)

    def event_loop(self) -> None:
        for event in pygame.event.get():
            
            self.manage_window(event)
            
            self.update_keys_pressed(event)

        self.create_context_menu()
        self.return_context_menu()
        self.move_origin()
        self.center()
    
    def draw_tile_lines(self) -> None:
        columns = int(WINDOW_WIDTH // TILE_SIZE / self.zoom)
        rows = int(WINDOW_HEIGHT // TILE_SIZE / self.zoom)
        
        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)

        support_lines_surface = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA).convert_alpha()
        #support_lines_surface.fill((100,100,100))

        for column in range(columns + 2) :
            x = origin_offset.x + column * TILE_SIZE
            pygame.draw.line(support_lines_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT / self.zoom), 2)
        for row in range(rows + 2):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(support_lines_surface, LINE_COLOR, (0, y), (WINDOW_WIDTH / self.zoom, y), 2)
        
        self.surface.blit(support_lines_surface, (0,0))

    def draw(self) -> None:
        self.surface.fill((BACKGROUND_COLOR))
        self.draw_tile_lines()

        for mass in masses:
            mass.draw(self.origin)

        

        pygame.draw.circle(self.surface, (250, 0, 0), self.origin, 10)

        zoomed_screen = pygame.transform.smoothscale_by(self.surface, self.zoom)
        self.display_surface.blit(zoomed_screen, vector(0, 0))
            #pygame.transform.scale(self.surface, (WINDOW_WIDTH * self.zoom, WINDOW_HEIGHT * self.zoom)), vector(0, 0))
        
        if self.context_menu != None:
            self.context_menu.active_context_menu.draw()

    def run(self) -> None:

        self.event_loop()

        if self.context_menu == None:
            for mass in masses:
                mass.update()
        else:
            self.context_menu.active_context_menu.update()
            print(self.context_menu.active_context_menu)
            
        self.draw()
        print(masses)