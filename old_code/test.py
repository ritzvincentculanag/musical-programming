import threading
import time
import pygame

from track import Track


class Loop:
    def __init__(self):
        pygame.init()

        self.track = Track()

        self.current_time = 0
        self.previous_time = round(time.time() * 1000)
        self.update_rate = 1.0 / 60.0
        self.accumulator = 0.0
        self.next_stat_time = round(time.time() * 1000) + 1000
        self.ups = 0
        self.fps = 0

    def start(self):
        game_loop = threading.Thread(target=self.game_loop)
        game_loop.start()


    def game_loop(self):
        while True:
            self.current_time = round(time.time() * 1000)
            last_render_time_in_seconds = (self.current_time - self.previous_time) / 1000.0
            self.accumulator += last_render_time_in_seconds
            self.previous_time = self.current_time

            while self.accumulator > self.update_rate:
                self.update()
                self.accumulator -= self.update_rate

            self.render()

            self.print_stats()

    def update(self):
        self.ups += 1

    def render(self):
        self.track.track()
        self.fps += 1

    def print_stats(self):
        if time.time() * 1000 > self.next_stat_time:
            print(f'FPS: {self.fps} | UPS:q {self.ups}')
            self.ups = 0
            self.fps = 0
            self.next_stat_time = round(time.time() * 1000) + 1000


def print_hello():
    while True:
        print("Main")


if __name__ == '__main__':
    loop = Loop()

    print_loop = threading.Thread(target=print_hello)
    print_loop.start()

    loop.start()
