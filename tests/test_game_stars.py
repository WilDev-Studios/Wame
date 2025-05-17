from dataclasses import dataclass
from wame.ui import Text

import pygame
import random
import wame

@dataclass
class Star:
    x: int
    y: int
    r: int
    speed: int
    surface: pygame.Surface

class TestScene(wame.Scene):
    def on_init(self) -> None:
        self.fps: Text = Text(self.frame, f"FPS | {self.engine.settings.max_fps}", (125, 125, 125), pygame.font.SysFont("Ubuntu", 12))
        self.fps.set_pixel_position((5, 5))

        self.stars: list[list[Star]] = [[], [], []]

        for _ in range(1000):
            self.stars[0].append(self.generate_star(0))
        
        for _ in range(100):
            self.stars[1].append(self.generate_star(3))

        for _ in range(25):
            self.stars[2].append(self.generate_star(5))

    def generate_star(self, index: int) -> Star:
        radius: int = 1 * (index + 1)
        radius_2: int = radius * 2

        circle: pygame.Surface = pygame.Surface((radius_2, radius_2), pygame.SRCALPHA)
        pygame.draw.circle(circle, (255, 255, 255), (radius, radius), radius)

        return Star(random.randint(0, 1920), random.randint(0, 1080), radius, index * 3, circle)

    def on_fixed_update(self) -> None:
        self.fps.set_text(f"FPS | {round(self.engine.fps)}")

    def on_render(self) -> None:
        for row in self.stars:
            for star in row:
                self.screen.blit(star.surface, (star.x - star.r, star.y - star.r))

    def on_update(self) -> None:
        dt: float = self.engine.delta_time
        sh: int = self.screen.get_height()

        for row in self.stars:
            for star in row:
                star.y += star.speed * dt

                if star.y - (star.r / 2) < sh:
                    continue

                star.y = 0 - (star.r // 2)

def test_game_starry_sky():
    engine: wame.Engine = wame.Engine("Tween Test", wame.Pipeline.PYGAME, settings_persistent=False)
    engine.set_update_interval(0.5)
    engine.register_scene("Test", TestScene)
    engine.set_scene("Test")

    engine.start()