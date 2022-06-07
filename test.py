import threading
import time
import pygame


class Loop:
    def __init__(self):
        pygame.init()

        self.current_time = 0
        self.previous_time = round(time.time() * 1000)
        self.update_rate = 1.0 / 60.0
        self.accumulator = 0.0
        self.next_stat_time = round(time.time() * 1000) + 1000
        self.ups = 0
        self.fps = 0

    def start(self):
        while True:
            self.current_time = round(time.time() * 1000)
            last_render_time_in_seconds = (self.current_time - self.previous_time) / 1000.0
            self.accumulator += last_render_time_in_seconds
            self.previous_time = self.current_time

            while self.accumulator > self.update_rate:
                self.update()
                self.render()
                self.accumulator -= self.update_rate

            self.print_stats()

    def update(self):
        self.ups += 1

    def render(self):
        self.fps += 1

    def print_stats(self):
        if time.time() * 1000 > self.next_stat_time:
            print(f'FPS: {self.fps} | UPS: {self.ups}')
            self.ups = 0
            self.fps = 0
            self.next_stat_time = round(time.time() * 1000) + 1000


if __name__ == '__main__':
    loop = Loop()
    loop.start()




