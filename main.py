from abc import ABC, abstractmethod
from random import randint
from time import sleep

class Observer(ABC):
    @abstractmethod
    def update(self, data):
        for (name, val) in data:
            setattr(self, name, val)
        
        self.on_change(self)
    
    @abstractmethod
    def on_change(self):
        pass


class Subject(ABC):

    @abstractmethod
    def __init__(self) -> None:
        self._observers = []
    
    def register(self, observer: Observer):
        self._observers.append(observer)

    def remove(self, observer: Observer):
        self._observers.remove(observer)

    def _get_vars(self):
        all_vars = self.__dict__.keys()
        return [(key, self.__dict__[key]) for key in all_vars if not key.startswith("_")]

    def notify(self):
        for observer in self._observers:
            observer.update(observer, self._get_vars())
    

class CpuSensor(Subject):
    
    # We must override the constructor, because of `abstractmethod` used in the parent 
    def __init__(self):
        super().__init__()

    def change_measurements(self, temp):
        self.temp = temp
        self.notify()





class CpuController(Observer):
    def on_change(self):
        print('\n')
        print("CpuController: ", end='')
        if self.temp > 90:
              print("Panic!")
        else:
              print("Everything under control")
    
class TempDisplay(Observer):
    def on_change(self):
        print("Display: ", end='')
        print(f'{self.temp} Deg')

cpu_sensor = CpuSensor() 
cpu_sensor.register(CpuController)
cpu_sensor.register(TempDisplay)


for i in range(10000):
    sleep(2)
    cpu_sensor.change_measurements(randint(50, 110))
