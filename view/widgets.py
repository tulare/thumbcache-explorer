# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk
from six.moves import tkinter_ttk as ttk
from six.moves import tkinter_font as tkFont
from six.moves.urllib.request import Request, urlopen

from io import BytesIO
from PIL import Image, ImageTk

from zope.interface import implementer
from helpers.observer import Observable, IObserver

@implementer(IObserver)
class ThumbsListbox(Tk.Listbox, Observable) :

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
            values = dict(zip(('index', 'offset', 'title', 'size'), widget.get(index)))
            self.notify('detail', **values)

    def observer_action(self, *args, **kwargs) :
        """Populates the listbox with entries"""
        if 'populate' in args :
            self.delete(0, Tk.END)
            for entry in kwargs['entries'] :
                self.insert(Tk.END, entry)

@implementer(IObserver)
class ThumbsListboxMulti(ttk.Treeview, Observable) :

    def __init__(self, master=None, headings=None, *args, **kwargs) :
        super(ThumbsListboxMulti, self).__init__(master, *args, **kwargs)
        Observable.__init__(self)
        self.bind('<<TreeviewSelect>>', self.select_action)

        # configure columns and select mode
        self.headings = headings
        self.config(
            selectmode='browse',
            columns=list(heading[0] for heading in self.headings),
            show='headings'
        )
        self.create_headings()
            
    def create_headings(self) :
        """Reset columns headings to default"""
        for colno, heading in enumerate(self.headings) :
            self.heading(colno, text=heading[0].title())
            self.column(colno, **heading[1])
        

    def select_action(self, event) :
        """Event triggered when listbox selection change"""
        widget = event.widget
        selection = widget.selection()
        if selection :
            item = widget.item(selection[0])
            self.notify('detail', values=item['values'])

    def observer_action(self, *args, **kwargs) :
        """Populates the listbox with entries"""
        if 'populate' in args :
            # discard previous content
            self.delete(*self.get_children())

            # restore headings defaults
            self.create_headings()

            # append entries
            for entry in kwargs['entries'] :
                self.insert('', Tk.END, values=entry)


def loadPhotoImage(url) :
    req = Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    try :
        img_bytes = urlopen(req).read()
        img_buffer = Image.open(BytesIO(img_bytes))
        photo = ImageTk.PhotoImage(img_buffer)
    except Exception as e :
        print(e)
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

