import threading, pygame


class FadeInOut:
    def __init__(self, surface):
        self.surface = surface
        self.fade_in_thread = None
        self.fade_out_thread = None

    def start_fade_in(self, duration=1000):
        self.fade_in_thread = threading.Thread(target=self._fade_in_)
        self.fade_in_thread.daemon = True
        self.fade_in_thread.start()
        print('fade_in_started')

    def _fade_in_(self, duration=100):
        alpha_step = 255 / duration
        background = pygame.Surface(self.surface.get_size()).convert()
        background.fill((0, 0, 0))
        for step in range(duration):
            background.set_alpha(255 - step * alpha_step)
            self.surface.blit(background, (0, 0))
            print(' alpha = ', background.get_alpha())
