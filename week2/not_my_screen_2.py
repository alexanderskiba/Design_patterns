import math
import pygame
import random

SCREEN_DIM = (800, 600)


def len(obj):
    return obj.__len__()


class Vec2D:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __add__(self, point):
        p = self.__class__(self._x + point.x, self._y + point.y)
        return p

    def __sub__(self, point):
        p = self.__class__(self._x - point.x, self._y - point.y)
        return p

    def __mul__(self, obj):
        if isinstance(obj, self.__class__):
            return self._x * obj.x + self._y * obj.y
        elif isinstance(obj, int) or isinstance(obj, float):
            p = self.__class__(self._x * obj, self._y * obj)
            return p

    def __len__(self):
        return math.sqrt(self._x * self._x + self._y * self._y)

    def __eq__(self, point):
        return self._x == point.x and self._y == point.y

    def int_pair(self):
        return int(self._x), int(self._y)


class Polyline:
    def __init__(self, points, speeds):
        self.points = points
        self.speeds = speeds

    def add_point(self, point, speed):
        """
        РґРѕР±Р°РІР»РµРЅРёРµ С‚РѕС‡РєРё РІ Р»РѕРјР°РЅРЅСѓСЋ СЃ РµРµ СЃРєРѕСЂРѕСЃС‚СЊСЋ
        """
        self.points.append(point)
        self.speeds.append(speed)

    def set_points(self, screen_dim):
        """С„СѓРЅРєС†РёСЏ РїРµСЂРµСЂР°СЃС‡РµС‚Р° РєРѕРѕСЂРґРёРЅР°С‚ РѕРїРѕСЂРЅС‹С… С‚РѕС‡РµРє"""
        for p in range(len(self.points)):
            self.points[p] = self.points[p] + self.speeds[p]

            if self.points[p].x > screen_dim[0] or self.points[p].x < 0:
                self.speeds[p] = Vec2D(- self.speeds[p].x, self.speeds[p].y)
            if self.points[p].y > screen_dim[1] or self.points[p].y < 0:
                self.speeds[p] = Vec2D(self.speeds[p].x, -self.speeds[p].y)

    @staticmethod
    def draw_points(display, points, style="points", width=3, color=(255, 255, 255)):
        """С„СѓРЅРєС†РёСЏ РѕС‚СЂРёСЃРѕРІРєРё С‚РѕС‡РµРє РЅР° СЌРєСЂР°РЅРµ"""
        if style == "line":
            for p_n in range(-1, len(points) - 1):
                pygame.draw.line(display, color,
                                 points[p_n].int_pair(),
                                 points[p_n + 1].int_pair(), width)

        elif style == "points":
            for p in points:
                pygame.draw.circle(display, color,
                                   p.int_pair(), width)

    def change_speed(self, speed_percent, speedup):
        speed_percent %= 100
        for i, _ in enumerate(self.speeds):
            self.speeds[i] *= 1 + speed_percent / 100 * (1 if speedup else -1)

    def delete_point(self):
        """
        delete bearing point
        """
        if len(self.points) > 0 and len(self.speeds) > 0:
            self.points.pop(-1)
            self.speeds.pop(-1)


class Knot(Polyline):
    def __init__(self, points, speeds, count=1):
        super().__init__(points, speeds)
        self._count = count
        self.all_points = points

    def add_point(self, point, speed):
        """
        РґРѕР±Р°РІР»РµРЅРёРµ С‚РѕС‡РєРё РІ Р»РѕРјР°РЅРЅСѓСЋ СЃ РµРµ СЃРєРѕСЂРѕСЃС‚СЊСЋ
        """
        super().add_point(point, speed)
        self.get_knot()

    def delete_point(self):
        super().delete_point()
        self.get_knot()

    def set_points(self, screen_dim):
        """С„СѓРЅРєС†РёСЏ РїРµСЂРµСЂР°СЃС‡РµС‚Р° РєРѕРѕСЂРґРёРЅР°С‚ РѕРїРѕСЂРЅС‹С… С‚РѕС‡РµРє"""
        super().set_points(screen_dim)
        self.get_knot()

    def get_point(self, points, alpha, deg=None):
        if deg is None:
            deg = len(points) - 1
        if deg == 0:
            return points[0]
        return points[deg] * alpha + self.get_point(points, alpha, deg - 1) * (1 - alpha)

    def get_points(self, base_points):
        alpha = 1 / self._count
        res = []
        for i in range(self._count):
            res.append(self.get_point(base_points, i * alpha))
        return res

    def get_knot(self):
        if len(self.points) < 3:
            self.all_points = []
        else:
            res = []
            for i in range(-2, len(self.points) - 2):
                ptn = list()
                ptn.append((self.points[i] + self.points[i + 1]) * 0.5)
                ptn.append(self.points[i + 1])
                ptn.append((self.points[i + 1] + self.points[i + 2]) * 0.5)

                res.extend(self.get_points(ptn))
            self.all_points = res

    def draw_line(self, display, width=3, color=(255, 255, 255)):
        self.draw_points(display, self.all_points, "line", width, color)

    def draw_bearing_points(self, display, width=3, color=(255, 255, 255)):
        self.draw_points(display, self.points, "points", width, color)

    def up_count(self, val):
        self._count += val
        self.get_knot()

    def down_count(self, val):
        self._count = self._count - val if self._count > val else 1
        self.get_knot()

    def get_count(self):
        return self._count

    def restart_line(self):
        self.points = []
        self.speeds = []
        self.count = 1
        self.all_points = []


