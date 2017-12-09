# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk

import sys
from view.webimage import WebImage


class PhotoWindow(Tk.Toplevel, object) :
    def __init__(self, master=None, title='PhotoWindow', closeFunc=None) :
        super(PhotoWindow, self).__init__(master)
        self.title(title)
        self.closeFunc = closeFunc
        self.protocol('WM_DELETE_WINDOW', self._closeWindow)
        self.createWidgets()

    def createWidgets(self) :
        # preview
        self.labelPhoto = WebImage(self, url='https://dummyimage.com/256x256/888/000')
        self.labelPhoto.pack()
        self.placeholder = self.labelPhoto.getPhoto()

    def updatePhoto(self, image=None, title=None) :
        if image is None :
            self.labelPhoto.setPhoto(self.placeholder)
        else :
            self.labelPhoto.setPhoto(image)
            
        if title is not None :
            self.title(title)

    def _closeWindow(self) :
        if callable(self.closeFunc) :
            if self.closeFunc(self) is True :
                self.destroy()
