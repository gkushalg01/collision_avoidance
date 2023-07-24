import wx
import random
import math

class Bot:
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

def repulsive_force(Bot1, Bot2, min_distance=15):
    dx = Bot2.position[0] - Bot1.position[0]
    dy = Bot2.position[1] - Bot1.position[1]
    distance = math.hypot(dx, dy)

    if distance < min_distance:
        force = min_distance / distance
        Bot1.position = (Bot1.position[0] - dx * force, Bot1.position[1] - dy * force)
        Bot2.position = (Bot2.position[0] + dx * force, Bot2.position[1] + dy * force)

class Model(wx.Frame):
    Timer_ID = 1
    NumWhiteBots = 50
    NumBlueBots = 5

    def __init__(self, *args, **kw):
        super(Model, self).__init__(*args, **kw)

        self.SetTitle("Collision Avoidance")
        self.timer = wx.Timer(self, Model.Timer_ID)
        self.Bind(wx.EVT_TIMER, self.on_timer, id=Model.Timer_ID)
        self.red_Bot = Bot((400, 300), 10, wx.Colour(255, 0, 0), 2.0)
        self.white_Bots = [Bot(self.get_random_point_inside_circle(400, 300, 100), 5, wx.Colour(255, 255, 255), 1.0) for _ in range(Model.NumWhiteBots)]
        self.blue_Bots = [Bot(self.get_random_point_inside_circle(400, 300, 100), 5, wx.Colour(0, 0, 255), 3.0) for _ in range(Model.NumBlueBots)]
        self.timer.Start(10)  # Update every 10 milliseconds

        self.Bind(wx.EVT_PAINT, self.on_paint)

    def on_timer(self, event):
        self.move_Bots()
        self.Refresh()

    def move_Bots(self):
        for Bot in self.white_Bots:
            Bot.move_towards(self.red_Bot.position)

        for Bot in self.blue_Bots:
            Bot.move_towards(self.red_Bot.position)

        for i, Bot1 in enumerate(self.white_Bots):
            for Bot2 in self.white_Bots[i+1:]:
                repulsive_force(Bot1, Bot2)

        for Bot1 in self.white_Bots:
            for Bot2 in self.blue_Bots:
                repulsive_force(Bot1, Bot2, min_distance=25)

    def get_random_point_inside_circle(self, center_x, center_y, radius):
        while True:
            x = random.uniform(center_x - radius, center_x + radius)
            y = random.uniform(center_y - radius, center_y + radius)
            if math.hypot(x - center_x, y - center_y) <= radius:
                return (x, y)

    def on_paint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.draw_Bots(dc)

    def draw_Bots(self, dc):
        dc.Clear()

        for Bot in self.white_Bots:
            dc.SetBrush(wx.Brush(Bot.color))
            dc.DrawCircle(int(Bot.position[0]), int(Bot.position[1]), Bot.radius)

        for Bot in self.blue_Bots:
            dc.SetBrush(wx.Brush(Bot.color))
            dc.DrawCircle(int(Bot.position[0]), int(Bot.position[1]), Bot.radius)

        dc.SetBrush(wx.Brush(self.red_Bot.color))
        dc.DrawCircle(int(self.red_Bot.position[0]), int(self.red_Bot.position[1]), self.red_Bot.radius)

class MyApp(wx.App):
    def OnInit(self):
        frame = Model(None, wx.ID_ANY, "Collision Avoidance", size=(800, 600))
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()
