# -*- encoding: utf-8 -*-

# python 2/3 compatibility
from __future__ import (
    absolute_import, print_function, division,
    unicode_literals
    )

from six.moves import tkinter as Tk
from six.moves.urllib.request import urlopen

import sys
from io import BytesIO
from PIL import Image, ImageTk

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

if __name__ == '__main__' :
    root = Tk.Tk()

    demo_url1 = 'https://dummyimage.com/320x270/999/fff'
    demo_url2 = 'https://dummyimage.com/320x270/fff/999'
    photo1 = None
    photo2 = loadPhotoImage(demo_url2)

    def echangePhotos(event=None) :
        global photo1, photo2
        photo1 = img.getPhoto()
        photo1, photo2 = photo2, photo1
        img.setPhoto(photo1)
        
    Tk.Button(root, text='Quitter', command=root.destroy).pack(fill=Tk.X)
    Tk.Button(root, text='Changer', command=echangePhotos).pack(fill=Tk.X)
    img = WebImage(root, url=demo_url1)
    img.pack(side=Tk.LEFT, fill=Tk.X)
    img2 = WebImage(root, photo=photo2)
    img2.pack(fill=Tk.X)

    root.mainloop()
    
