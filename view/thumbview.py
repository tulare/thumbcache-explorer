# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk

from zope.interface import implementer
from helpers.observer import IObserver

from view.window import PhotoWindow
from view.widgets import ListboxObservable

from model.thumbcache import THMBC_DBS, Thumbcache

@implementer(IObserver)
class ThumbcacheFrame(Tk.Frame, object) :
    def __init__(self, master=None) :
        super(ThumbcacheFrame, self).__init__(master)
        self.master.title('Thumbcache View')
        self.pack()
        self.createWidgets()
        self.populate()
        self.showImage()

    def createWidgets(self) :
        # Action
        Tk.Button(self,
            text='Regénération cache',
            command=self.populate
        ).pack(fill=Tk.X)
        
        # Listbox
        self.thumblist = ListboxObservable(self, height=25, width=40)
        self.thumblist.pack(side=Tk.LEFT)
        #self.thumblist.bind('<ButtonRelease-1>', self.showImage)
        self.thumblist.add_observer(self)

        # preview
        self.thumbimage = None

        # radiobuttons
        self.cachefile = Tk.StringVar()
        for label, cachefile in THMBC_DBS.items() :
            Tk.Radiobutton(self,
                    text=label,
                    variable=self.cachefile,
                    value=cachefile,
                    command=self.populate
            ).pack(anchor=Tk.W)
        self.cachefile.set(THMBC_DBS['256x256'])

        # checkbox zero
        self.zero = Tk.BooleanVar()
        self.ckZero = Tk.Checkbutton(self,
                                     text='Images vides',
                                     variable=self.zero,
                                     command=self.populate)
        self.ckZero.pack(anchor=Tk.W)

    def update(self, *args, **kwargs) :
        try :
            index, value = args
            image = self.cache.getImage(index=int(value.split()[0]))
            title = value.split()[2]
            self.showImage(image, title)
        except Exception as e :
            print(e)

    def showImage(self, image=None, title='<Inconnu>') :
        if not self.thumbimage :
            self.thumbimage = PhotoWindow(self, title, closeFunc=self.closeView)

        self.thumbimage.updatePhoto(image, title)
        

    def closeView(self, widget) :
        self.thumbimage = None
        return True
        
    def populate(self) :
        self.thumblist.delete(0, Tk.END)
        self.cache = Thumbcache(self.cachefile.get(), cached=True)
        
        for indice, entry in enumerate(self.cache) :
            listEntry = '{:9d} - {:x} - {:6d}'.format(
                indice, entry.entryHash, entry.dataSize
            )
            if not self.zero.get() and entry.dataSize == 0 :
                continue
            self.thumblist.insert(Tk.END, listEntry)

if __name__ == "__main__" :
    app = ThumbcacheFrame()
    app.mainloop()
