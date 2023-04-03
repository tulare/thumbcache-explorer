# -*- encoding: utf-8 -*-

from model import *

from helpers.observer import IObserver
from zope.interface import implementer

@implementer(IObserver)
class Observer(object) :
    def observer_action(self, *args, **kwargs) :
        print(args, kwargs)


if __name__ == '__main__' :
    
    model = Model()
    model.add_observer(Observer())

    model.build(empty=True)
    print('--------------------------------------------------------')
    model.build()
    print('--------------------------------------------------------')
    model.build(cachefile=TC_DBS['32x32'])
    

