# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk

from view.widgets import ThumbsListbox
from model import THMBC_DBS


class ThumbcacheFrame(Tk.Frame, object) :
    def __init__(self, master=None, *args, **kwargs) :
        super(ThumbcacheFrame, self).__init__(master, *args, **kwargs)
        self.pack(fill=Tk.BOTH, expand=1)
        self.createWidgets()
        self.populate()

    def createWidgets(self) :
        # Action Button
        Tk.Button(self,
            text='Regénération cache',
            command=self.populate
        ).pack(side=Tk.TOP, fill=Tk.X)
        
        # Listbox
        self.thumblist = ThumbsListbox(self, height=25, width=35)
        self.thumblist.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)

        # radiobuttons
        self.cachefile = Tk.StringVar()
        for label, cachefile in THMBC_DBS.items() :
            Tk.Radiobutton(
                self,
                text=label,
                variable=self.cachefile,
                value=cachefile,
                command=self.populate
            ).pack(anchor=Tk.W)
        self.cachefile.set(THMBC_DBS['256x256'])

        # checkbox empty
        self.empty = Tk.BooleanVar()
        Tk.Checkbutton(
            self,
            text='Images vides',
            variable=self.empty,
            command=self.populate
        ).pack(anchor=Tk.W)
        
    def populate(self) :
        self.update()
        self.event_generate('<<Populate>>', when='tail')
        

if __name__ == "__main__" :
    app = ThumbcacheFrame()
    app.pack()
    app.mainloop()
