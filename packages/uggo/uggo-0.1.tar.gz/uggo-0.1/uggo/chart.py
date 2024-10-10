from dataclasses import dataclass, field
from typing import List
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw, ImageFont

@dataclass
class Chart(ABC):
    width: int
    height: int
    data: List[float]
    labels: List[str]
    x_label: str = None
    y_label: str = None
    title: str = None
    margin: int = 70
    max_value: float = field(init=False)

    def __post_init__(self):
        self.max_value = max(self.data) if self.data else 0

    @abstractmethod
    def draw_data(self, draw):
        pass

    def draw(self):
        image = Image.new('RGB', (self.width, self.height), color='white')
        draw = ImageDraw.Draw(image)

        self.draw_data(draw)
        self.draw_title(draw)
        if (self.x_label and self.y_label):
            self.draw_axes(draw)
        self.draw_labels(draw, image)

        return image

    def draw_title(self, draw):
        if self.title:
            font = ImageFont.truetype("arial.ttf", 20)
            draw.text((self.width // 2, self.margin // 2), self.title, fill='black', font=font, anchor='mm')

    def draw_axes(self, draw):
        draw.line([(self.margin, self.height - self.margin),
                   (self.margin, self.margin)], fill='black', width=2)
        draw.line([(self.margin, self.height - self.margin),
                   (self.width - self.margin, self.height - self.margin)], fill='black', width=2)

    def draw_labels(self, draw, image):
        label_font = ImageFont.truetype("arial.ttf", 12)
        axis_font = ImageFont.truetype("arial.ttf", 14)

        # Draw y-axis labels
        for i in range(5):
            y = self.height - self.margin - i * (self.height - 2 * self.margin) / 4
            value = int(i * self.max_value / 4)
            draw.text((self.margin - 5, y), str(value), fill='black', font=label_font, anchor='rm')

        # Draw x-axis label
        x_label_pos = (self.width / 2, self.height - 10)
        draw.text(x_label_pos, self.x_label, fill='black', font=axis_font, anchor='ms')

        # Draw y-axis label
        y_label_pos = (10, self.height / 2)
        txt_img = Image.new('RGBA', axis_font.getsize(self.y_label), (255, 255, 255, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((0, 0), self.y_label, fill='black', font=axis_font)
        rotated_txt = txt_img.rotate(90, expand=1)
        y_label_pos = (int(y_label_pos[0]), int(y_label_pos[1]))
        image.paste(rotated_txt, y_label_pos, rotated_txt)
