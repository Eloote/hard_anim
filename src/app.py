"""Окно Tkinter и отрисовка анимации."""

import tkinter as tk
from tkinter import ttk

from src.model import AnimationModel


class AnimationApp:
    """Управлять окном, таймером и отображением модели."""

    def __init__(self):
        """Создать холст и элементы управления."""
        self.model = AnimationModel()
        self.paused = False
        self.window = tk.Tk()
        self.window.title("Hard anim — круг и треугольник")
        self.window.resizable(False, False)
        self.field = tk.Canvas(self.window, width=700, height=650,
                               bg="white", highlightthickness=0)
        self.field.pack()
        # Создаём один многоугольник, затем меняем только его координаты.
        self.polygon = self.field.create_polygon(
            self.model.points(350, 325), outline="black", fill="", width=3)
        controls = ttk.Frame(self.window, padding=10)
        controls.pack(fill="x")
        self.pause_button = ttk.Button(
            controls, text="Пауза", command=self.toggle_pause)
        self.pause_button.pack(side="left")
        ttk.Button(controls, text="Сброс", command=self.reset).pack(
            side="left", padx=8)
        ttk.Label(controls, text="Пробел — пауза • R — сброс").pack(
            side="right")
        # Клавиши вызывают те же обработчики, что и кнопки.
        self.window.bind("<space>", self.toggle_pause)
        self.window.bind("<KeyPress-r>", self.reset)
        self.window.bind("<KeyPress-R>", self.reset)
        self.window.after(20, self.animate)

    def toggle_pause(self, event=None):
        """Переключить паузу кнопкой или клавишей пробела."""
        self.paused = not self.paused
        self.pause_button.configure(
            text="Продолжить" if self.paused else "Пауза")
        return "break"

    def reset(self, event=None):
        """Показать исходный круг и остановить анимацию для осмотра."""
        self.model.reset()
        self.paused = True
        self.pause_button.configure(text="Продолжить")
        self.field.coords(self.polygon, *self.model.points(350, 325))
        return "break"

    def animate(self):
        """Обновить фигуру и запланировать следующий кадр через 20 мс."""
        if not self.paused:
            self.model.advance()
            self.field.coords(self.polygon, *self.model.points(350, 325))
        # after не блокирует окно: кнопки остаются доступными и на паузе.
        self.window.after(20, self.animate)

    def run(self):
        """Запустить главный цикл обработки событий."""
        self.window.mainloop()
