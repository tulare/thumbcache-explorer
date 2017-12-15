# -*- encoding: utf-8 -*-

from model import Model
from view import View
from controller import Controller

model = Model()
view = View()
controller = Controller(model, view)
controller.run()

