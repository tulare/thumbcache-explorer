# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk
from six.moves import tkinter_ttk as ttk
from six.moves import tkinter_font as tkFont
from view.thumbview import ThumbcacheFrame
from view.window import PhotoWindow


class View(Tk.Tk, object) :

    def __init__(self, *args, **kwargs) :
        super(View, self).__init__(*args, **kwargs)
        self.title('Thumbcache View')

        self.createStyles()

        self.frame = ThumbcacheFrame(self)
        self.frame.pack(fill=Tk.BOTH, expand=1)

        self.thumbimage = None
        self.showImage()

        self.deiconify()

    def createStyles(self) :
        self._style = ttk.Style(master=self)

        self._fonts = {}
        self._fonts['ThumbListFont'] = tkFont.Font(
            family='Consolas',
            size=9
        )

        self._style.configure(
            'ThumbList.Treeview',
            font=self._fonts['ThumbListFont'],
            foreground='#555555'
        )

    def showImage(self, image=None, title='<sans titre>') :
        if not self.thumbimage :
            self.thumbimage = PhotoWindow(self, title, closeFunc=self.closeView)

        self.thumbimage.updatePhoto(image, title)

    def closeView(self, widget) :
        self.thumbimage = None
        return True

    @property
    def thumblist(self) :
        return self.frame.thumblist

if __name__ == '__main__' :
    import random
    sampleno = 0
    
    def add_sample() :
        global sampleno

        for n in range(100) :
            view.thumblist.insert(
                '', 'end',
                values=(
                    sampleno,
                    '{:016x}'.format(random.randint(0, 2**64)),
                    random.randint(0, 2**16)
                )
            )
            sampleno += 1
        
    view = View()
    view.bind('<<Populate>>', lambda event : add_sample()) 
    view.mainloop()
