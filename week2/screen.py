import pygame
import random
import math
import time

SCREEN_DIM = (800, 600)

# =======================================================================================
# Класс 2-мерных векторов Vec2d [1]. В классе следует определены методы для основных математических операций,
# необходимых для работы с вектором: Vec2d.__add__ (сумма), Vec2d.__sub__ (разность), Vec2d.__mul__ (произведение на число).
# А также добавить возможность вычислять длину вектора с использованием функции len(a) и метод int_pair,
# который возвращает кортеж из двух целых чисел (текущие координаты вектора).
# =======================================================================================


class Vec2d:

    def __init__(self, v=(0, 0)):
        """Вектор определяется координатами x, y — точка конца вектора.
        Начало вектора всегда совпадает с центом координат."""
        if v is None:
            self.x2 = float(0)
            self.y2 = float(1)
        self.x = float(v[0])
        self.y = float(v[1])

    def __sub__(self, other):
        """"Разность двух векторов"""
        return Vec2d((self.x - other.x, self.y - other.y))

    def __add__(self, other):
        """Cумма двух векторов"""
        return Vec2d((self.x + other.x, self.y + other.y))

    def __mul__(self, k):
        """Произведение на число"""
        return Vec2d((self.x * k, self.y * k))

    def __len__(self):
        """Длина вектора"""
        return math.sqrt(self.x * self.x + self.y * self.y)

    def int_pair(self):
        """Два целых числа"""
        return int(self.x), int(self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"({self.x}, {self.y})"

    # def vec(self, x, y):
    #     """РІРѕР·РІСЂР°С‰Р°РµС‚ РїР°СЂСѓ РєРѕРѕСЂРґРёРЅР°С‚, РѕРїСЂРµРґРµР»СЏСЋС‰РёС… РІРµРєС‚РѕСЂ (РєРѕРѕСЂРґРёРЅР°С‚С‹ С‚РѕС‡РєРё РєРѕРЅС†Р° РІРµРєС‚РѕСЂР°),
    #     РєРѕРѕСЂРґРёРЅР°С‚С‹ РЅР°С‡Р°Р»СЊРЅРѕР№ С‚РѕС‡РєРё РІРµРєС‚РѕСЂР° СЃРѕРІРїР°РґР°СЋС‚ СЃ РЅР°С‡Р°Р»РѕРј СЃРёСЃС‚РµРјС‹ РєРѕРѕСЂРґРёРЅР°С‚ (0, 0)"""
    #     return y - x


class Polyline:
    """ Класс замкнутых ломаных"""

    def __init__(self, display, points, speeds, step):
        self.display = display
        self.points = points
        self.speeds = speeds
        self.steps = step

    def draw_points(self, points, style="points", width=3, color=(255, 255, 255)):
        """ Точки на экране"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(self.display, color,
                                 (int(points[p_n].x), int(points[p_n].y)),
                                 (int(points[p_n + 1].x), int(points[p_n + 1].y)), width)
        elif style == "points":
            for p in points:
                pygame.draw.circle(self.display, color,
                                   (int(p.x), int(p.y)), width)

    def set_points(self):
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]
            if self.points[p].x > SCREEN_DIM[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2d((- self.speeds[p].x, self.speeds[p].y))
            if self.points[p].y > SCREEN_DIM[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2d((self.speeds[p].x, -self.speeds[p].y))

    def add_point(self, pos):
        self.points.append(Vec2d(pos))
        self.speeds.append(Vec2d((random.random() * 2, random.random() * 2)))

    # def delete_point(self):
    #     self._points.pop()

    def draw_help(self):
        """Отрисовка экрана справки программы"""
        self.display.fill((50, 50, 50))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        data = [["F1", "Show Help"], ["R", "Restart"], ["P", "Pause/Play"], ["Num+", "More points"],
                ["Num-", "Less points"], ["UP", "Fast"], ["DOWN", "Slow"],
                ["", ""], [str(self.steps), "Current points"]]

        pygame.draw.lines(self.display, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for i, text in enumerate(data):
            self.display.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
            self.display.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * i))

class Knot(Polyline):

    def __init__(self, display, points, speeds, step):
        self.display = display
        self.points = points
        self.speeds = speeds
        self.steps = step

    def add_point(self, pos):
        super().add_point(pos)
        self.get_knot(self.points, self.steps)

    # def delete_point(self):
    #     super().delete_point()
    #     self.get_knot()

    def set_points(self):
        super().set_points()
        self.get_knot(self.points, self.steps)

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return (points[deg] * alpha) + (self.get_point(points, alpha, deg - 1) * (1 - alpha))

    def get_points(self, base_points, count):
        alpha = 1 / count
        res = []
        for i in range(count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self, bpoints, count):
        if len(bpoints) < 3:
            return []
        res = []
        for i in range(-2, len(bpoints) - 2):
            ptn = []
            ptn.append((bpoints[i] + bpoints[i + 1]) * 0.5)
            ptn.append(bpoints[i + 1])
            ptn.append((bpoints[i + 1] + bpoints[i + 2]) * 0.5)

            res.extend(self.get_points(ptn, count))
        return res


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_caption("MyScreenSaver")

    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    k = Knot(gameDisplay, [], [], 35)

    working = True
    show_help = False
    pause = True

    hue = 0
    color = pygame.Color(0)
    delay = 0.0
    delay_step = 0.005

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    k.points = []
                    k.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    k.steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    k.steps -= 1 if k.steps > 1 else 0
                if event.key == pygame.K_UP:
                    # 'true' if True else 'false'
                    # delay = delay - 1 if delay - 1 >= 0 else 0
                    delay = delay - delay_step if delay - delay_step >= 0 else 0
                    # delay = delay - 1
                    print(delay)
                if event.key == pygame.K_DOWN:
                    delay = delay + delay_step
                    print(delay)

            if event.type == pygame.MOUSEBUTTONDOWN:
                k.add_point(event.pos)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)
        k.draw_points(k.points)
        k.draw_points(k.get_knot(k.points, k.steps), "line", 3, color)
        if not pause:
            k.set_points()
        if show_help:
            k.draw_help()

        pygame.display.flip()
        time.sleep(delay)

    pygame.display.quit()
    pygame.quit()
    exit(0)