# -*- encoding: utf-8 -*-

from zope.interface import Interface, Attribute, implementer

class IObserver(Interface) :
    def update(*args, **kwargs) :
        """Method called when observable notify change"""


class IObservable(Interface) :

    observers = Attribute("""set of observers of the observable""")

    def register(observer) :
        """Add an observer to this observable"""

    def unregister(observer) :
        """Remove an observer from this observable"""

    def unregister_all() :
        """Remove all observers from this observable"""

    def notify(*args, **kwargs) :
        """Notify all observers of this observable with theses arguments"""

@implementer(IObservable)
class Observable(object) :

    def __init__(self) :
        self.observers = set()

    def register(self, observer) :
        if not IObserver.providedBy(observer) :
            raise ValueError("Object is not an IObserver")
        self.observers.add(observer)

    def unregister(self, observer) :
        self.observers.remove(observer)

    def unregister_all(self) :
        self.observers.clear()
        
    def notify(self, *args, **kwargs) :
        for observer in self.observers :
            observer.update(*args, **kwargs)

