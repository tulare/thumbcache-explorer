from controller import *

from model import Model
from view import View

if __name__ == '__main__' :

    model = Model()
    view = View()
    controller = Controller(model, view)
    controller.run()
