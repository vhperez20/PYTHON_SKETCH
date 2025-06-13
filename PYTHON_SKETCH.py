import tkinter as tk
from tkinter.colorchooser import askcolor
from PIL import ImageGrab

# Pressure and touch
from kivy.graphics import Color, Line
from kivy.utils import get_color_from_hex

class AdvancedSketchPad:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sketch Pad")

        self.brush_color = "black"
        self.brush_size = 3
        self.undo_stack = []

        self.canvas = tk.Canvas(self.root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

        self.last_x = None
        self.last_y = None

        control_frame = tk.Frame(self.root)
        control_frame.pack()

        tk.Button(control_frame, text="Clear", command=self.clear_canvas).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Undo", command=self.undo).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Color", command=self.choose_color).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Save", command=self.save_canvas).pack(side=tk.LEFT)

        tk.Label(control_frame, text="Brush Size:").pack(side=tk.LEFT)
        self.size_slider = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL, command=self.change_brush_size)
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side=tk.LEFT)

    def draw(self, event):
        if self.last_x and self.last_y:
            line = self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.brush_color, width=self.brush_size,
                capstyle=tk.ROUND, smooth=True
            )
            self.undo_stack.append(line)
        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.undo_stack.clear()

    def undo(self):
        if self.undo_stack:
            self.canvas.delete(self.undo_stack.pop())

    def choose_color(self):
        color = askcolor(title="Select Brush Color")
        if color[1]:
            self.brush_color = color[1]

    def change_brush_size(self, val):
        self.brush_size = int(val)

    def save_canvas(self):
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        img = ImageGrab.grab().crop((x, y, x1, y1))
        img.save("sketch.png")
    
    def on_touch_move(self, touch):
        pressure = getattr(touch, 'pressure', 1.0)
        width = max(1, 10 * pressure)
        with self.canvas:
            Color(*self.current_color)
            Line(points=(touch.x, touch.y), width=width)
        print("Touch info:", touch.profile)
        print ("Pressure:", pressure)
        for attr in touch.profile:
            print(f"{attr}:", getattr(touch, attr, None))


if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedSketchPad(root)
    root.mainloop()

