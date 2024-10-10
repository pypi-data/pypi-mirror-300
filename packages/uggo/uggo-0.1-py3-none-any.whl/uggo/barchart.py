from dataclasses import dataclass, field
from PIL import ImageFont
import random
from .chart import Chart

@dataclass
class BarChart(Chart):
    gap_percentage: float = 0.2
    bar_width: float = field(init=False)
    gap_width: float = field(init=False)

    def __post_init__(self):
        super().__post_init__()
        self.bar_width = (self.width - 2 * self.margin) / (len(self.data) * (1 + self.gap_percentage))
        self.gap_width = self.bar_width * self.gap_percentage

    def draw_data(self, draw):
        for i, value in enumerate(self.data):
            x = self.margin + i * (self.bar_width + self.gap_width)
            y = self.height - self.margin - (value / self.max_value) * (self.height - 2 * self.margin)
            draw.rectangle([x, y, x + self.bar_width, self.height - self.margin], 
                           fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # Draw x-axis labels
        label_font = ImageFont.truetype("arial.ttf", 12)
        for i, label in enumerate(self.labels):
            x = self.margin + i * (self.bar_width + self.gap_width) + self.bar_width / 2
            draw.text((x, self.height - self.margin + 10), label, fill='black', font=label_font, anchor='mt')
