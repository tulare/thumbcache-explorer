# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk
from six.moves.urllib.request import urlopen

from io import BytesIO
from PIL import Image, ImageTk

from zope.interface import implementer
from helpers.observer import Observable


class ListboxObservable(Tk.Listbox, Observable):

    def __init__(self, master=None, *args, **kwargs) :
        super(ListboxObservable, self).__init__(master, *args, **kwargs)
        Observable.__init__(self)
        self.bind('<<ListboxSelect>>', self.onselect)

    def onselect(self, event) :
        widget = event.widget
        selection = widget.curselection()
        if selection :
            index = int(selection[0])
            value = widget.get(index)
            self.notify(index, value, widget=widget)


def loadPhotoImage(url) :
    try :
        img_bytes = urlopen(url).read()
        img_buffer = Image.open(BytesIO(img_bytes))
        photo = ImageTk.PhotoImage(img_buffer)
    except Exception as e :
        photo = None
    return photo


class WebImage(Tk.Label, object) :
    def __init__(self, master=None, url=None, photo=None, **config) :
        super(WebImage, self).__init__(master, config)
        self.url = url
        self.photo = photo
        self.update()

    def update(self) :
        """ Mise à jour du Label : la photo est prioritaire sur l'url """
        if isinstance(self.photo, ImageTk.PhotoImage) :
            self.url = None
        else :
            self.photo = loadPhotoImage(self.url)
        self.config(image=self.photo)
                   
    def setUrl(self, url) :
        self.url = url
        self.photo = None
        self.update()

    def setPhoto(self, photo) :
        if isinstance(photo, ImageTk.PhotoImage) :
            self.photo = photo
        else :
            self.photo = ImageTk.PhotoImage(photo)
        self.update()

    def getPhoto(self) :
        return self.photo

