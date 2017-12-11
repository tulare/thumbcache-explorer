# -*- encoding: utf-8 -*-

from zope.interface import Interface, Attribute, implementer

class IObserver(Interface) :
    def update(*args, **kwargs) :
        """Method called when observable notify change"""


class IObservable(Interface) :

    observers = Attribute("""set of observers of the observable""")

    def add_observer(observer) :
        """Add an observer to this observable"""

    def remove_observer(observer) :
        """Remove an observer from this observable"""

    def remove_all_observers() :
        """Remove all observers from this observable"""

    def notify(*args, **kwargs) :
        """Notify all observers of this observable with theses arguments"""

@implementer(IObservable)
class Observable(object) :

    def __init__(self) :
        self.observers = set()

    def add_observer(self, observer) :
        if not IObserver.providedBy(observer) :
            raise ValueError("Object is not an IObserver")
        self.observers.add(observer)

    def remove_observer(self, observer) :
        self.observers.remove(observer)

    def remove_all_observers(self) :
        self.observers.clear()
        
    def notify(self, *args, **kwargs) :
        for observer in self.observers :
            observer.update(*args, **kwargs)

