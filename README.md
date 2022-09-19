Design Patterns are commonly tested solutions for problems developers face, one of the most known design patterns out there is the **Observer Pattern**,  it's pretty common with apps that have GUI. for example in JavaScript observers are offered by the browser API to easily detect changes in the state of the application.

# What is Observer Pattern? 🔭

The observer pattern is when you have a **Subject **object and many **Observers** objects with a one-to-many relation, each **Observer** is notified whenever the **Subject** state changes.

All **Observers** are able to unsubscribe and no longer get the **Subject** updates

### Is it the same as Pub/Sub Pattern? 🤔

No, the Publishers/Subscribers Pattern is similar but not the exact thing.
* Observer Pattern: observers are aware of the Subject, and the **Subject maintains a list of Observers**.

*  Pub/Sub: Publishers and Subscribers **know nothing about each other** and communicate using a message passing mechanism which makes it asynchronous.




# Implementation ⚙

![uml.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1663557651386/cVEMOxHcm.png align="left")

To make it easier to understand the implementation, we will design a simple CPU temperature monitor.
Our design will have two abstract classes called `Subject` and `Observer`, where`CpuSensor` will inherit the `Subject` class while the `CpuController` and `TempDisplay` will inherit the `Observer` class.

`TempDisplay` is responsible for displaying temperature, while `CpuController` will perform dummy actions upon the last temperature read.



### Subject

First, import ```ABC``` and ```abstractmethod``` from the built in library ```abc``` which allows us to do abstract classes

```python
from abc import ABC, abstractmethod
```
We will create the class, and make it extends ABC

```python
class Subject(ABC):
    
```
in the constructor, we will instantiate a private variable called `_observers` with an empty array to track the **observers**, adding the `abstractmethod` decorator to prevent `Subject` to be instiniated.

```python
class Subject(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._observers = []
```

After that, the `register` and `unregister` methods will be added, so the observers can subscribe and unsubscribe from the Subject

```python
class Subject(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def remove(self, observer):
        self._observers.remove(observer)
```

Then, the `notify` function will be declared, which is responsible for updating observers with the new data, for now, we will just leave it empty.

```python
class Subject(ABC):
    @abstractmethod
    def __init__(self) -> None:
        self._observers = []

    def register(self, observer):
        self._observers.append(observer)

    def remove(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            pass
```


### Observer

Just like the `Subject`, the `Observer` class should extends `ABC`


 ```python
class Observer(ABC):
```

Adding two abstract methods, `on_change` and `update`, both have `abstractmethod` decorator.

* `update`: inject data to the observer and call `on_change`
* `on_change`: empty function

```python
class Observer(ABC):
    @abstractmethod
    # data is array of tuples of (dataName, Value)
    def update(self, data):
        for (name, val) in data:
            setattr(self, name, val)
        
        self.on_change(self)
    
    @abstractmethod
    def on_change(self):
        pass
```


### Connect `Observer` with `Subject` ⚔

Let's get back to the `Subject` class and complete `notify` logic.

Since we know that each observer has the `update` function, we will call that for each observer, but as you know the `update` function receives data in an array, to do that, we will have a private function called `_get_vars` which will arrange all public variables of the `Subject` in array.

```python
class Subject(ABC):
# ...
  def _get_vars(self):
      all_vars = self.__dict__.keys() # get all keys
      # filters all vars that don't start '_'
      # and returns them as an array of tuple that has the name and the value
      return [(key, self.__dict__[key]) for key in all_vars if not key.startswith("_")]
  def notify(self):
          for observer in self._observers:
              observer.update(observer, self._get_vars())
```


### `CpuSensor`

In the `CpuSensor` class, we will:

* Extend `Subject`
* Call the parent constructor
* Implement `change_measurements`


```python
class CpuSensor(Subject):
    
    # We must override the constructor, because of `abstractmethod` used in the parent 
    def __init__(self):
        super().__init__()

    def change_measurements(self, temp):
        self.temp = temp
        self.notify()
```


### `CpuController` and `TempDisplay`

Because we want `CpuController` and `TempDisplay` to be observers, we will have them extends `Observer`, we will also override the `on_change` function on both observers, so the `TempDisplay` will print temperature, where the `CpuController` will print "panic" if the temperature gets more than 90°.

```python

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

```



### Driver 🏎

It's time now to set up a driver and test our CPU monitor 😁

We will add a few built-in functions to help us.

```python
from random import randint
from time import sleep
```


then

```python
cpu_sensor = CpuSensor() 
cpu_sensor.register(CpuController)
cpu_sensor.register(TempDisplay)

for i in range(10000):
    sleep(2)
    cpu_sensor.change_measurements(randint(50, 110))

```

Output

```bash
CpuController: Everything under control
Display: 56 Deg


CpuController: Everything under control
Display: 74 Deg


CpuController: Panic!
Display: 97 Deg
```



# Conclusion

One drawback of this pattern is that it can lead to a memory leak if the observers were not removed from the `Subject` class, because it holds a strong reference to the **observers**, for instance, if these observers were UI components that are no longer appears on the screen but still registered in some `Subject`, the `Subject` will keep re-rendering these invisible components and waste CPU cycles on them, this issue known as [Lapsed Listener Problem](https://en.wikipedia.org/wiki/Lapsed_listener_problem)

That was the Observer pattern, with a practical example you can build on top of it, if you are interested in reading real CPU temperatures you can check this cool cross-platform package [pyspectator](https://pypi.org/project/pyspectator/)

