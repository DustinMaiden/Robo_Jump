from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ListProperty
from kivy.core.text import LabelBase
LabelBase.register(name="Robotech GP", fn_regular="ROBOTECH GP.ttf")

class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

#######################################################################################

class Beacon(Sprite):
    def __init__(self,pos):
        super(Beacon, self).__init__(source='beacon.png', pos=pos)

    #parabolic movement
    def update(self,count2):
        if self.y < dp(400):
            self.x -= count2
            self.y += count2 + count2

class Beacon2(Sprite):
    def __init__(self,pos):
        super(Beacon2, self).__init__(source='beacon.png', pos=pos)

    # parabolic movement
    def update(self):
         self.y += 1
         self.x += 1

##########################################################################################

class Platform(Sprite):
    def __init__(self,pos):
        super(Platform, self).__init__(source='atlas://platform_atlas/platform_1',pos=pos)
        self.isextended = 0

    def update(self,count):
        if count == 1:
            self.source='atlas://platform_atlas/platform_2'
        elif count == 2:
            self.source='atlas://platform_atlas/platform_3'
            self.isextended = 1;

        #elif count == 3:
         #   self.source='atlas://platform_atlas/platform_4'
        #elif count == 4:
         #   self.source='atlas://platform_atlas/platform_5'

    def extension(self):
        return self.isextended

###########################################################################################

class Title(Sprite):
    def __init__(self,pos):
        super(Title, self).__init__(pos=pos)
        self.roboTitle = Label(text = "Robo", font_name = 'Robotech GP', font_size = '150sp', pos = (dp(150), dp(450)))
        self.jumpTitle = Label(text = "Jump", font_name = 'Robotech GP', font_size = '150sp', pos = (dp(550), dp(450)))

    def update(self,count):
        if count == 1:
            self.add_widget(self.roboTitle)
        elif count == 3:
            self.imager2 = 1
            self.Beacon = Beacon(pos=(225, 0))
            self.parent.add_widget(self.Beacon)
            Clock.schedule_interval(self.update3, 1 / 10.0)
        elif count == 8:
            self.add_widget(self.jumpTitle)

    def update3(self, *ignore):
        self.Beacon.update(self.imager2)

        self.imager2 += 1

####################################################################################

class Player(Sprite):
    def __init__(self, pos):
        super(Player, self).__init__(source='atlas://robot_atlas/base', pos=pos)
        self.size = [75, 75]
        self.velocity_y = 0
        self.gravity = 0
        self.ready = 0

    def update(self):
        self.velocity_y += self.gravity
        self.y -= self.velocity_y
        if self.y<=180:
            self.velocity_y = 0
            self.gravity = 0

    def update2(self, count):
        if self.ready == 0 and count % 2 == 0:
            self.source = 'atlas://robot_atlas/walk_left'
            self.y += 3
        elif self.ready == 0 and count % 2 != 0:
            self.source = 'atlas://robot_atlas/walk_right'
            self.y += 3

        if self.y >= 180:
            self.ready = 1
            self.source = 'atlas://robot_atlas/base'

    def readiness(self):
        return self.ready


    def on_touch_down(self, *ignore):
        self.y+=125
        self.gravity = .5
        self.source = 'atlas://robot_atlas/jump'

############################################################################

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source = source)
        self.add_widget(self.image)
        self.size = self.image.size

class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source='background.png')
        self.size = self.background.size
        self.add_widget(self.background)

        self.Platform = Platform(pos=(190, 0))
        self.add_widget(self.Platform)

        self.Player = Player(pos=(330, 50))
        self.add_widget(self.Player)

        self.Title = Title(pos=(0,450))
        self.add_widget(self.Title)

        self.imager = 0
        self.l = "toot"
        self.j = "bang"
        Clock.schedule_interval(self.update, 1.0 / 60.0)
        Clock.schedule_interval(self.update2, 1)


    def update(self, *ignore):
        self.Player.update()


    def update2(self, *ignore):
        self.Platform.update(self.imager)

        if self.Platform.extension() == 1 and self.Player.readiness() == 0:
            self.l = Label(text='Hello world', font_color='white', pos=(250,250))
            self.add_widget(self.l)
            self.Player.update2(self.imager)
        elif self.Player.readiness() != 0:
            self.j = Label(text='Goodbye world', font_color='white', pos=(250,350))
            self.add_widget(self.j)

        if self.imager < 10:
            self.Title.update(self.imager)

        self.imager += 1

#######################################################################

class GameApp(App):
    def build(self):
        game =  Game()
        Window.size = game.size
        return game

if __name__ == "__main__":
    GameApp().run()



