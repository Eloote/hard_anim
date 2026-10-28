"""Проверки геометрии и смены направления анимации."""

import math
import unittest

from src.model import AnimationModel


class ModelTests(unittest.TestCase):
    """Проверить ключевые состояния независимо от графического окна."""

    def test_circle(self):
        """Начальная фигура имеет постоянный радиус."""
        model = AnimationModel()
        points = model.points(0, 0)
        for x, y in zip(points[::2], points[1::2]):
            self.assertAlmostEqual(math.hypot(x, y), 200)

    def test_triangle(self):
        """Вершины и середины сторон имеют ожидаемые радиусы."""
        model = AnimationModel()
        for i in range(3):
            angle = math.pi / 2 + i * 2 * math.pi / 3
            self.assertAlmostEqual(model.triangle_radius(angle), 200)
            self.assertAlmostEqual(
                model.triangle_radius(angle + math.pi / 3), 100)

    def test_cycle(self):
        """Модель достигает обеих границ и остаётся внутри диапазона."""
        model = AnimationModel()
        for _ in range(100):
            model.advance()
        self.assertAlmostEqual(model.progress, 1)
        self.assertEqual(model.direction, -1)
        for _ in range(100):
            model.advance()
        self.assertAlmostEqual(model.progress, 0)
        self.assertEqual(model.direction, 1)
        for _ in range(2000):
            model.advance()
            self.assertTrue(0 <= model.progress <= 1)

    def test_reset(self):
        """Сброс восстанавливает начальное состояние."""
        model = AnimationModel()
        model.advance()
        model.reset()
        self.assertEqual((model.progress, model.direction), (0, 1))


if __name__ == "__main__":
    unittest.main()
