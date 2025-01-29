
import sys
from collections.abc import Callable
from functools import update_wrapper

from Common.FlexibleMagicMock import FlexibleMagicMock
from Common.ControllerABC import ControllerABC
from Common.MVCHelperFunctions import (
    TestableControlFunction, do_all_control_method_calls, verify_object_field_has_mock_attributes
)


def CreateQtController(cls):
    '''
        A class decorator that makes an object into a controler.
        The controller expects to be called with a parent window,
        a model for underlying data which is not visible or editable
        to the user and a layout class containing the visual components
        of the GUI.

        If initializeUI is present, it will be checked and called.
        If initalizeModels is present, it will be checked and called.
    '''
    class QtController(cls):
        ''' Inner class for controller '''

        def __init__(self, parent_window, Model, Layout, *args, **kwargs):
            super().__init__(*args, **kwargs)

            parent_class = self.getControllerParentClass()
            if not issubclass(parent_class, ControllerABC):
                raise NotImplementedError(f"Class {parent_class.__name__} does not implement ControllerABC.")

            self.layout = Layout()
            self.layout.setupUi(parent_window)
            self.model = Model()
            self.parent = parent_window

            if 'MOCK_INTERFACES' in sys.argv:
                self.verifyModelAndLayoutAttributes()

            self.setup()
            update_wrapper(self, parent_class)  # Updates doc strings

        def setup(self):
            '''
                Unconventional practice:
                Since these are checked with a mock, they are called with a static method
            '''
            self.setupCallbacks(self)
            self.initializeModels(self)
            self.initializeUi(self)

        def verifyModelAndLayoutAttributes(self):
            '''
                Verify that everything that is callable refers to attributes that actually exist
            '''
            mock_controller = FlexibleMagicMock()
            self.setupCallbacks(mock_controller)
            do_all_control_method_calls(self, mock_controller)
            self.initializeModels(mock_controller)
            self.initializeUi(mock_controller)

            verify_object_field_has_mock_attributes(mock_controller, "layout", self.layout)
            verify_object_field_has_mock_attributes(mock_controller, "model", self.model)
            verify_object_field_has_mock_attributes(mock_controller, "parent", self.parent)

        def getControllerParentClass(self):
            return cls

    return QtController


class QtControlFunction:
    '''
        A decorator for static class functions which converts
        it into a testable function with given test arguments.
    '''
    def __init__(self, *test_args, **test_kwargs):
        self.test_args = test_args
        self.test_kwargs = test_kwargs

    def __call__(self, func: Callable):
        control_function = TestableControlFunction(func, self.test_args, self.test_kwargs)
        update_wrapper(control_function, func)
        return control_function
