# -*- encoding: utf-8 -*-

from zope.interface import implementer
from helpers.observer import IObserver

@implementer(IObserver)
class Controller(object) :

    def __init__(self, model, view) :
        self.model, self.view = model, view
        self.bind_model()
        self.bind_view()

    def bind_model(self) :
        self.model.add_observer(self.view.thumblist)

    def bind_view(self) :
        self.view.bind('<<Populate>>', self.populate)
        self.view.thumblist.add_observer(self)

    def run(self) :
        self.view.mainloop()

    def observer_action(self, *args, **kwargs) :
        if 'detail' in args :
            index, title, size = kwargs['values']
            title = '{} - {}'.format(index, title)
            image = self.model.getImage(index)
            self.view.showImage(image, title)

    def populate(self, event) :
        widget = event.widget
        self.model.build(
            widget.cachefile.get(),
            widget.empty.get()
            )
