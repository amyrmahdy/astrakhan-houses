from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.core.window import Window
from clustering import general
import matplotlib.pyplot as plt

class BoxLayoutExample(BoxLayout):       
    def __init__(self, **kwargs):
        super(BoxLayoutExample, self).__init__(**kwargs)
        Window.bind(on_request_close=self.end_func)
    def end_func(self, *args):
        plt.close('all')
        CianApp().stop()
        Window.close()  
    try:
        TIPDOMA = StringProperty('кирпичный')
        TIPREMONT = StringProperty('не важно')
        ALGORITHM = StringProperty('DBSCAN')
        def clicked_button(self,button,min_area,max_area,eps):
            if button.text == "Баз. кластеры":
                general(0,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)
            elif button.text == "Без оценки":
                general(1,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)            
            elif button.text == "С оценкой":
                general(2,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)
            elif button.text == "Детали":
                general(3,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)
            elif button.text == "Кластеризация":
                general(4,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)
            elif button.text == "Предсказание":
                general(5,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)
            elif button.text == "Вместе":
                general(6,float(min_area.text),float(max_area.text),self.TIPDOMA,self.TIPREMONT,float(eps.text),self.ALGORITHM)

    except Exception as e:
        print("Error in UI")
        print(e)


class CianApp(App):
    pass


CianApp().run()

