import pygame, math
from pygame.math import Vector2 as vector
from pygame import gfxdraw
from settings import draw_circle

class RadiusInput():
    def __init__(
            self,
            surface: pygame.Surface,
            position: vector,
            font_size: int,
            __pre_selected_option: object | None = None
            ) -> None:
        self.display_surface = surface #pygame.display.get_surface()

        self.radius = 0
        self.position = position
        self.font = pygame.font.Font('assets/font/Product Sans Regular.ttf', font_size)
        self.margin = 7
        self.between_text_margin = 3
        self.selection_margin = 2
        self.text_surfaces = self.__create_text_surfaces()
        self.selected_option = None
        self.pre_selected_option = __pre_selected_option
        self.return_text = None
        self.max_input = 60

        self.click = False
        self.pre_click = False


        self.input_rect = pygame.Rect(
            self.position.x + self.margin,
            self.position.y + self.margin + self.text_surfaces[0][0].get_height() + self.margin,
            125,
            125
        )
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.input_rect.width + (self.margin * 2),
            self.input_rect.height + self.text_surfaces[0][0].get_height() + (self.between_text_margin * 2) + (self.margin * 2) + self.text_surfaces[1][0].get_height() + (self.selection_margin * 2)
        )

        self.input_surface = self.__create_input_surface()
        self.surface = pygame.Surface(self.rect.size).convert_alpha()
        self.text_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        self.__draw_text_surface()
    
    def __create_text_surfaces(self) -> list:
        text_surfaces = []

        for option in ['Radius: 0', 'Reset', 'Save']:
            text_surfaces.append((self.font.render(option, True, (0, 0, 0)).convert_alpha(), option))        
        
        return text_surfaces
    
    def __create_input_surface(self, mouse_pos: vector = None) -> pygame.Surface:
        input_surface = pygame.Surface(self.input_rect.size, pygame.SRCALPHA).convert_alpha()
        rect = input_surface.get_rect()

        for radius in range(0, self.max_input + 1, 15):
            gfxdraw.circle(
                input_surface,
                rect.centerx,
                rect.centery,
                radius,
                (150, 150, 150),
            )

        pygame.draw.aalines(
            input_surface,
            (0, 0, 0),
            False,
            [rect.midtop, rect.midbottom, rect.center,
             rect.midleft, rect.midright
             ]
        )

        if mouse_pos:
            draw_circle(
                input_surface,
                (200, 0, 0),
                vector(self.input_rect.width / 2, self.input_rect.height / 2),
                int(mouse_pos.distance_to(vector(self.input_rect.width / 2, self.input_rect.height / 2)))
            )
        
        return input_surface

    def __pick_option(self) -> None:
        mouse_pos = vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if self.rect.collidepoint(mouse_pos):
            if mouse_pos.distance_to(self.input_rect.center) <= self.max_input:
                if True:
                    self.__click_input(mouse_pos)
            else:
                for surface, position in self.surface_position_tuples[1:]:
                    rect = surface.get_rect()
                    rect.update(position.x + self.position.x, position.y + self.position.y, rect.width, rect.height)
                    if self.selected_option == None:
                        if rect.collidepoint(mouse_pos):
                            rect.update(position.x - self.selection_margin, position.y - self.selection_margin, rect.width + self.selection_margin * 2, rect.height + self.selection_margin * 2)
                            self.selected_option = rect
                            self.__click_option(surface)
                    else:
                        break

    def return_radius(self) -> vector:
        self.pre_selected_option.active_context_menu = self.pre_selected_option
        self.pre_selected_option.return_text = None
        self.return_text = None

        return self.radius

    def __update_input_surface(self, mouse_pos: vector) -> None:
            self.input_surface = self.__create_input_surface(mouse_pos - self.input_rect.topleft)

            self.radius = mouse_pos.distance_to(self.input_rect.center)
            angle = math.atan2(mouse_pos.y - self.input_rect.centery, mouse_pos.x - self.input_rect.centerx)
            decrease_acc = 25
            vector_acceleration = vector(math.cos(angle) * self.radius / decrease_acc, math.sin(angle) * self.radius / decrease_acc)
            self.power_vector = vector_acceleration

            self.text_surfaces[0] = (self.font.render(f'Radius {round(self.radius, 1)}', True, (0, 0, 0)).convert_alpha(), f'Radius {round(self.radius, 1)}')
            self.__draw_text_surface()

    def __click_input(self, mouse_pos: vector) -> None:
        self.click = pygame.mouse.get_pressed()[0]
        if self.click:
            self.__update_input_surface(mouse_pos)

    def __click_option(self, surface: pygame.Surface) -> None:
        self.click = pygame.mouse.get_pressed()[0]
        if not self.click and self.pre_click:
            for surface_then_text in self.text_surfaces[1:]:
                if surface == surface_then_text[0]:
                    if surface_then_text[1] == 'Reset':
                        self.__update_input_surface(vector(self.input_rect.centerx, self.input_rect.centery))
                    elif surface_then_text[1] == 'Save':
                        self.return_text = 'Return'
        self.pre_click = self.click

    def __draw_text_surface(self) -> None:
        self.surface_position_tuples = []
        for surface, text in self.text_surfaces:
            if 'Radius' in text:
                potition = vector(
                    self.margin,
                    self.margin
                )
            elif 'Reset' in text:
                potition = vector(
                    self.margin,
                    self.rect.height - self.margin - surface.get_height()
                )
            elif 'Save' in text:
                potition = vector(
                    self.rect.width - self.margin - surface.get_width(),
                    self.rect.height - self.margin - surface.get_height()
                )
            else: print(text)
            self.surface_position_tuples.append((surface, potition))
        self.text_surface.fill((0, 0, 0, 0))
        self.text_surface.blits(self.surface_position_tuples)

    def __draw_selected_option(self) -> None:
        if self.selected_option != None:
            pygame.draw.rect(
                self.surface,
                (210, 210, 210),
                self.selected_option
            )
            self.selected_option = None

    def __draw_border(self, width: int = 2) -> None:
        pygame.draw.polygon(
            self.surface,
            (50, 50, 50),
            [
                vector(0, 0), 
                vector(0, self.rect.height - width), 
                vector(self.rect.width - width, self.rect.height - width), 
                vector(self.rect.width - width, 0)
                ],
            width
        )
        self.surface.fill((50, 50, 50), pygame.Rect(self.rect.width - width, self.rect.height - width, width, width))
    
    def draw(self) -> None:

        self.surface.fill((255, 255, 255))
        self.__draw_selected_option()
        self.surface.blit(self.text_surface, vector(0, 0))
        self.surface.blit(self.input_surface, self.input_rect.topleft - self.position)
        self.__draw_border(width=2)

        self.display_surface.blit(self.surface, self.rect)
    
    def update(self) -> None:
        
        self.__pick_option()