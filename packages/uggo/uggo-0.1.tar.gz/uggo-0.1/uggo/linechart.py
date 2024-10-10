from dataclasses import dataclass, field
from PIL import ImageFont
import random
from .chart import Chart

@dataclass
class LineChart(Chart):
    def __post_init__(self):
        super().__post_init__()
        self.point_radius = 5
        self.line_width = 2
        self.x_step = (self.width - 2 * self.margin) / (len(self.data) - 1)

    def draw_data(self, draw):
        points = []
        for i, value in enumerate(self.data):
            x = self.margin + i * self.x_step
            y = self.height - self.margin - (value / self.max_value) * (self.height - 2 * self.margin)
            points.append((x, y))

        # Draw lines
        for i in range(len(points) - 1):
            draw.line([points[i], points[i+1]], fill='blue', width=self.line_width)

        # Draw points
        for point in points:
            draw.ellipse([point[0] - self.point_radius, point[1] - self.point_radius,
                          point[0] + self.point_radius, point[1] + self.point_radius], fill='red')

        # Draw x-axis labels
        label_font = ImageFont.truetype("arial.ttf", 12)
        for i, label in enumerate(self.labels):
            x = self.margin + i * self.x_step
            draw.text((x, self.height - self.margin + 10), label, fill='black', font=label_font, anchor='mt')
