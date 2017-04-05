from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source = source)
        self.add_widget(self.image)
        self.size = self.image.size

class Player(Sprite):
    def __init__(self, pos):
        super(Player, self).__init__(source='robot_test_color2.png', pos=pos)
        self.velocity_y = 0
        self.gravity = 0

    def update(self):
        self.velocity_y += self.gravity
        #self.velocity_y = max(self.velocity_y, -10)
        self.y -= self.velocity_y
        if self.y<=10:
            self.velocity_y = 0
            self.gravity = 0

    def on_touch_down(self, *ignore):
        self.y+=125
        self.gravity = .5


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source='background.png')
        self.size = self.background.size
        self.add_widget(self.background)
        self.Player = Player(pos=(285, 0))
        self.add_widget(self.Player)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, *ignore):
        self.Player.update()

class GameApp(App):
    def build(self):
        game =  Game()
        Window.size = game.size
        return game

if __name__ == "__main__":
    GameApp().run()