class Lines:
    def __init__(self, line):
        self.select_line = line
        self.lines_list = [line]
        self.index_sel_line = 0

        self.counter = 0

    def add_line(self, line):
        self.lines_list.append(line)
        self.index_sel_line = len(self.lines_list) - 1
        self.select_line = self.lines_list[self.index_sel_line]

    def prev_line(self):
        self.index_sel_line = (self.index_sel_line - 1) % len(self.lines_list)
        self.select_line = self.lines_list[self.index_sel_line]

    def next_line(self):
        self.index_sel_line = (self.index_sel_line + 1) % len(self.lines_list)
        self.select_line = self.lines_list[self.index_sel_line]

    def sel_line(self, index):
        if 0 <= index < len(self.lines_list):
            self.select_line = self.lines_list[index]

    def count_lines(self):
        return len(self.lines_list)

    def restart_lines(self):
        self.lines_list.clear()
        self.lines_list.append(Knot([], []))
        self.index_sel_line = 0
        self.select_line = self.lines_list[self.index_sel_line]

    def get_index_sel_line(self):
        return self.index_sel_line

    def delete_select_line(self):
        if len(self.lines_list) > 1:
            self.lines_list.pop(self.index_sel_line)
            self.prev_line()
        else:
            self.restart_lines()

    def set_lines_points(self, screen_dim):
        for i, _ in enumerate(self.lines_list):
            self.lines_list[i].set_points(screen_dim)

    def change_speeds(self, speed_percents, speedup):
        for line in self.lines_list:
            line.change_speed(speed_percents, speedup)

    def __iter__(self):
        return self

    def __next__(self):
        if 0 <= self.counter < len(self.lines_list):
            self.counter += 1
            return self.lines_list[self.counter - 1]
        else:
            self.counter = 0
            raise StopIteration


def draw_help(line):
    """С„СѓРЅРєС†РёСЏ РѕС‚СЂРёСЃРѕРІРєРё СЌРєСЂР°РЅР° СЃРїСЂР°РІРєРё РїСЂРѕРіСЂР°РјРјС‹"""
    gameDisplay.fill((50, 50, 50))
    font1 = pygame.font.SysFont("courier", 24)
    font2 = pygame.font.SysFont("serif", 24)
    data = list()
    data.append(["F1", "   Show Help"])
    data.append(["R", "   Restart"])
    data.append(["P", "   Pause/Play"])
    data.append(["D", "   Delete bearing point"])
    data.append(["L", "   append line"])
    data.append(["arr l", "   select previous line"])
    data.append(["arr r", "   select next line"])
    data.append(["arr up", "   More points"])
    data.append(["arr down", "   Less points"])
    data.append(["q", "delete select line"])
    data.append(["x", "faster"])
    data.append(["z", "slower"])
    data.append([str(line.get_count()), "Current points"])

    pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
        (0, 0), (800, 0), (800, 600), (0, 600)], 5)
    for i, text in enumerate(data):
        gameDisplay.blit(font1.render(
            text[0], True, (128, 128, 255)), (100, 100 + 30 * i))
        gameDisplay.blit(font2.render(
            text[1], True, (128, 128, 255)), (200, 100 + 30 * i))


def draw_number_of_line(display, num):
    pygame.draw.rect(display, (120, 120, 120), (SCREEN_DIM[0] * 0.95, 0, SCREEN_DIM[0] * 0.05, SCREEN_DIM[1] * 0.05))
    font1 = pygame.font.SysFont("courier", 15)
    display.blit(font1.render(f"{num}", True, (255, 255, 255)), (SCREEN_DIM[0] * 0.97, 0))


if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_DIM)
    pygame.display.set_caption("MyScreenSaver")
    working = True
    show_help = False
    pause = True
    clock = pygame.time.Clock()
    fps = 100

    hue = 0
    color = pygame.Color(0)

    line = Knot([], [])
    lines = Lines(Knot([], []))

    while working:
        # clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    lines.restart_lines()
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_UP:
                    lines.select_line.up_count(1)
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_DOWN:
                    lines.select_line.down_count(1)
                if event.key == pygame.K_d:
                    lines.select_line.delete_point()
                if event.key == pygame.K_l:
                    lines.add_line(Knot([], []))
                if event.key == pygame.K_LEFT:
                    lines.prev_line()
                if event.key == pygame.K_RIGHT:
                    lines.next_line()
                if event.key == pygame.K_q:
                    lines.delete_select_line()
                if event.key == pygame.K_z:
                    lines.change_speeds(20, False)
                if event.key == pygame.K_x:
                    lines.change_speeds(20, True)

            if event.type == pygame.MOUSEBUTTONDOWN:
                point = Vec2D(*event.pos)
                speed = Vec2D(random.random() * 2, random.random() * 2)
                lines.select_line.add_point(point, speed)

        gameDisplay.fill((0, 0, 0))
        hue = (hue + 1) % 360
        color.hsla = (hue, 100, 50, 100)

        draw_number_of_line(gameDisplay, lines.get_index_sel_line() + 1)

        for line in lines:
            line.draw_bearing_points(gameDisplay)
            line.draw_line(gameDisplay)

        lines.select_line.draw_bearing_points(gameDisplay)
        lines.select_line.draw_line(gameDisplay, 3, color)

        if not pause:
            lines.set_lines_points(SCREEN_DIM)
        if show_help:
            draw_help(lines.select_line)

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)