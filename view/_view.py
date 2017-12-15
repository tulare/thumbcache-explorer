# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk
from view.thumbview import ThumbcacheFrame
from view.window import PhotoWindow


class View(Tk.Tk, object) :

    def __init__(self, *args, **kwargs) :
        super(View, self).__init__(*args, **kwargs)
        self.title('Thumbcache View')

        self.frame = ThumbcacheFrame()

        self.thumbimage = None
        self.showImage()

        self.deiconify()

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

