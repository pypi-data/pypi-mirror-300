from dataclasses import dataclass, field
from PIL import ImageFont
import random
import math
from .chart import Chart

@dataclass
class PieChart(Chart):
    def __post_init__(self):
        super().__post_init__()
        self.total = sum(self.data)
        self.radius = min(self.width, self.height) // 2 - self.margin
        self.center = (self.width // 2, self.height // 2)

    def draw_data(self, draw):
        start_angle = 0
        for i, value in enumerate(self.data):
            end_angle = start_angle + (value / self.total) * 360
            self.draw_pie_slice(draw, start_angle, end_angle, self.get_color(i))
            start_angle = end_angle

    def draw_pie_slice(self, draw, start_angle, end_angle, fill):
        draw.pieslice([
            (self.center[0] - self.radius, self.center[1] - self.radius),
            (self.center[0] + self.radius, self.center[1] + self.radius)
        ], start=start_angle, end=end_angle, fill=fill, outline='white')

    def draw_labels(self, draw, image):
        font = ImageFont.truetype("arial.ttf", 12)
        start_angle = 0
        for i, (value, label) in enumerate(zip(self.data, self.labels)):
            angle = start_angle + (value / self.total) * 360 / 2
            x = self.center[0] + int((self.radius + 20) * math.cos(math.radians(angle)))
            y = self.center[1] + int((self.radius + 20) * math.sin(math.radians(angle)))

            percentage = f"{value/self.total:.1%}"
            text = f"{label}: {percentage}"

            bbox = draw.textbbox((x, y), text, font=font)
            draw.rectangle(bbox, fill='white', outline='white')
            draw.text((x, y), text, fill='black', font=font, anchor='mm')

            start_angle += (value / self.total) * 360

    def get_color(self, index):
        colors = [
            (255, 99, 71),   # Tomato
            (60, 179, 113),  # Medium Sea Green
            (106, 90, 205),  # Slate Blue
            (255, 165, 0),   # Orange
            (30, 144, 255),  # Dodger Blue
            (255, 105, 180), # Hot Pink
            (50, 205, 50),   # Lime Green
            (255, 215, 0),   # Gold
        ]
        return colors[index % len(colors)]
