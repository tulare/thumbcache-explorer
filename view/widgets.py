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
from helpers.observer import Observable, IObserver

@implementer(IObserver)
class ThumbsListbox(Tk.Listbox, Observable):

    def __init__(self, master=None, *args, **kwargs) :
        super(ThumbsListbox, self).__init__(master, *args, **kwargs)
        Observable.__init__(self)
        self.bind('<<ListboxSelect>>', self.select_action)

    def select_action(self, event) :
        """Event triggered when listbox selection change"""
        widget = event.widget
        selection = widget.curselection()
        if selection :
            index = int(selection[0])
            values = dict(zip(('index', 'title', 'size'), widget.get(index)))
            self.notify('detail', **values)

    def observer_action(self, *args, **kwargs) :
        """Populates the listbox with entries"""
        if 'populate' in args :
            self.delete(0, Tk.END)
            for entry in kwargs['entries'] :
                self.insert(Tk.END, entry)


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
        self.refresh()

    def refresh(self) :
        """ Mise à jour du Label : la photo est prioritaire sur l'url """
        if isinstance(self.photo, ImageTk.PhotoImage) :
            self.url = None
        else :
            self.photo = loadPhotoImage(self.url)
        self.config(image=self.photo)
                   
    def setUrl(self, url) :
        self.url = url
        self.photo = None
        self.refresh()

    def setPhoto(self, photo) :
        if isinstance(photo, ImageTk.PhotoImage) :
            self.photo = photo
        else :
            self.photo = ImageTk.PhotoImage(photo)
        self.refresh()

    def getPhoto(self) :
        return self.photo

