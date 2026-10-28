"""Превращение окружности в треугольник в полярных координатах."""

import math


class AnimationModel:
    """Хранить параметры фигуры и состояние циклической анимации."""

    def __init__(self, radius=200, points_count=180):
        """Задать радиус, число точек и начальное состояние круга."""
        if radius <= 0 or points_count < 3:
            raise ValueError("Радиус должен быть > 0, число точек >= 3")
        self.radius = radius
        self.points_count = points_count
        self.progress = 0.0
        # 1 — движение к треугольнику, -1 — обратно к кругу.
        self.direction = 1

    def triangle_radius(self, angle):
        """Вернуть расстояние до стороны треугольника вдоль луча."""
        sector = 2 * math.pi / 3
        vertex_angle = math.pi / 2
        side_angle = vertex_angle + math.pi / 3
        # Сводим угол к сектору одной стороны. Проекция расстояния
        # на нормаль к стороне равна радиусу вписанной окружности.
        delta = (angle - side_angle + sector / 2) % sector - sector / 2
        inner_radius = self.radius * math.cos(math.pi / 3)
        return inner_radius / math.cos(delta)

    def points(self, center_x, center_y):
        """Вернуть плоский список координат для Canvas.create_polygon."""
        result = []
        for i in range(self.points_count):
            angle = 2 * math.pi * i / self.points_count
            triangle_r = self.triangle_radius(angle)
            # Линейная интерполяция: 0 — круг, 1 — треугольник.
            radius = (self.radius * (1 - self.progress)
                      + triangle_r * self.progress)
            # На холсте ось Y направлена вниз, поэтому вычитаем синус.
            result.extend((center_x + radius * math.cos(angle),
                           center_y - radius * math.sin(angle)))
        return result

    def advance(self):
        """Сделать шаг и поменять направление на границе превращения."""
        self.progress += 0.01 * self.direction
        # Ограничиваем прогресс, чтобы фигура не выходила за крайние формы.
        if self.progress >= 1:
            self.progress = 1.0
            self.direction = -1
        elif self.progress <= 0:
            self.progress = 0.0
            self.direction = 1

    def reset(self):
        """Вернуть исходную окружность и прямое направление движения."""
        self.progress = 0.0
        self.direction = 1
