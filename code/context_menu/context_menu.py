import pygame
from pygame.math import Vector2 as vector
from context_menu.vector_input import VectorInput
from context_menu.radius_input import RadiusInput


class ContextMenu():
    def __init__(
            self,
            surface: pygame.Surface,
            options: list[str | list[str]],
            font_size: int,
            __pre_selected_option: object | None = None
            ) -> None:
        self.display_surface = surface #pygame.display.get_surface()

        self.position = vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        self.options = options
        self.font = pygame.font.Font('assets/font/Product Sans Regular.ttf', font_size)
        self.margin = 7
        self.between_text_margin = 3
        self.text_surfaces = self.__create_text_surfaces()
        self.selected_option = None
        self.pre_selected_option = __pre_selected_option
        self.recursive_context_menu = {}
        self.return_text = None

        self.click = False
        self.pre_click = False

        self.active_context_menu = self
        
        for option in self.options:
            if type(option) == list:
                if option[1] == 'vector_input':
                    self.recursive_context_menu[option[0]] = VectorInput(self.display_surface, self.position, font_size, self)
                elif option[1] == 'radius_input':
                    self.recursive_context_menu[option[0]] = RadiusInput(self.display_surface, self.position, font_size, self)
                else:
                    self.recursive_context_menu[option[0]] = ContextMenu(self.display_surface, option[1:], font_size, self)
            else:
                self.recursive_context_menu[option] = None
        
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.__find_widest_option().get_width() + (self.margin * 2),
            self.__find_options_total_height() + (self.margin * 2)
        )
        
        self.surface = pygame.Surface(self.rect.size).convert_alpha()
        self.text_surface = pygame.Surface(self.rect.size, pygame.SRCALPHA).convert_alpha()
        self.__draw_text_surface()
        

    def __create_text_surfaces(self) -> list:
        text_surfaces = []

        for option in self.options:
            if type(option) == list:
                text = self.font.render(option[0], True, (0, 0, 0)).convert_alpha()
                text_surfaces.append((text, option[0]))
            else:
                text = self.font.render(option, True, (0, 0, 0)).convert_alpha()
                text_surfaces.append((text, option))
        
        return text_surfaces

    def __find_widest_option(self) -> pygame.Surface:
        widest_option = None
        for surface in self.text_surfaces:
            if widest_option == None:
                widest_option = surface[0]
            elif surface[0].get_width() > widest_option.get_width():
                widest_option = surface[0]
        return widest_option
    
    def __find_options_total_height(self) -> int:
        total = 0
        for surface in self.text_surfaces:
            total += surface[0].get_height() + self.between_text_margin
        return total - self.between_text_margin

    def __pick_option(self) -> None:
        mouse_pos = vector(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        if self.rect.collidepoint(mouse_pos):
            for surface, position in self.surface_position_tuples:
                rect = surface.get_rect()
                rect.update(self.position.x, position.y + self.position.y, self.rect.width, rect.height)
                if self.selected_option == None:
                    if rect.collidepoint(mouse_pos):
                        rect.update(0, position.y, self.rect.width, rect.height)
                        self.selected_option = rect
                        self.__click(surface)
                else:
                    break
    
    def __back(self) -> None:
        self.pre_selected_option.active_context_menu = self.pre_selected_option
        self.pre_selected_option.return_text = None

    def __click(self, surface: pygame.Surface) -> None:
        self.click = pygame.mouse.get_pressed()[0]
        if not self.click and self.pre_click:
            for surface_then_text in self.text_surfaces:
                if surface == surface_then_text[0]:
                    if self.recursive_context_menu[surface_then_text[1]] != None:
                        self.active_context_menu = self.recursive_context_menu[surface_then_text[1]]
                        self.return_text = surface_then_text[1]
                    elif surface_then_text[1] == 'Back':
                        self.__back()
                    else:
                        self.return_text = surface_then_text[1]
        self.pre_click = self.click

    def __draw_text_surface(self) -> None:
        self.surface_position_tuples = []
        total_height = (self.margin)
        for surface in self.text_surfaces:
            position = vector(
                self.margin,
                total_height
            )
            self.surface_position_tuples.append((surface[0], position))
            total_height += surface[0].get_height() + self.between_text_margin
        #self.text_surface.fill((255, 255, 255))
        self.text_surface.blits(self.surface_position_tuples)
        #self.text_surface.blit(surface_position_tuples[0][0], self.position)

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
    
    def read_output(self) -> list:
        output = []

        if self.active_context_menu != self:
            output.append(self.return_text)
            output.append(self.active_context_menu.return_text)
        else:
            output.append(self.return_text)

        return output

    def draw(self) -> None:

        self.surface.fill((255, 255, 255))
        self.__draw_selected_option()
        self.surface.blit(self.text_surface, vector(0, 0))
        self.__draw_border(width=2)

        self.display_surface.blit(self.surface, self.rect)

    def update(self) -> None:
        
        self.__pick_option()