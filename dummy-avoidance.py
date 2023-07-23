import wx
import random
import math

class Dot:
    def __init__(self, position, radius, color, speed):
        self.position = position
        self.radius = radius
        self.color = color
        self.speed = speed
        self.velocity = (0, 0)

    def move_towards(self, target):
        direction = (target[0] - self.position[0], target[1] - self.position[1])
        length = math.hypot(direction[0], direction[1])
        if length > 0:
            direction = (direction[0] / length, direction[1] / length)
        self.velocity = (direction[0] * self.speed, direction[1] * self.speed)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

def repulsive_force(dot1, dot2, min_distance=15):
    dx = dot2.position[0] - dot1.position[0]
    dy = dot2.position[1] - dot1.position[1]
    distance = math.hypot(dx, dy)

    if distance < min_distance:
        force = min_distance / distance
        dot1.position = (dot1.position[0] - dx * force, dot1.position[1] - dy * force)
        dot2.position = (dot2.position[0] + dx * force, dot2.position[1] + dy * force)

class MyFrame(wx.Frame):
    Timer_ID = 1
    NumWhiteDots = 50
    NumBlueDots = 5

    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.SetTitle("Collision Avoidance")
        self.timer = wx.Timer(self, MyFrame.Timer_ID)
        self.Bind(wx.EVT_TIMER, self.on_timer, id=MyFrame.Timer_ID)
        self.red_dot = Dot((400, 300), 10, wx.Colour(255, 0, 0), 2.0)
        self.white_dots = [Dot(self.get_random_point_inside_circle(400, 300, 100), 5, wx.Colour(255, 255, 255), 1.0) for _ in range(MyFrame.NumWhiteDots)]
        self.blue_dots = [Dot(self.get_random_point_inside_circle(400, 300, 100), 5, wx.Colour(0, 0, 255), 3.0) for _ in range(MyFrame.NumBlueDots)]
        self.timer.Start(10)  # Update every 10 milliseconds

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_timer(self, event):
        self.move_dots()
        self.Refresh()

    def move_dots(self):
        for dot in self.white_dots:
            dot.move_towards(self.red_dot.position)

        for dot in self.blue_dots:
            dot.move_towards(self.red_dot.position)

        for i, dot1 in enumerate(self.white_dots):
            for dot2 in self.white_dots[i+1:]:
                repulsive_force(dot1, dot2)

        for dot1 in self.white_dots:
            for dot2 in self.blue_dots:
                repulsive_force(dot1, dot2, min_distance=25)

    def get_random_point_inside_circle(self, center_x, center_y, radius):
        while True:
            x = random.uniform(center_x - radius, center_x + radius)
            y = random.uniform(center_y - radius, center_y + radius)
            if math.hypot(x - center_x, y - center_y) <= radius:
                return (x, y)

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.draw_dots(dc)

    def draw_dots(self, dc):
        dc.Clear()

        for dot in self.white_dots:
            dc.SetBrush(wx.Brush(dot.color))
            dc.DrawCircle(int(dot.position[0]), int(dot.position[1]), dot.radius)

        for dot in self.blue_dots:
            dc.SetBrush(wx.Brush(dot.color))
            dc.DrawCircle(int(dot.position[0]), int(dot.position[1]), dot.radius)

        dc.SetBrush(wx.Brush(self.red_dot.color))
        dc.DrawCircle(int(self.red_dot.position[0]), int(self.red_dot.position[1]), self.red_dot.radius)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, wx.ID_ANY, "Collision Avoidance", size=(800, 600))
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
