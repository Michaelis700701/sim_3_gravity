import pygame, math, random
from pygame.math import Vector2 as vector
from settings import *

class Mass():
    def __init__(self,
                 surface: pygame.Surface,
                 start_vec: vector,
                 radius: int,
                 velocity: vector = vector(0, 0),
                 centered: bool = False
                 ) -> None:
        
        self.display_surface = surface

        self.position = start_vec
        self.pre_position = start_vec
        self.radius = radius
        self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO
        self.velocity = velocity
        self.centered = centered
        self.color = random.choice(MASSES_COLOR)
        self.rect = pygame.Rect(
            self.position.x - self.radius / math.sqrt(2),
            self.position.y - self.radius / math.sqrt(2), 
            self.radius * math.sqrt(2),
            self.radius * math.sqrt(2)
        )
    
    def get_velocity(self) -> None:
        for mass in masses:
            if self != mass:
                vector_distance = self.position - mass.position
                distance = math.sqrt(vector_distance.x ** 2 + vector_distance.y ** 2)
                force = G * ((self.mass * mass.mass) / (distance ** 2))
                acceleration = force / self.mass
                angle = math.atan2(mass.position.y - self.position.y, mass.position.x - self.position.x)
                vector_acceleration = vector(math.cos(angle) * acceleration, math.sin(angle) * acceleration)
                self.velocity += vector_acceleration

    def collide(self) -> None:
        for mass in masses:
            if (self != mass
                and self.rect.colliderect(mass.rect)
                and self.mass >= mass.mass
                ):
                    
                    mass_radius = math.sqrt(mass.mass / math.pi / MASS_AREA_RATIO)
                    self.radius += mass_radius / 2
                    self.mass = math.pi * (self.radius ** 2) * MASS_AREA_RATIO

                    self.rect = pygame.Rect(
                        self.position.x - self.radius / math.sqrt(2),
                        self.position.y - self.radius / math.sqrt(2), 
                        self.radius * math.sqrt(2),
                        self.radius * math.sqrt(2)
                    )
                    
                    masses.remove(mass)

    def draw(self, origin: vector) -> None:
        pygame.draw.circle(
            self.display_surface, self.color, self.position + origin, self.radius
        )
        if KEYS_PRESSED[pygame.K_F3]:
            drawable_rect = pygame.Rect(self.rect.left + origin.x, self.rect.top + origin.y, self.rect.width, self.rect.height)
            pygame.draw.rect(self.display_surface, (150, 0, 0), drawable_rect, 2)
            position_diff = self.position - self.pre_position
            exageration = 25
            pygame.draw.line(self.display_surface, 
                             (150, 0, 0), 
                             (self.pre_position + position_diff) + origin, 
                             (self.position + position_diff * exageration) + origin,
                             2)
    
    def update(self) -> None:
        self.collide()
        self.get_velocity()

        self.pre_position = vector(self.position)
        
        self.position += self.velocity

        self.rect = pygame.Rect(
            self.position.x - self.radius / math.sqrt(2),
            self.position.y - self.radius / math.sqrt(2), 
            self.radius * math.sqrt(2),
            self.radius * math.sqrt(2)
        )