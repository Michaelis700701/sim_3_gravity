import pygame
from settings import *
from simulation import Simulation

class Main():
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED).convert_alpha()
        self.clock = pygame.time.Clock()
        self.app_state = AppState()

    def run(self) -> None:
        while True:
            
            self.app_state.state_manager()
            
            pygame.display.update()
            self.clock.tick(60)
            #print(self.clock.get_fps())

class AppState():
    def __init__(self) -> None:
        self.simulation = Simulation()

    def state_manager(self) -> None:
        if ACTIVE_STATE['active_state'] == 'sim':
            self.simulation.run()

if __name__ == '__main__':
    main = Main()
    main.run()
    
    #profile.runctx('main.run()', globals(), locals())