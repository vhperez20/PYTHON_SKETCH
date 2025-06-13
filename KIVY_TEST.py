from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.utils import get_color_from_hex

class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.color = get_color_from_hex("#000000")  # Black

    def on_touch_down(self, touch):
        # Print the available touch attributes
        print("Touch profile:", touch.profile)
        for attr in touch.profile:
            print(f"{attr}: {getattr(touch, attr, None)}")

        # Start drawing
        pressure = getattr(touch, 'pressure', 1.0)
        width = 5 * pressure  # Base line width on pressure
        with self.canvas:
            Color(*self.color)
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=width)

    def on_touch_move(self, touch):
        pressure = getattr(touch, 'pressure', 1.0)
        width = 5 * pressure
        line = touch.ud.get('line')
        if line:
            line.points += [touch.x, touch.y]
            line.width = width  # Dynamically update width if possible

class PressureTestApp(App):
    def build(self):
        return DrawingWidget()

if __name__ == "__main__":
    PressureTestApp().run()
