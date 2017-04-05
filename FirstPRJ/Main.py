import kivy
kivy.require('1.9.1') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.config import Config


Config.set('graphics','resizable',0) #don't make the app re-sizeable
#Graphics fix
Window.clearcolor = (0,0,0,1.)  #this fixes drawing issues on some phones

#Widget class - main widget containing game
class GUI(Widget):
    def __init__(self, **kwargs):
        super(GUI, self).__init__(**kwargs)
        l = Label(text='Not Your first Kivy App!')
        l.x = Window.width / 2 - l.width / 2
        l.y = Window.height / 2
        self.add_widget(l)

#Application class
class ClientApp(App):
    def build(self):
        #this is where the root widget goes
        #should be a canvas
        app = GUI()
        return app

if __name__ == '__main__' :
    ClientApp().run()



