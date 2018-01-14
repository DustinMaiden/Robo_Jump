from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.text import LabelBase
from kivy.config import Config
LabelBase.register(name="Robotech GP", fn_regular="ROBOTECH GP.ttf")


class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

#######################################################################################


class Beacon(Sprite):

    def __init__(self, pos):
        super(Beacon, self).__init__(source='beacon.png', pos=pos)

    def update(self, count2):
        if self.y < dp(300):
            self.x -= count2
            self.y += count2

        if self.x < dp(100):
            self.x += count2


class Beacon2(Sprite):

    def __init__(self, pos):
        super(Beacon2, self).__init__(source='beacon.png', pos=pos)

    # simple motion
    def update(self, count2):
        if self.y < dp(300):
            self.x += count2
            self.y += count2

        if self.x > dp(600):
            self.x -= count2

###########################################################################################


class Platform(Sprite):

    def __init__(self, pos):
        super(Platform, self).__init__(source='atlas://platform_atlas/platform_1',pos=pos)
        self.isextended = 0
        self.play_on = 0

    def open(self,count):
        if count == 1:
            self.source='atlas://platform_atlas/platform_2'
        elif count == 2:
            self.source='atlas://platform_atlas/platform_3'
            self.isextended = 1

    def close(self, count):
        if count == 1:
            self.source='atlas://platform_atlas/platform_4'
        elif count == 2:
            self.source='atlas://platform_atlas/platform_5'
        elif count == 3:
            self.imager2 = 1
            self.Beacon = Beacon(pos=(dp(225), dp(0)))
            self.parent.add_widget(self.Beacon)
            self.Beacon2 = Beacon2(pos=(dp(425), dp(0)))
            self.parent.add_widget(self.Beacon2)
            self.play_on = 1
            Clock.schedule_interval(self.update3, 1 / 10.0)

    def update3(self, *ignore):
        self.Beacon.update(self.imager2)
        self.Beacon2.update(self.imager2)
        self.imager2 += 1

    def extension(self):
        return self.isextended

    def ready_to_play(self):
        return self.play_on

#########################################################################################


class Title(Sprite):
    def __init__(self,pos):
        super(Title, self).__init__(pos=pos)
        self.roboTitle = Label(text = "Robo  Jump", font_name = 'Robotech GP', font_size = '150sp', pos = (dp(350), dp(500)))
        self.add_widget(self.roboTitle)


#########################################################################################


class Player(Sprite):
    def __init__(self, pos):
        super(Player, self).__init__(source='atlas://robot_atlas/base', pos=pos)
        self.size = [dp(75), dp(75)]
        self.jump = 0
        self.velocity_y = 0
        self.gravity = 0
        self.ready = 0

    def update(self):
        self.velocity_y += self.gravity
        self.y -= self.velocity_y

        if self.y <= dp(180):
            self.jump = 0
            self.velocity_y = 0
            self.gravity = 0

    def start_game(self, count):
        if self.ready == 0 and count % 2 == 0:
            self.source = 'atlas://robot_atlas/walk_left'
            self.y += dp(20)
        elif self.ready == 0 and count % 2 != 0:
            self.source = 'atlas://robot_atlas/walk_right'
            self.y += dp(20)

        if self.y >= dp(180):
            self.ready = 1
            self.source = 'atlas://robot_atlas/base'

    def readiness(self):
        return self.ready

    def on_touch_down(self, *ignore):
        self.jump = 1
        self.source = 'atlas://robot_atlas/jump'
        self.y += dp(125)
        self.gravity = 1

    def is_jump(self):
        return self.jump

############################################################################################


class Projectile(Sprite):
    def __init__(self, pos):
        super(Projectile, self).__init__(source='saw_blade.png', pos=pos)
        self.size = [dp(25), dp(25)]
        self.i = "bang"

        self.velocity_x = 20
        self.velocity_y = 0
        self.gravity = .12

    def update(self):
        self.velocity_y += self.gravity
        self.velocity_x = 5

        self.x += self.velocity_x
        self.y -= self.velocity_y


#############################################################################################

class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source = source)
        self.add_widget(self.image)
        self.size = self.image.size

##############################################################################################


class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.imager = 0
        self.imager3 = 0
        self.gameStart = 0
        self.counter = 0
        self.background1 = Background(source='background.png')
        self.size = self.background1.size

        Clock.schedule_interval(self.update_manager, 1.0 / 60.0)


    def start_game(self, pos):
        self.button1.x = dp(25)
        self.button1.y = dp(25)
        self.button1.text = 'Block Left'

        self.button2.x = dp(675)
        self.button2.y = dp(25)
        self.button2.text = 'Block Right'

        self.Platform = Platform(pos=(dp(215), dp(0)))
        self.add_widget(self.Platform)

        self.Player = Player(pos=(dp(365), dp(50)))
        self.add_widget(self.Player)

        self.Projectiles = []

        Clock.schedule_interval(self.startup, 1)
        Clock.schedule_interval(self.update, 1.0 / 60.0)


    def update(self, dt):
        self.counter += 1
        self.Player.update()
        if self.Platform.ready_to_play() == 1 and len(self.Projectiles) < 20:
            if self.counter % 25 == 0:
                Projectile_l = Projectile(pos=(dp(0), dp(425)))
                self.Projectiles.append(Projectile_l)
                self.add_widget(Projectile_l)

        for proj in self.Projectiles:
            proj.update()

        # if self.Platform.ready_to_play() == 1:

        #if self.Projectile.collide_widget(self.Player) and self.Player.is_jump() == 0:
         #   self.remove_widget(self.Title)

    def startup(self, *ignore):
        self.Platform.open(self.imager)

        if self.Platform.extension() == 1 and self.Player.readiness() == 0:
            self.Player.start_game(self.imager)
        elif self.Player.readiness() != 0:
            self.Platform.close(self.imager3)
            self.imager3 += 1

        self.imager += 1

    def update_manager(self, dt):
        if self.gameStart == 0:
            self.background = Background(source='background.png')
            self.add_widget(self.background)

            self.Title = Title(pos=(dp(250),dp(450)))
            self.add_widget(self.Title)

            self.button1 = Button(text = 'Start Game', pos=(dp(200), dp(275)))
            self.button1.bind(on_press=self.start_game)
            self.add_widget(self.button1)

            self.button2 = Button(text = 'Tutorial', pos=(dp(500), dp(275)))
            self.add_widget(self.button2)
            self.button2.bind(on_press=self.practice)
            self.gameStart = 1

    def practice(self, pos):
       self.button2.text='tomato'

##############################################################################################

class GameApp(App):
    def build(self):
        game =  Game()
        Window.size = game.size
        return game

if __name__ == "__main__":
    GameApp().run()



